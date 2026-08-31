import os
import time
from typing import Tuple

from Models.Hizmil_Driver import (
    HizmilDriver, ResultKind, ModeKind,
    RegData, AccData, SerialCommon, ConnectionStatus, StrealData, MeasureData
)

from Models.Board import Board, BoardKind
from Models.Sensor import SensorChKind, RegPageKind, SensorConnectionStatusKind, SensorTypeKind
from Models.SensorSR500 import RegAddrKind

class HizmilDriverUSB(HizmilDriver):
    TIMEOUT = 10

    CMD_GET_VER     = 0x00
    CMD_START_MEASURE = 0x01
    CMD_STOP_MEASURE  = 0x02
    CMD_WRITE_REG     = 0x03
    CMD_READ_PAGE     = 0x04
    CMD_SET_ROM       = 0x07
    CMD_GET_STATUS    = 0x08
    CMD_READ_REG      = 0x0A
    CMD_SYSTEM_CTRL   = 0x21
    SUB_SET_TIME      = 0x02
    SUB_SET_TRANSFER  = 0x01
    CMD_GET_SAMPLING  = 0x22
    SUB_GET_COUNT     = 0x01
    SUB_GET_DATA      = 0x02

    PAGE_LIMIT = (0,2)
    CH_LIMIT   = (0,3)
    ADDR_LIMIT = (0,0x1F)

    def __init__(self):
        super().__init__()
        self._ser = None
        self._lock = threading.Lock()
        self._recv_event = threading.Event()
        self._resp_ok = True
        self.version = bytearray(4)
        self._sampling_count = 0
        self.offset_strain = [0]*(self.ch_max)
        self.offset_temp:list[float] = [0]*(self.ch_max)

        # serial receive thread
        self._rx_thread = None
        self._running = False

        self._driver = HizmilDriver
        self._usb_serial = [UsbSerial(), UsbSerial()] # UsbSerialのPython版インスタンス
        self._lock_cmd = [threading.Lock(), threading.Lock()]
        self._current_cmd = [0, 0]
        self._recv_event = [threading.Event(), threading.Event()]
        self._resp_ret = [False, False]
        self._timeout = 5.0  # 例: 5秒タイムアウト

        self._check_status_thread = None

    def connect(self, com:list[str]) -> ConnectionStatus:
        """
        USB通信接続
        com: COMポート名 (例: 'COM3')
        戻り値: 結果 ('OK' または 'ResponseError' 等)
        """
        result = ResultKind.response_error
        result_status = ConnectionStatus.other_error

        if self._is_connected:
            return result_status

        self._usb_serial[0]._data_received_handler = self.data_received_callback1
        self.board.append(Board(BoardKind.board1, self.sensor_ch_max, SensorTypeKind.sr500))
        self._usb_serial[1]._data_received_handler = self.data_received_callback2
        self.board.append(Board(BoardKind.board2, self.sensor_ch_max, SensorTypeKind.sr500))

        for i in range(BoardKind.board_num.value):
            if com[i] != "":
                ret = self._usb_serial[i].open(com[i], self.BAUDRATE)
                if ret:
                    # C#のイベント購読はPythonではコールバックセットに直す（要実装）
                    #usb.set_data_received_callback(self.data_received_callback)

                    result = self.get_board_version(self.board[i].board_no)
                    if not result == ResultKind.ok:
                        self._usb_serial[i].close()
                        break

                    if result == ResultKind.ok:
                        self.board[i].is_connected = True
                    else:
                        self._usb_serial[i].close()
                        break
                else:
                    self._usb_serial[i].close()
                    result = ResultKind.response_error
                    break

        if not result == ResultKind.ok:
            for com in self._usb_serial:
                com.close()
            return ConnectionStatus.board_not_detected
        else:
            self._is_connected = True
            if self.is_timestamp:
                result = self.set_time()

        sensor_num = 0
        for i in range(self.ch_max):
            if self.board[i // self.sensor_ch_max].is_connected:
                # センサ接続確認
                for j in range(RegPageKind.sensor_reg_page_num.value):
                    ret, _ = self.read_reg_page(i, j)
                    if ret != ResultKind.ok:
                        continue

                ret, _ = self.get_status(i)
                if ret != ResultKind.ok:
                    continue
                sensor_num += 1

        if sensor_num == 0:
            for com in self._usb_serial:
                com.close()
            return ConnectionStatus.sensor_not_detected
        else:
            self._check_status_thread = threading.Thread(target=self.check_status, daemon=True)
            self._check_status_thread.start()
            return ConnectionStatus.success

    def disconnect(self, com:list[str]):
        """
        USB（COMポート）と切断する
        com: COMポート名（未使用だが引数保持）
        戻り値: 結果（"OK" など）
        """
        result = "OK"

        self._is_connected = False

        for usb in self._usb_serial:
            if usb is not None:
                usb.close()
                usb = None

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
        write_data:list[RegData] = [RegData(addr=RegAddrKind.ANACAL.value, data=0),     # ANACAL
                                  RegData(addr=RegAddrKind.OFFSETCOEF0.value, data=0),  # OFFSETCOEEF0
                                  RegData(addr=RegAddrKind.OFFSETCOEF1.value, data=0)]  # OFFSETCOEEF1
        result = self.write_reg(ch, RegPageKind.sensor_reg_page0.value, write_data)
        if result != ResultKind.ok:
            return result
        # セトリング待ち(1ms)待機
        time.sleep(0.001)
        # 指定チャネルの GetStatus を実行
        result, status = self.get_status(ch)
        if result != ResultKind.ok:
            return result

        # ANACAL 読み出し
        read_addr:list[int] = [RegAddrKind.ANACAL.value]
        result, read_data = self.read_reg(ch, RegPageKind.sensor_reg_page0.value, read_addr)
        if result != ResultKind.ok or len(read_data) == 0:
            return result
        # 上位 8 ビットを保持しつつ、下位 8 ビット (`OCAL`) を更新
        ocal = int(status.strain * 0.001144)
        anacal = (read_data[0].data & 0xFF00) | (ocal & 0x00FF)
        # ① ANACAL の書き込み（上位 8 ビットを維持しつつ、OCAL のみ更新）
        write_data.clear()
        write_data.append(RegData(addr=RegAddrKind.ANACAL.value, data=anacal))
        result = self.write_reg(ch, RegPageKind.sensor_reg_page0.value, write_data)
        if result != ResultKind.ok:
            return result
        # セトリング待ち(1ms)待機
        time.sleep(0.001)

        # 再度指定チャネルの GetStatus を実行
        result, status = self.get_status(ch)
        if result != ResultKind.ok:
            return result
        # 使用する温度を決定
        if ex_temp_enable:
            current_temp = ex_temp
        else:
            current_temp = status.temp

        # ひずみデータを基に OFFSETCOEEF0/1 を計算
        offset_coef = int(status.strain * 0.75 *(1-0.0022 * (current_temp - 27)))
        # ② OFFSETCOEEF0 の書き込み, ③ OFFSETCOEEF1 の書き込み
        write_data.clear()
        write_data.append(RegData(addr=RegAddrKind.OFFSETCOEF0.value, data=offset_coef))
        write_data.append(RegData(addr=RegAddrKind.OFFSETCOEF1.value, data=offset_coef))
        result = self.write_reg(ch, RegPageKind.sensor_reg_page0.value, write_data)
        if result != ResultKind.ok:
            return result
        # セトリング待ち(1ms)待機
        time.sleep(0.001)

        # SetRom 実行
        result = self.set_rom(ch)
        if result != ResultKind.ok:
            return result
        # 再度指定チャネルの GetStatus を実行
        result, status = self.get_status(ch)
        if result != ResultKind.ok:
            return result
        # 保存する温度を決定
        if ex_temp_enable:
            hold_temp = ex_temp
        else:
            hold_temp = status.temp

        # 取得したひずみデータと温度データをグローバル変数に保存
        if result == ResultKind.ok:
            self.offset_strain[ch] = status.strain
            self.offset_temp[ch] = hold_temp

        return result

    def temp_calibration(self, ch: int, ex_temp: float, ex_temp_enable: bool) -> ResultKind:
        """
        温度補正キャリブレーション
        :param ch:
        :param ex_temp:
        :param ex_temp_enable:
        :return:
        """
        board, board_ch = self.get_board_ch(ch)
        if not self.board[board.value].sensor[board_ch].is_enable:
            return ResultKind.ok

        # ① OFSETTMPCOEF0 と OFSETTMPCOEF1 を 0 にリセット
        write_data:list[RegData] = [RegData(addr=RegAddrKind.OFFSETTMPCOEF0.value, data=0),     # OFSETTMPCOEF0
                                    RegData(addr=RegAddrKind.OFFSETTMPCOEF1.value, data=0)]  # OFSETTMPCOEF1
        result = self.write_reg(ch, RegPageKind.sensor_reg_page0.value, write_data)
        if result != ResultKind.ok:
            return result
        # セトリング待ち(1ms)待機
        time.sleep(0.001)

        # ②指定チャネルの GetStatus を実行
        result, status = self.get_status(ch)
        if result != ResultKind.ok:
            return result

        # ③使用する温度を決定
        if ex_temp_enable:
            current_temp = ex_temp
        else:
            current_temp = status.temp

        # ④ 0点オフセット時のデータを取得
        zero_offset_strain = self.offset_strain[ch]
        zero_offset_temp = self.offset_temp[ch]

        # ⑤ 温度補正係数の計算 ☆0除算の可能性があることを相談済。後で対応を考える。
        offset_temp_coef = (((status.strain - zero_offset_strain) * (1 - 0.00225 * (current_temp - 27)))
                            / (current_temp - zero_offset_temp) * 96.0)
        # 16bit整数に変換
        offset_temp_coef = int(offset_temp_coef)

        # ⑥ OFSETTMPCOEF0 の書き込み、⑦ OFSETTMPCOEF1 の書き込み
        write_data.clear()
        write_data.append(RegData(addr=RegAddrKind.OFFSETTMPCOEF0.value, data=offset_temp_coef))  # OFSETTMPCOEF0
        write_data.append(RegData(addr=RegAddrKind.OFFSETTMPCOEF1.value, data=offset_temp_coef))  # OFSETTMPCOEF1
        result = self.write_reg(ch, RegPageKind.sensor_reg_page0.value, write_data)
        if result != ResultKind.ok:
            return result
        # セトリング待ち(1ms)待機
        time.sleep(0.001)

        # ⑧SetRom 実行
        result = self.set_rom(ch)
        if result != ResultKind.ok:
            return result
        # ⑨再度指定チャネルの GetStatus を実行
        result, status = self.get_status(ch)
        if result != ResultKind.ok:
            return result
        # 取得したひずみデータと温度データをグローバル変数に保存
        if result == ResultKind.ok:
            self.offset_strain[ch] = status.strain
            self.offset_temp[ch] = status.temp

        return result

    def do_command(self, board:BoardKind, cmd: bytearray) -> ResultKind:
        """
        送って → 応答待ち。threading.Event を使う（秒単位）。
        """
        with self._lock:
            result = []
            if BoardKind.board_num.value <= board.value:
                for i in range(BoardKind.board_num.value):
                    if self.board[i].is_connected:
                        self._resp_ret[i] = False
                        if not hasattr(self, "_recv_event"):
                            self._recv_event[i] = threading.Event()
                        else:
                            self._recv_event[i].clear()
                        ret = self.send_command(self.board[i].board_no, cmd)
                        if not ret:
                            return ResultKind.response_error

                for i in range(BoardKind.board_num.value):
                    if self.board[i].is_connected:
                        # 待ち。本来なら全てのイベントがセットされるまで待つ処理としたいが、Pythonに複数イベントをWaitする仕組みがない
                        result.append(self.wait_response(self.board[i].board_no))
                    else:
                        result.append(ResultKind.ok)
            else:
                # 応答バッファとイベントをクリア
                self._resp_ret[board.value] = False
                # self.myTimeout は秒（例: 5.0）
                if not hasattr(self, "_recv_event"):
                    self._recv_event[board.value] = threading.Event()
                else:
                    self._recv_event[board.value].clear()

                # 送信
                ret = self.send_command(board, cmd)
                if ret:
                    # 待ち
                    result.append(self.wait_response(board))
                else:
                    return ResultKind.response_error

            return ResultKind.ok if all(res == ResultKind.ok for res in result) else ResultKind.timeout

    def send_command(self, board:BoardKind, cmd: bytearray) -> bool:
        """
        コマンド送信。送信前に現在コマンドを保持。
        """

        if self._usb_serial[board.value] is None:
            return False
        with self._lock_cmd[board.value]:
            self._current_cmd[board.value] = cmd[0]  # そのまま格納（比較時にマスクする）
        return self._usb_serial[board.value].send(cmd, len(cmd))

    def wait_response(self, board:BoardKind) -> ResultKind:
        """
        Event で待つ（秒）。結果は myRespRet のAND。
        """
        ok = self._recv_event[board.value].wait(self._timeout)  # 秒
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
                enable = False if ( status == 0xFFFF or status == 0x0000 ) else True
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

import serial
import threading
from Models.Hizmil_Driver import SerialCommon

class UsbSerial(SerialCommon):
    def __init__(self):
        super().__init__()
        self._serial_port = None
        self._rx_thread = None
        self._decode_thread = None
        self._running = False
        self._callback = None  # デコード後のコールバック
        self._queue = []
        self._lock = threading.Lock()
        self._queueLock = threading.Lock()
        self.init_state()
        self.data_received_handler = None  # コールバック格納用

        self._framed_packets = []  # 完成フレームの一時リスト
        self._data_received_handler = self._on_frame  # C#のevent相当

    def open(self, port, baudrate):
        try:
            # インスタンスの生成とOpen処理を分けて明示的にバッファを確保しなおす
            self._serial_port = serial.Serial()
            self._serial_port.port = port
            self._serial_port.baudrate = baudrate
            self._serial_port.bytesize = serial.EIGHTBITS
            self._serial_port.parity = serial.PARITY_NONE
            self._serial_port.stopbits = serial.STOPBITS_ONE
            self._serial_port.xonxoff = False
            self._serial_port.rtscts = False
            self._serial_port.dsrdtr = False
            self._serial_port.timeout = 0.1
            if os.name == 'nt':
                self._serial_port.set_buffer_size(rx_size=4096, tx_size=4096)
            self._serial_port.open()
            self._serial_port.reset_input_buffer()
            self._serial_port.reset_output_buffer()
            time.sleep(0.1)

            self._running = True
            self._rx_thread = threading.Thread(target=self._receive_loop, daemon=True)
            self._rx_thread.start()
            self._decode_thread = threading.Thread(target=self.queue_decode, daemon=True)
            self._decode_thread.start()
            return True
        except Exception as e:
            print(f"Open Error: {e}")
            self._serial_port = None
            return False

    def close(self):
        self._running = False
        if self._serial_port:
            self._serial_port.close()
            self._serial_port = None


    def send(self, buffer: bytes, count: int | None = None) -> bool:
        """
        SR500フレームへエンコードして送信。
        """
        if self._serial_port is None:
            return False

        payload = buffer if count is None else buffer[:count]
        enc: list[int] = []
        self.encode_sr500(enc, payload)  # 第1引数は出力リスト（C#と同じ）
        try:
            #print("TX(enc):", bytes(enc).hex(), flush=True)
            self._serial_port.write(bytes(enc))  # 書き込み
            # PycharmデバッガとUSB処理の衝突防止用
            time.sleep(0.01)
            return True
        except Exception:
            return False

    def set_data_received_callback(self, callback):
        """
        デコード済みデータを渡すコールバックを登録
        callback(data: list[int])
        """
        self.data_received_handler = callback

    def _receive_loop(self):
        while self._running:
            if self._serial_port.in_waiting > 0:
                with self._lock:
                    data = self._serial_port.read(self._serial_port.in_waiting)
                # コールバックにバイト列を渡す（例：list(data)で整数リスト化も可）
                if data:
                    #print("RX(raw):", data.hex(), flush=True)
                    with self._queueLock:
                        self._queue.extend(data)  # バッファに追加
            else:
                threading.Event().wait(0.01)

    def queue_decode(self):
        while self._running:
            chunk = b''
            if self._queue:
                with self._queueLock:
                    chunk = bytes(self._queue)
                    self._queue.clear()

            if chunk:
                # C#と同じ：内部状態を使ってデコード。終端で DataReceived が呼ばれる
                self.decode_sr500(chunk)

            # DataReceived で溜まった完成フレームを取り出す
            packets = []
            if self._framed_packets:
                with self._lock:
                    packets, self._framed_packets = self._framed_packets, []

            for packet in packets:
                if self._callback:
                    self._callback(packet)

            threading.Event().wait(0.01)

    def _on_frame(self, frame_list):
        # frame_list は int のリスト（C#の list<byte> 相当）
        with self._lock:
            self._framed_packets.append(bytes(frame_list))









