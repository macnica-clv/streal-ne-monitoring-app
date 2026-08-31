import time
from typing import Tuple
from Models.Hizmil_Driver import (HizmilDriver, ResultKind, ModeKind, StateKind, AccData, RegData,
                                  StrealData, MeasureData, SerialCommon, ConnectionStatus)
from Models.Board import Board, BoardKind
from decimal import Decimal, ROUND_HALF_UP
from Models.Sensor import SensorChKind, RegPageKind, SensorConnectionStatusKind, SensorTypeKind
from Models.SensorSR300 import RegAddrKindSR300
from Models.SensorSR500 import RegAddrKind

import socket
import threading
import time
from typing import List, Callable, Optional

class HizmilDriverLANSR300(HizmilDriver):
    def __init__(self, ip: list[str], port: str):
        super().__init__()
        self._ser = None
        self._lock = threading.Lock()
        self._recv_event = threading.Event()
        self._resp_ok = True
        self.version = bytearray(4)
        self._sampling_count = 0
        self.offset_strain = [0]*(self.ch_max)
        self.offset_temp:list[float] = [0]*(self.ch_max)

        self._rx_thread = None
        self._running = False

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.myIpAddr = ip
        self.myPort = port
        self._tcp_serial = [TcpSerial(), TcpSerial()]
        self._lock_cmd = [threading.Lock(), threading.Lock()]
        self._current_cmd = [0, 0]
        self._recv_event = [threading.Event(), threading.Event()]
        self._resp_ret = [False, False]

        self._timeout = 5.0

        self._check_status_thread = None

    def connect(self, com: list[str]) -> ConnectionStatus:
        result = ResultKind.response_error
        if self._is_connected:
            return ConnectionStatus.other_error

        # ★再接続時の増殖対策（おすすめ）
        self.board.clear()

        # board定義（従来通り）
        self._tcp_serial[0]._data_received_handler = self.data_received_callback1
        self.board.append(Board(BoardKind.board1, self.sensor_ch_max, SensorTypeKind.sr300))
        self._tcp_serial[1]._data_received_handler = self.data_received_callback2
        self.board.append(Board(BoardKind.board2, self.sensor_ch_max, SensorTypeKind.sr300))

        connected_any = False

        for i in range(BoardKind.board_num.value):
            # 0.0.0.0 は未使用扱い
            if com[i] == "0.0.0.0":
                self.board[i].is_connected = False
                continue

            # TCP接続
            ret = self._tcp_serial[i].connect(com[i], 1024)
            if not ret:
                self._tcp_serial[i].close()
                self.board[i].is_connected = False
                continue  # ★breakしない

            # バージョン取得で疎通確認
            result = self.get_board_version(self.board[i].board_no)
            if result != ResultKind.ok:
                self._tcp_serial[i].close()
                self.board[i].is_connected = False
                continue  # ★breakしない

            self.board[i].is_connected = True
            connected_any = True

        # ★1台も繋がってないなら従来通り失敗
        if not connected_any:
            for s in self._tcp_serial:
                s.close()
            return ConnectionStatus.board_not_detected

        # ★ここから先は「1台以上接続済み」として進める
        self._is_connected = True

        if self.is_timestamp:
            _ = self.set_time()

        # ---- センサ接続確認（従来ロジックを活かす）
        sensor_num = 0
        for ch in range(self.ch_max):
            if self.board[ch // self.sensor_ch_max].is_connected:
                for page in range(RegPageKind.sensor_reg_page_num.value):
                    ret, _ = self.read_reg_page(ch, page)
                    if ret != ResultKind.ok:
                        continue
                    ret, _ = self.get_status(ch)
                    if ret != ResultKind.ok:
                        continue
                    sensor_num += 1

        if sensor_num == 0:
            return ConnectionStatus.sensor_not_detected

        self._check_status_thread = threading.Thread(target=self.check_status, daemon=True)
        self._check_status_thread.start()
        return ConnectionStatus.success

    def disconnect(self, com: list[str]):
        result = "OK"
        self._is_connected = False

        for tcp in self._tcp_serial:
            if tcp is not None:
                tcp.close()

        # クールダウン（次のconnectが安定しやすい）
        time.sleep(0.2)
        return result

    def get_version(self, version: list[int]) ->  ResultKind:
        """
        バージョン取得
        version: バージョンを格納するbytearray
        戻り値: 結果（"OK" など）
        """
        result1 = self.get_board_version(BoardKind.board1)
        if result1 == ResultKind.ok:
            version[0] = self.board[0].version
        else:
            version[0] = 0

        result2 = self.get_board_version(BoardKind.board2)
        if result2 == ResultKind.ok:
            version[1] = self.board[1].version
        else:
            version[1] = 0

        if result1 != ResultKind.ok:
            result = result1
        elif result2 != ResultKind.ok:
            result = result2
        else:
            result = ResultKind.ok

        return result

    def get_board_version(self, board:BoardKind) ->  ResultKind:
        """
        バージョン取得
        version: バージョンを格納するbytearray
        戻り値: 結果（"OK" など）
        """
        cmd = bytearray(1)
        cmd[0] = self.TRIMMINGIF_CMD_GET_VER

        result = self.do_command(board, cmd)

        return result

    def start_measure(self, interval: int, mode: ModeKind) -> ResultKind:
        """
        計測開始
        interval: 計測周期
        mode: 計測モード
        戻り値: 結果 ("OK" など)
        """
        cmd = bytearray(6)
        cmd[0] = self.TRIMMINGIF_CMD_START_MEASURE
        cmd[1] = (interval & 0x000000FF)
        cmd[2] = (interval & 0x0000FF00) >> 8
        cmd[3] = (interval & 0x00FF0000) >> 16
        cmd[4] = (interval & 0xFF000000) >> 24
        cmd[5] = mode.value

        result = self.do_command(BoardKind.board_num, cmd)

        if result == ResultKind.ok:
            self.is_measuring = True

        return result

    def stop_measure(self) -> ResultKind:
        """
        計測停止
        戻り値: 結果 ("OK" など)
        """
        cmd = bytearray(1)
        cmd[0] = self.TRIMMINGIF_CMD_STOP_MEASURE
        result = self.do_command(BoardKind.board_num, cmd)

        if result == ResultKind.ok:
            self.is_measuring = False

        return result

    def write_reg(self, ch: int, page: int, data: list[RegData]) -> ResultKind:
        board, board_ch = self.get_board_ch(ch)
        count = len(data)
        size = 2 + count * 3
        addr_index_base = 2
        data_index_base1 = 3
        data_index_base2 = 4
        cmd = bytearray(size)

        if page > self.PAGE_UPPER_LIMIT or page < self.PAGE_LOWER_LIMIT or board_ch > self.CH_UPPER_LIMIT or board_ch < self.CH_LOWER_LIMIT:
            result = ResultKind.parameter_error
        else:
            cmd[0] = (board_ch << 6) | self.TRIMMINGIF_CMD_WRITE_REG
            cmd[1] = page
            for i in range(count):
                if self.ADDR_LOWER_LIMIT <= data[i].addr <= self.ADDR_UPPER_LIMIT:
                    cmd[ addr_index_base + (i * 3)] = data[i].addr
                    cmd[ data_index_base1 + (i * 3)] = data[i].data & 0x00FF
                    cmd[ data_index_base2 + (i * 3)] = (data[i].data & 0xFF00) >> 8

            result = self.do_command(board, cmd)
            if result == ResultKind.ok:
                self.board[board.value].sensor[board_ch].set_registers(page, data)

        return result

    def read_reg_page(self, ch: int, page: int) -> Tuple[ResultKind, list[RegData]]:
        board, board_ch = self.get_board_ch(ch)

        cmd = bytearray(2)
        if page > self.PAGE_UPPER_LIMIT or page < self.PAGE_LOWER_LIMIT or board_ch > self.CH_UPPER_LIMIT or board_ch < self.CH_LOWER_LIMIT:
            result = ResultKind.parameter_error
        else:
            cmd[0] = (board_ch << 6) | self.TRIMMINGIF_CMD_READ_PAGE
            cmd[1] = page
            self.reg_data.clear()
            result = self.do_command(board, cmd)

        return result, self.reg_data

    def set_rom(self, ch: int) -> ResultKind:
        board, board_ch = self.get_board_ch(ch)

        cmd = bytearray(1)
        if board_ch > self.CH_UPPER_LIMIT or board_ch < self.CH_LOWER_LIMIT:
            result = ResultKind.parameter_error
        else:
            cmd[0] = (board_ch << 6) | self.TRIMMINGIF_CMD_SET_ROM
            result = self.do_command(board, cmd)

        return result

    def get_status(self, ch: int) -> Tuple[ResultKind, StrealData]:
        board, board_ch = self.get_board_ch(ch)
        streal_data = StrealData()
        is_enable = False
        cmd = bytearray(1)
        if board_ch > self.CH_UPPER_LIMIT or board_ch < self.CH_LOWER_LIMIT:
            result = ResultKind.parameter_error
        else:
            cmd[0] = (board_ch << 6) | self.TRIMMINGIF_CMD_GET_STATUS
            result = self.do_command(board, cmd)
            if result == ResultKind.ok:
                streal_data.status = self.board[board.value].sensor[board_ch].status
                streal_data.temp = self.board[board.value].sensor[board_ch].last_temp
                streal_data.strain = self.board[board.value].sensor[board_ch].last_strain
                is_enable = self.board[board.value].sensor[board_ch].is_enable

            self.board[board.value].sensor[board_ch].set_sensor_status(
                streal_data.status,
                streal_data.temp,
                streal_data.strain,
                is_enable)

        return result, streal_data

    def read_reg(self, ch: int, page: int, addr: list[int]) -> Tuple[ResultKind, list[RegData]]:
        board, board_ch = self.get_board_ch(ch)
        count = len(addr)
        size = 2 + count
        cmd = bytearray(size)

        if count == 0 or page > self.PAGE_UPPER_LIMIT or page < self.PAGE_LOWER_LIMIT or board_ch > self.CH_UPPER_LIMIT or board_ch < self.CH_LOWER_LIMIT:
            result = ResultKind.parameter_error
        else:
            cmd[0] = (board_ch << 6) | self.TRIMMINGIF_CMD_READ_REG
            cmd[1] = page
            for i in range(count):
                if self.ADDR_LOWER_LIMIT <= addr[i] <= self.ADDR_UPPER_LIMIT:
                    cmd[i+2] = addr[i]

            self.reg_data.clear()
            result = self.do_command(board, cmd)

        return result, self.reg_data

    def offset_calibration(self, ch: int, ex_temp: float, ex_temp_enable: bool) -> ResultKind:
        """
        0点オフセットキャリブレーション
        """
        board, board_ch = self.get_board_ch(ch)
        if not self.board[board.value].sensor[board_ch].is_enable:
            return ResultKind.ok

        # 書き込み対象レジスタを一度リセットする
        write_data: list[RegData] = [RegData(addr=RegAddrKindSR300.DOFS.value, data=0)]  # 内蔵オフセット
        result = self.write_reg(ch, RegPageKind.sensor_reg_page0.value, write_data)
        if result != ResultKind.ok:
            return result
        # セトリング待ち(1ms)待機
        time.sleep(0.001)
        # 指定チャネルの GetStatus を実行
        result, status = self.get_status(ch)
        if result != ResultKind.ok:
            return result

        # 内蔵オフセット 書き込み
        d = Decimal(str(status.strain)) * (-1)
        val = int(d.quantize(Decimal("1E1"), rounding=ROUND_HALF_UP))
        val //= 10
        write_data: list[RegData] = [RegData(addr=RegAddrKindSR300.DOFS.value, data=val)]  # 内蔵オフセット
        result = self.write_reg(ch, RegPageKind.sensor_reg_page0.value, write_data)
        if result != ResultKind.ok:
            return result

        result = self.set_rom(ch)
        if result != ResultKind.ok:
            return result

        return result

    def temp_calibration(self, ch: int, ex_temp: float, ex_temp_enable: bool) -> ResultKind:
        return ResultKind.ok

    def set_time(self) -> ResultKind:
        """
        時刻設定
        戻り値: 結果 ("OK" など)
        """
        import datetime

        result = [ResultKind.ok, ResultKind.ok]
        for i in range(BoardKind.board_num.value):
            if self.board[i].is_connected:
                now = datetime.datetime.now()
                cmd = bytearray(11)
                cmd[0] = self.TRIMMINGIF_CMD_SYSTEM_CTRL
                cmd[1] = self.SUB_CMD_SET_TIME
                cmd[2] = 9
                cmd[3] = ((now.year // 10 % 10) << 4) | (now.year % 10)
                cmd[4] = ((now.month // 10) << 4) | (now.month % 10)
                cmd[5] = ((now.day // 10) << 4) | (now.day % 10)
                cmd[6] = ((now.hour // 10) << 4) | (now.hour % 10)
                cmd[7] = ((now.minute // 10) << 4) | (now.minute % 10)
                cmd[8] = ((now.second // 10) << 4) | (now.second % 10)
                cmd[9] = now.microsecond // 1000 & 0xFF
                cmd[10] = (now.microsecond // 1000) >> 8

                result[i] = self.do_command(self.board[i].board_no, cmd)

        if result[0] != ResultKind.ok:
            return result[0]
        if result[1] != ResultKind.ok:
            return result[1]
        return ResultKind.ok

    def set_transfer_mode(self, buf_setting: int) -> ResultKind:
        """
        転送モード設定
        buf_setting: バッファON/OFF設定
        戻り値: 結果 ("OK" など)
        """
        if not 0 <= buf_setting <= 0xFF:
            return ResultKind.parameter_error

        cmd = bytearray(4)
        cmd[0] = self.TRIMMINGIF_CMD_SYSTEM_CTRL
        cmd[1] = self.SUB_CMD_SET_TRANSFER_MODE
        cmd[2] = 0x01
        cmd[3] = buf_setting

        return self.do_command(BoardKind.board_num, cmd)

    def get_sensor_type(self, board: BoardKind) -> Tuple[ResultKind, int, int]:
        """
        指定ボードのセンサー種別を取得する。
        """
        if board == BoardKind.board_num:
            return ResultKind.parameter_error, self.SENSOR_TYPE_INVALID, self.SENSOR_TYPE_INVALID

        cmd = bytearray(4)
        cmd[0] = self.TRIMMINGIF_CMD_SYSTEM_CTRL
        cmd[1] = self.SUB_CMD_GET_SENSOR_TYPE
        cmd[2] = 0x00

        result = self.do_command(board, cmd)
        if result != ResultKind.ok:
            return result, self.SENSOR_TYPE_INVALID, self.SENSOR_TYPE_INVALID

        return (
            ResultKind.ok,
            self.sensor_type_ch1[board.value],
            self.sensor_type_ch2[board.value],
        )

    def get_network_address(self, board: BoardKind, network_type: int) -> Tuple[ResultKind, bytearray]:
        """
        指定ボードのネットワークアドレスを取得する。
        """
        if board == BoardKind.board_num:
            return ResultKind.parameter_error, bytearray()

        address_size = self.get_network_address_size(network_type)
        if address_size == 0:
            return ResultKind.parameter_error, bytearray()

        cmd = bytearray(5)
        cmd[0] = self.TRIMMINGIF_CMD_SYSTEM_CTRL
        cmd[1] = self.SUB_CMD_SET_NETWORK_ADDR
        cmd[2] = 0x02
        cmd[3] = network_type
        cmd[4] = self.NETWORK_ADDR_READ

        result = self.do_command(board, cmd)
        if result != ResultKind.ok:
            return result, bytearray()

        if (
            self.network_address_type[board.value] != network_type
            or len(self.network_address[board.value]) != address_size
        ):
            return ResultKind.response_error, bytearray()

        return ResultKind.ok, bytearray(self.network_address[board.value])

    def set_network_address(
        self,
        board: BoardKind,
        network_type: int,
        address: bytes | bytearray | list[int],
    ) -> Tuple[ResultKind, bytearray]:
        """
        指定ボードのネットワークアドレスを設定する。
        """
        if board == BoardKind.board_num:
            return ResultKind.parameter_error, bytearray()

        address_size = self.get_network_address_size(network_type)
        try:
            request_address = bytearray(address)
        except TypeError:
            return ResultKind.parameter_error, bytearray()

        if address_size == 0 or len(request_address) != address_size:
            return ResultKind.parameter_error, bytearray()

        cmd = bytearray(5 + address_size)
        cmd[0] = self.TRIMMINGIF_CMD_SYSTEM_CTRL
        cmd[1] = self.SUB_CMD_SET_NETWORK_ADDR
        cmd[2] = 0x02 + address_size
        cmd[3] = network_type
        cmd[4] = self.NETWORK_ADDR_WRITE
        cmd[5:] = request_address

        result = self.do_command(board, cmd)
        if result != ResultKind.ok:
            return result, bytearray()

        if (
            self.network_address_type[board.value] != network_type
            or len(self.network_address[board.value]) != address_size
        ):
            return ResultKind.response_error, bytearray()

        return ResultKind.ok, bytearray(self.network_address[board.value])

    def get_sampling_count(self) -> Tuple[ResultKind, int]:
        """
        サンプリング件数の取得
        """
        self._sampling_count = 0
        self.sampling_count = 0

        cmd = bytearray(3)
        cmd[0] = self.TRIMMINGIF_CMD_GET_SAMPLING
        cmd[1] = self.SUB_CMD_GET_SAMPLING_COUNT
        cmd[2] = 0x00

        result = self.do_command(BoardKind.board_num, cmd)
        if result != ResultKind.ok:
            return result, 0

        return ResultKind.ok, self._sampling_count

    def get_sampling_data(self) -> Tuple[ResultKind, int]:
        """
        サンプリングデータ取得要求
        """
        self._sampling_count = 0
        self.sampling_count = 0

        cmd = bytearray(3)
        cmd[0] = self.TRIMMINGIF_CMD_GET_SAMPLING
        cmd[1] = self.SUB_CMD_GET_SAMPLING_DATA
        cmd[2] = 0x00

        result = self.do_command(BoardKind.board_num, cmd)
        if result != ResultKind.ok:
            return result, 0

        return ResultKind.ok, self._sampling_count

    def do_command(self, board: BoardKind, cmd: bytearray) -> ResultKind:
        """
        LAN用: コマンド送信 → 応答待ち。
        各ボードごとに threading.Event を使って応答を待機。
        """
        with self._lock:
            result = []
            # 複数ボードの場合
            if BoardKind.board_num.value <= board.value:
                for i in range(BoardKind.board_num.value):
                    if self.board[i].is_connected:
                        self._resp_ret[i] = False
                        # イベント初期化
                        if not hasattr(self, "_recv_event"):
                            self._recv_event[i] = threading.Event()
                        else:
                            self._recv_event[i].clear()
                        ret = self.send_command(self.board[i].board_no, cmd)
                        if not ret:
                            return ResultKind.response_error

                # 応答待ち
                for i in range(BoardKind.board_num.value):
                    if self.board[i].is_connected:
                        result.append(self.wait_response(self.board[i].board_no))
                    else:
                        result.append(ResultKind.ok)

            else:
                # 単一ボードの場合
                self._resp_ret[board.value] = False
                if not hasattr(self, "_recv_event"):
                    self._recv_event[board.value] = threading.Event()
                else:
                    self._recv_event[board.value].clear()

                # LAN送信
                ret = self.send_command(board, cmd)
                if ret:
                    result.append(self.wait_response(board))
                else:
                    return ResultKind.response_error

            return ResultKind.ok if all(res == ResultKind.ok for res in result) else ResultKind.timeout

    def send_command(self, board: BoardKind, cmd: bytearray) -> bool:
        """
        LAN用: コマンド送信。送信前に現在コマンドを保持。
        """
        if self._tcp_serial[board.value] is None :
            return False
        with self._lock_cmd[board.value]:
            self._current_cmd[board.value] = cmd[0]  # 先頭バイトを保持（比較用）

        # LAN送信（TcpSerial.sendを利用）
        return self._tcp_serial[board.value].send(cmd, len(cmd))

    def wait_response(self, board: BoardKind) -> ResultKind:
        """
        LAN用: Eventで待機（秒単位）。結果は _resp_ret の値で判定。
        """
        ok = self._recv_event[board.value].wait(self._timeout)
        if not ok:
            return ResultKind.timeout
        return ResultKind.ok if self._resp_ret[board.value] else ResultKind.response_error

    def data_received_callback1(self, data: list):
        """
        シリアルデータ受信コールバック
        data: 受信データ（リスト of int）
        """
        #print("CB DataReceived1 -> CmdAnalyze", flush=True)
        self.cmd_analyze(BoardKind.board1, data)

    def data_received_callback2(self, data: list):
        """
        シリアルデータ受信コールバック
        data: 受信データ（リスト of int）
        """
        #print("CB DataReceived2 -> CmdAnalyze", flush=True)
        self.cmd_analyze(BoardKind.board2, data)

    def cmd_analyze(self, board:BoardKind, data: list) -> bool:
        """
        受信データをコマンドごとに解析・分岐
        """
        ret = False

        if len(data) < 2:
            return False

        ch = data[0] & self.TRIMMINGIF_CMD_CH_MASK
        current_report_id = (data[1] & self.TRIIMINGIF_REPORT_ID_MASK) >> 1

        # 初回は記録のみ
        if not self.first_report_id_set[board.value]:
            expect_report_id = self.pre_report_id[board.value] + 1
            if expect_report_id >= self.TRIIMINGIF_REPORT_ID_OVERFLOW:
                expect_report_id = self.TRIIMINGIF_REPORT_ID_MIN
            #if expect_report_id != current_report_id:
                # ☆後で対応する self.NotifyPacketLost()
        else:
            self.first_report_id_set[board.value] = False

        self.pre_report_id[board.value] = current_report_id

        cmd = data[0] & self.TRIMMINGIF_CMD_MASK

        if cmd == self.TRIMMINGIF_CMD_GET_VER:
            ret = self.get_version_response(board, data)
        elif cmd == self.TRIMMINGIF_CMD_START_MEASURE:
            ret = self.start_measure_response(board, data)
        elif cmd == self.TRIMMINGIF_CMD_STOP_MEASURE:
            ret = self.stop_measure_response(board, data)
        elif cmd == self.TRIMMINGIF_CMD_WRITE_REG:
            ret = self.write_reg_response(board, data)
        elif cmd == self.TRIMMINGIF_CMD_READ_PAGE:
            ret = self.read_reg_page_response(board, data)
        elif cmd == self.TRIMMINGIF_CMD_SET_ROM:
            ret = self.set_rom_response(board, data)
        elif cmd == self.TRIMMINGIF_CMD_GET_STATUS:
            ret = self.get_status_response(board, data)
        elif cmd == self.TRIMMINGIF_CMD_READ_REG:
            ret = self.read_reg_response(board, data)
        elif cmd == self.TRIMMINGIF_CMD_MEASURE_NOTIFY:
            ret = self.measure_notify_response(board, data)
        elif cmd == self.TRIMMINGIF_CMD_SYSTEM_CTRL:
            ret = self.system_ctrl_response(board, data)
        elif cmd == self.TRIMMINGIF_CMD_GET_SAMPLING:
            ret = self.get_sampling_data_response(board, data)
        else:
            pass  # 未対応コマンド

        #print("SetResponse cmd=", hex(data[0] & self.TRIMMINGIF_CMD_MASK), "\n", flush=True)
        self.set_response(board, data[0] & self.TRIMMINGIF_CMD_MASK, ret)
        return ret

    def set_response(self, board:BoardKind, cmd: int, resp_ret: bool):
        """
        受信コマンドと送信コマンドを TRIMMINGIF_CMD_MASK でマスクして照合。
        一致したら結果を積み、WaitResponse を解除。
        """
        mask = self.TRIMMINGIF_CMD_MASK
        with self._lock_cmd[board.value]:
            if (self._current_cmd[board.value] & mask) == (cmd & mask):
                self._resp_ret[board.value] = resp_ret
                # 解除
                if hasattr(self, "_recv_event"):
                    self._recv_event[board.value].set()

    def get_version_response(self, board:BoardKind, data: list) -> bool:
        """
        バージョン取得コマンドの応答処理
        """
        ret = False
        ack = data[1] & self.TRIMMINGIF_ACK_MASK
        if len(data) == 6 and ack == self.TRIMMINGIF_ACK_OK:
            version = data[5] << 24 | data[4] << 16 | data[3] << 8 | data[2]
            self.board[board.value].version = version
            ret = True
        return ret

    def start_measure_response(self, board:BoardKind, data: list) -> bool:
        """
        計測開始コマンドの応答処理
        """
        ret = False
        ack = data[1] & self.TRIMMINGIF_ACK_MASK
        if len(data) == 2 and ack == self.TRIMMINGIF_ACK_OK:
            ret = True
        return ret

    def stop_measure_response(self, board:BoardKind, data: list) -> bool:
        """
        計測停止コマンドの応答処理
        """
        ret = False
        ack = data[1] & self.TRIMMINGIF_ACK_MASK
        if len(data) == 2 and ack == self.TRIMMINGIF_ACK_OK:
            ret = True
        return ret

    def write_reg_response(self, board:BoardKind, data: list) -> bool:
        """
        レジスタ書込みコマンドの応答処理
        """
        ret = False
        ack = data[1] & self.TRIMMINGIF_ACK_MASK
        if len(data) == 2 and ack == self.TRIMMINGIF_ACK_OK:
            ret = True
        return ret

    def read_reg_page_response(self, board:BoardKind, data: list) -> bool:
        """
        レジスタPage読出しコマンドの応答処理
        """
        ret = False
        ack = data[1] & self.TRIMMINGIF_ACK_MASK
        if (len(data)-3) % self.REG_DATA_SIZE == 0 and ack == self.TRIMMINGIF_ACK_OK:
            ch = (data[0] & self.TRIMMINGIF_CMD_CH_MASK) >> 6
            page = data[2]
            num = (len(data) - 3) // self.REG_DATA_SIZE
            index = 3
            reg_data:list[RegData] = []
            for i in range(num):
                reg_data.append(RegData(addr=data[index], data=data[index + 1] + (data[index + 2] << 8)))
                index += 3
            self.reg_data.extend(reg_data)
            self.board[board.value].sensor[ch].set_registers(page, reg_data)
            ret = True
        return ret

    def set_rom_response(self, board:BoardKind, data: list) -> bool:
        """
        ROM設定コマンドの応答処理
        """
        ret = False
        ack = data[1] & self.TRIMMINGIF_ACK_MASK
        if len(data) == 2 and ack == self.TRIMMINGIF_ACK_OK:
            ret = True
        return ret

    def get_status_response(self, board:BoardKind, data: list) -> bool:
        """
        状態取得コマンドの応答処理
        """
        ret = False
        ack = data[1] & self.TRIMMINGIF_ACK_MASK
        if len(data) == 8:
            ch = (data[0] & self.TRIMMINGIF_CMD_CH_MASK) >> 6
            if ack == self.TRIMMINGIF_ACK_OK:
                status = data[2] + (data[3] << 8)
                temp = (data[4] + (data[5] << 8))
                strain = data[6] + (data[7] << 8)
                temp = temp - (0 if temp <= 32767 else 65536)
                temp /= 256
                strain = strain - (0 if strain <= 32767 else 65536)
                enable = False if (temp == 0x0000 and strain == 0x0000) else True
                self.board[board.value].sensor[ch].set_sensor_status(status, temp, strain, enable)
                ret = True

        return ret

    def read_reg_response(self, board:BoardKind, data: list) -> bool:
        """
        レジスタ読出しコマンドの応答処理
        """
        ret = False
        ack = data[1] & self.TRIMMINGIF_ACK_MASK
        if (len(data)-3) % self.REG_DATA_SIZE == 0 and ack == self.TRIMMINGIF_ACK_OK:
            ch = (data[0] & self.TRIMMINGIF_CMD_CH_MASK) >> 6
            page = data[2]
            num = (len(data) - 3) // self.REG_DATA_SIZE
            index = 3
            for i in range(num):
                self.reg_data.append(RegData(addr=data[index], data=data[index + 1] + (data[index + 2] << 8)))
                index += 3
            self.board[board.value].sensor[ch].set_registers(page, self.reg_data)
            ret = True
        return ret

    def measure_notify_response(self, board:BoardKind, data: list) -> bool:
        """
        計測結果通知
        """
        ret = False
        ack = data[1] & self.TRIMMINGIF_ACK_MASK
        #print(f"measure_notify_response")
        if (len(data) - 2) % self.measure_data_size == 0 and ack == self.TRIMMINGIF_ACK_OK:
            num = ((len(data) - 2) // self.measure_data_size)
            index = 2
            notify_data_list:list[MeasureData] = []
            for i in range(num):
                measure_data = MeasureData()
                if self.is_timestamp:
                    measure_data.seconds = data[index] + (data[index+1] << 8) + (data[index+2] << 16) + (data[index+3] << 24)
                    index += 4
                    measure_data.nanoseconds = data[index] + (data[index + 1] << 8) + (data[index + 2] << 16) + (data[index + 3] << 24)
                    index += 4
                for j in range(self.sensor_ch_max):
                    streal_data = StrealData()
                    status = data[index] + (data[index+1] << 8)
                    streal_data.status = status
                    temp = data[index + 2] + (data[index + 3] << 8)
                    streal_data.temp = temp - (0 if temp <= 32767 else 65536)
                    streal_data.temp /= 256
                    strain = data[index + 4] + (data[index + 5] << 8)
                    streal_data.strain = strain - (0 if strain <= 32767 else 65536)
                    is_enable = False if status == 0 else True
                    self.board[board.value].sensor[j].set_sensor_status(status, streal_data.temp, streal_data.strain, is_enable)
                    measure_data.sensor_data.append(streal_data)
                    measure_data.strain_value.append(self.board[board.value].sensor[j].last_strain_value)
                    index += 6
                if self.is_ext_data:
                    index += 2
                index += + self.alignment_area_size
                notify_data_list.append(measure_data)
            self._fire_notify_measure(board, notify_data_list)

            ret = True
        return ret

    def system_ctrl_response(self, board:BoardKind, data: list) -> bool:
        """
        システムコントロールコマンドの応答処理
        """
        ret = False
        ack = data[1] & self.TRIMMINGIF_ACK_MASK
        if len(data) >= 3 and ack == self.TRIMMINGIF_ACK_OK:
            sub_cmd = data[2]
            if sub_cmd == self.SUB_CMD_SET_TRANSFER_MODE or sub_cmd == self.SUB_CMD_SET_TIME:
                ret = True
            elif sub_cmd == self.SUB_CMD_GET_SENSOR_TYPE:
                if len(data) >= 6 and data[3] == 0x02:
                    self.sensor_type_ch1[board.value] = data[4]
                    self.sensor_type_ch2[board.value] = data[5]
                    ret = True
            elif sub_cmd == self.SUB_CMD_SET_NETWORK_ADDR:
                if len(data) >= 5:
                    address_size = self.get_network_address_size(data[4])
                    if address_size > 0 and data[3] == address_size + 1 and len(data) >= 4 + data[3]:
                        self.network_address_type[board.value] = data[4]
                        self.network_address[board.value] = bytearray(data[5:5 + address_size])
                        ret = True
        return ret

    def get_sampling_data_response(self, board:BoardKind, data: list) -> bool:
        """
        計測データ取得コマンドの応答処理
        """
        ret = False
        ack = data[1] & self.TRIMMINGIF_ACK_MASK
        self._sampling_count = 0
        self.sampling_count = 0
        if len(data) >= 6 and ack == self.TRIMMINGIF_ACK_OK and data[3] == 0x02:
            sub_cmd = data[2]
            if sub_cmd == self.SUB_CMD_GET_SAMPLING_COUNT or sub_cmd == self.SUB_CMD_GET_SAMPLING_DATA:
                self._sampling_count = (data[4] << 8) + data[5]
                self.sampling_count = self._sampling_count
                ret = True
        return ret

class TcpSerial(SerialCommon):

    def __init__(self):
        super().__init__()
        self._is_connected = False
        self._rx_thread = None
        self._decode_thread = None
        self._callback = None  # デコード後のコールバック
        self._queue = []
        self._lock = threading.Lock()
        self.init_state()
        self.data_received_handler = None  # コールバック格納用

        self._framed_packets = []  # 完成フレームの一時リスト
        self._data_received_handler = self._on_frame  # C#のevent相当
        self.my_socket: Optional[socket.socket] = None
        self.connecting_flg = False
        self.cancel_event = threading.Event()

    def is_connected(self) -> bool:
        return self._is_connected

    def connect(self, ip_addr: str, port: int) -> bool:
        self.cancel_event.clear()
        self.connecting_flg = False

        for _ in range(1):
            try:
                self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.my_socket.settimeout(3)
                self.my_socket.connect((ip_addr, port))
                self._is_connected = True
                self.connecting_flg = True

                self._rx_thread = threading.Thread(target=self._receive_loop, daemon=True)
                self._rx_thread.start()
                self._decode_thread = threading.Thread(target=self.queue_decode, daemon=True)
                self._decode_thread.start()

                self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65535)
                self.connecting_flg = False
                self.init_state()
                return True
            except Exception as e:
                print(f"Connect error: {e}")
                try:
                    if self.my_socket:
                        self.my_socket.close()
                except Exception:
                    pass
                self.my_socket = None
                self._is_connected = False
                self.connecting_flg = False
                time.sleep(0.2)

        return False
    # TcpSerial クラスに追加/修正

    def close(self):
        # 1) まずループ停止を指示
        self.cancel_event.set()
        self._is_connected = False

        # 2) recv() ブロック解除のためソケットを shutdown → close
        sock = self.my_socket
        self.my_socket = None
        if sock:
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            try:
                sock.close()
            except Exception:
                pass

        # 3) スレッド終了を待つ（短時間 join）
        if self._rx_thread and self._rx_thread.is_alive():
            self._rx_thread.join(timeout=1.0)
        if self._decode_thread and self._decode_thread.is_alive():
            self._decode_thread.join(timeout=1.0)

        self._rx_thread = None
        self._decode_thread = None

    def _receive_loop(self):
        """LAN用受信ループ: ソケットからデータを読み取り、キューに追加"""
        while not self.cancel_event.is_set():
            if self.my_socket:
                try:
                    # 非ブロッキングにするためにタイムアウト設定済み
                    data = self.my_socket.recv(65535)  # 最大1024バイト受信
                    if data:
                        #print(f"RX(raw): {data.hex()}", flush=True)
                        #with self._lock:
                            self._queue.extend(data)  # バイト列をキューに追加
                    else:
                        # 接続が切れた場合
                        break
                except socket.timeout:
                    # データがない場合は少し待機
                    continue
                except Exception as e:
                    print(f"Receive error: {e}")
                    break
            else:
                threading.Event().wait(0.01)

    def set_data_received_callback(self, callback):
        """
        デコード済みデータを渡すコールバックを登録
        callback(data: list[int])
        """
        self.data_received_handler = callback

    def queue_decode(self):
        """LAN用デコードループ: _queueからデータを取り出し、SR500プロトコルでデコード"""
        while not self.cancel_event.is_set():
            chunk = b''
            # 受信キューからデータをまとめて取り出す
            with self._lock:
                if self._queue:
                    chunk = bytes(self._queue)
                    self._queue.clear()

            if chunk:
                # SR500プロトコルでデコード（SerialCommonのdecode_sr500を利用）
                self.decode_sr500(chunk)

            # 完成したフレームを取り出してコールバックに渡す
            packets = []
            with self._lock:
                if self._framed_packets:
                    packets, self._framed_packets = self._framed_packets, []

            for packet in packets:
                if self._callback:
                    self._callback(packet)

            threading.Event().wait(0.01)

    def send(self, buffer: bytes, count: int | None = None) -> bool:
        """
        SR500フレームへエンコードしてTCPソケットで送信。
        """
        if self.my_socket is None or not self.is_connected():
            return False

        payload = buffer if count is None else buffer[:count]
        enc: list[int] = []
        self.encode_sr500(enc, payload)  # SR500プロトコルでエンコード

        try:
            # print(f"TX(enc): {bytes(enc).hex()}", flush=True)
            self.my_socket.sendall(bytes(enc))  # ソケットに送信
            return True
        except Exception as e:
            print(f"Send error: {e}")
            return False

    def _on_frame(self, frame_list):
        # frame_list は int のリスト（C#の list<byte> 相当）
        with self._lock:
            self._framed_packets.append(bytes(frame_list))

