import threading
import time
from enum import Enum
from dataclasses import dataclass, field
from threading import Lock, Event
from typing import Optional, Tuple,  Callable
import queue

from Models.Board import Board, BoardKind
from Models.Sensor import RegData, SensorChKind, SensorConnectionStatusKind, SensorStatus


# --------------------------
# 列挙型の定義
# --------------------------
class ResultKind(Enum):
    ok = 0
    parameter_error = 1
    response_error = 2
    timeout = 3

class ModeKind(Enum):
    all = 1
    no_status = 2
    strain_only = 3

class StateKind(Enum):
    search_top = 0
    search_end = 1
    escape = 2

class ConnectionStatus(Enum):
    success = 0
    sensor_not_detected = 1
    board_not_detected = 2
    other_error = 3
    mixed_sensor = 4


# --------------------------
# データ構造
# --------------------------
@dataclass
class StrealData:
    status: int = 0
    temp: float = 0
    strain: int = 0

@dataclass
class MeasureData:
    seconds: int = 0
    nanoseconds: int = 0
    sensor_data: list[StrealData] = field(default_factory=list)
    strain_value: list[float] = field(default_factory=list)

@dataclass
class AccData:
    X: int = 0
    Y: int = 0
    Z: int = 0

# --------------------------
# ベースドライバクラス
# --------------------------
class HizmilDriver:
    # コマンド定数
    TRIMMINGIF_CMD_GET_VER        = 0x00
    TRIMMINGIF_CMD_START_MEASURE  = 0x01
    TRIMMINGIF_CMD_STOP_MEASURE   = 0x02
    TRIMMINGIF_CMD_WRITE_REG      = 0x03
    TRIMMINGIF_CMD_READ_PAGE      = 0x04
    TRIMMINGIF_CMD_SET_ROM        = 0x07
    TRIMMINGIF_CMD_GET_STATUS     = 0x08
    TRIMMINGIF_CMD_READ_REG       = 0x0A
    TRIMMINGIF_CMD_MEASURE_NOTIFY = 0x0B
    TRIMMINGIF_CMD_ACC_NOTIFY     = 0x0D
    TRIMMINGIF_CMD_SYSTEM_CTRL    = 0x21
    SUB_CMD_SET_TRANSFER_MODE     = 0x01
    SUB_CMD_SET_TIME              = 0x02
    SUB_CMD_SET_NETWORK_ADDR      = 0x03
    SUB_CMD_GET_SENSOR_TYPE       = 0x04
    TRIMMINGIF_CMD_GET_SAMPLING   = 0x22
    SUB_CMD_GET_SAMPLING_COUNT    = 0x01
    SUB_CMD_GET_SAMPLING_DATA     = 0x02

    TRIMMINGIF_CMD_CH_MASK = 0xC0
    TRIMMINGIF_CMD_MASK = 0x3F
    TRIIMINGIF_REPORT_ID_MASK = 0xFE
    TRIIMINGIF_REPORT_ID_MAX = 0x7F
    TRIIMINGIF_REPORT_ID_MIN = 0x00
    TRIIMINGIF_REPORT_ID_INTERVAL = 0x01
    TRIIMINGIF_REPORT_ID_OVERFLOW = 0x80
    TRIMMINGIF_ACK_MASK = 0x01
    TRIMMINGIF_ACK_OK = 0x00
    TRIMMINGIF_ACK_NG = 0x01

    SENSOR_TYPE_INVALID = 0x00
    SENSOR_TYPE_SR300 = 0x03
    SENSOR_TYPE_SR500 = 0x05
    NETWORK_ADDR_TYPE_IP = 0x01
    NETWORK_ADDR_TYPE_SUBNET_MASK = 0x02
    NETWORK_ADDR_TYPE_GATEWAY = 0x03
    NETWORK_ADDR_TYPE_MAC = 0x04

    # 上限下限定数
    PAGE_UPPER_LIMIT = 0x02
    PAGE_LOWER_LIMIT = 0x00
    CH_UPPER_LIMIT   = 0x03
    CH_LOWER_LIMIT   = 0x00
    ADDR_UPPER_LIMIT = 0x1F
    ADDR_LOWER_LIMIT = 0x00

    # その他定数
    TIMEOUT_NORMAL = 10000
    TIGERKIN_WAITING_STABILITY = 4000
    NETWORK_ADDR_IPV4_SIZE = 4
    NETWORK_ADDR_MAC_SIZE = 6
    BAUDRATE = 921600
    NETWORK_ADDR_READ = 0x01
    NETWORK_ADDR_WRITE = 0x02

    CODE_TOP        = 0xFE
    CODE_END        = 0xFD
    CODE_ESCAPE     = 0x5C
    ESCAPE_CODE_TOP = 0x00
    ESCAPE_CODE_END = 0x01

    REG_DATA_SIZE = 3
    INTERVAL_MS = 500
    INTERVAL_SEC = INTERVAL_MS / 1000.0

    def __init__(self):
        # モデル毎の設定
        # unico
        # self.board_max = 2
        # self.sensor_ch_max = 4
        # self.ch_max = self.board_max * self.sensor_ch_max
        # self.is_timestamp = False
        # self.is_ext_data = True
        # self.alignment_area_size = 0
        # SRHX099HS
        self.board_max = 2
        self.sensor_ch_max = 2
        self.ch_max = self.board_max * self.sensor_ch_max
        self.is_timestamp = True
        self.is_ext_data = True
        self.alignment_area_size = 2

        data_size = self.sensor_ch_max * 6
        if self.is_timestamp:
            data_size += 8
        if self.is_ext_data:
            data_size += 2
        self.measure_data_size = data_size + self.alignment_area_size

        # チャンネル数とグループバイト数
        self.group_bytes = lambda: 8 + self.sensor_ch_max * 6 + 4

        # コールバックハンドラリスト
        self._notify_measure_handlers: list[Callable[[BoardKind, list[MeasureData]], None]] = []
        self._notify_acc_handlers: list[Callable[[bool, AccData], None]] = []
        self._notify_packet_lost_handlers: list[Callable[[], None]] = []

        # 校正値
        self.offset_strain: list[int] = [0] * self.ch_max
        self.offset_temp: list[int]   = [0] * self.ch_max

        # 内部状態
        self._is_connected    = False
        self.version        = []
        self.reg_data: list[RegData] = []
        self.streal_data: StrealData = StrealData()
        self._lock_cmd        = Lock()
        self._resp_ret: list[bool]    = []
        self._timeout        = self.TIMEOUT_NORMAL
        self._recv_event      = list[Event]
        self.pre_report_id    = [0, 0]
        self.first_report_id_set: list[bool] = [True, True]
        self.sampling_count  = 0
        self.sensor_type_ch1: list[int] = [self.SENSOR_TYPE_INVALID] * self.board_max
        self.sensor_type_ch2: list[int] = [self.SENSOR_TYPE_INVALID] * self.board_max
        self.network_address_type: list[int] = [0] * self.board_max
        self.network_address: list[bytearray] = [bytearray() for _ in range(self.board_max)]
        self.board = []
        self.is_measuring = False

        # 通信デコーダ状態
        self.state = StateKind.search_top
        self.decoded_data = bytearray()

        # 計測データのキュー
        self.measureData = queue.Queue(maxsize=0)

    def is_connected(self) -> bool:
        return self._is_connected

    # 抽象メソッド
    def connect(self, com: list[str]) -> ConnectionStatus:
        raise NotImplementedError()
    def get_version(self, version: list[int]) -> ResultKind:
        raise NotImplementedError()
    def set_time(self) -> ResultKind:
        raise NotImplementedError()
    def start_measure(self, interval: int, mode: ModeKind) -> ResultKind:
        raise NotImplementedError()
    def stop_measure(self) -> ResultKind:
        raise NotImplementedError()
    def write_reg(self, ch: int, page: int, data: list[RegData]) -> ResultKind:
        raise NotImplementedError()
    def read_reg_page(self, ch: int, page: int) -> Tuple[ResultKind, list[RegData]]:
        raise NotImplementedError()
    def set_rom(self, ch: int) -> ResultKind:
        raise NotImplementedError()
    def get_status(self, ch: int) -> Tuple[ResultKind, StrealData]:
        raise NotImplementedError()
    def read_reg(self, ch: int, page: int, addr: list[int]) -> Tuple[ResultKind, list[RegData]]:
        raise NotImplementedError()
    def disconnect(self, com:list[str]) -> ResultKind:
        raise NotImplementedError()
    def set_transfer_mode(self, buf_setting: int) -> ResultKind:
        """
        転送モード設定
        buf_setting: バッファON/OFF設定
        戻り値: 結果 ("OK" など)
        """
        raise NotImplementedError()
    def get_sensor_type(self, board: BoardKind) -> Tuple[ResultKind, int, int]:
        raise NotImplementedError()
    def get_network_address(self, board: BoardKind, network_type: int) -> Tuple[ResultKind, bytearray]:
        raise NotImplementedError()
    def set_network_address(
        self,
        board: BoardKind,
        network_type: int,
        address: bytes | bytearray | list[int]
    ) -> Tuple[ResultKind, bytearray]:
        raise NotImplementedError()
    def get_sampling_count(self) -> Tuple[ResultKind, int]:
        raise NotImplementedError()
    def get_sampling_data(self) -> Tuple[ResultKind, int]:
        raise NotImplementedError()
    def offset_calibration(self, ch: int, ex_temp: float, ex_temp_enable: bool) -> ResultKind:
        raise NotImplementedError()
    def temp_calibration(self, ch: int, ex_temp: float, ex_temp_enable: bool) -> ResultKind:
        raise NotImplementedError()

    # イベント登録
    def on_notify_measure(self, handler: Callable[[BoardKind, list[MeasureData]], None]) -> None:
        self._notify_measure_handlers.append(handler)
    def on_notify_acc(self, handler: Callable[[bool, AccData], None]) -> None:
        self._notify_acc_handlers.append(handler)
    def on_notify_packet_lost(self, handler: Callable[[], None]) -> None:
        self._notify_packet_lost_handlers.append(handler)

    # イベント発火
    def _fire_notify_measure(self, board: BoardKind, data: list[MeasureData]) -> None:
        for h in self._notify_measure_handlers:
            h(board, data)
    def _fire_notify_acc(self, result: bool, data: AccData) -> None:
        for h in self._notify_acc_handlers:
            h(result, data)
    def _fire_notify_packet_lost(self) -> None:
        for h in self._notify_packet_lost_handlers:
            h()

    def get_ch(self, board: BoardKind, ch: int) -> int:
        return self.sensor_ch_max * board.value + ch

    def get_board_ch(self, ch: int) -> Tuple[BoardKind, int]:
        board = ch // self.sensor_ch_max
        board_ch = ch % self.sensor_ch_max
        return BoardKind(board), board_ch

    def get_version_value(self) -> list[str]:
        version = []
        for board in self.board:
            if board.is_connected:
                components = []
                version_value = board.version
                components.append((version_value >> 24) & 0xFF)
                components.append((version_value >> 16) & 0xFF)
                components.append((version_value >> 8) & 0xFF)
                components.append(version_value & 0xFF)
                version.append(".".join(map(str, components)))
            else:
                version.append("")

        return version

    def get_network_address_size(self, network_type: int) -> int:
        if network_type in (
            self.NETWORK_ADDR_TYPE_IP,
            self.NETWORK_ADDR_TYPE_SUBNET_MASK,
            self.NETWORK_ADDR_TYPE_GATEWAY,
        ):
            return self.NETWORK_ADDR_IPV4_SIZE
        if network_type == self.NETWORK_ADDR_TYPE_MAC:
            return self.NETWORK_ADDR_MAC_SIZE
        return 0

    def init_status_all(self):
        for ch in range(self.ch_max):
            if self.is_sensor_enable(ch):
                self.init_status(ch)

    def init_status(self, ch: int):
        ret, data = self.get_status(ch)
        if ret == ResultKind.ok:
            self.set_sensor_init(ch, data.strain, data.temp)

    def set_sensor_init(self, ch: int, init_strain: int, init_temp: float):
        board, board_ch = self.get_board_ch(ch)
        self.board[board.value].sensor[board_ch].set_init(init_strain, init_temp)

    def is_sensor_enable(self, ch: int) -> bool:
        board, board_ch = self.get_board_ch(ch)
        return self.board[board.value].sensor[board_ch].is_enable

    def is_board_sensor_enable(self, board: BoardKind, ch: int) -> bool:
        return self.board[board.value].sensor[ch].is_enable

    def check_status(self):
        last_time = time.time()
        while self._is_connected:
            current_time = time.time()
            elapsed_time = current_time - last_time
            if self.INTERVAL_SEC <= elapsed_time:
                last_time = current_time
                for i in range(self.ch_max):
                    if not self.get_sensor_connection_status(i) == SensorConnectionStatusKind.no_connect:
                        ret, _ = self.get_status(i)
            threading.Event().wait(0.1)

    def get_sensor_status_all(self) -> list[SensorStatus]:
        sensor_status: list[SensorStatus] = []
        for i in range(self.ch_max):
            sensor_status.append(self.get_sensor_status(i))

        return sensor_status

    def get_sensor_status(self, ch: int) -> SensorStatus:
        # ☆センサデータ表示に使用するデータ取得用
        board, board_ch = self.get_board_ch(ch)
        return self.board[board.value].sensor[board_ch].get_sensor_status()

    def get_sensor_connection_status(self, ch: int) -> SensorConnectionStatusKind:
        # ☆ステータスバーやHome画面の接続状態取得用
        board, board_ch = self.get_board_ch(ch)
        return self.board[board.value].sensor[board_ch].connection_status

    def get_board_connection_status(self, board_no: BoardKind) -> bool:
        for board in self.board:
            if board.get_board_no() == board_no:
                return board.is_connected
        return False

    def get_sensor_ids(self) -> list[str]:
        return sum([board.get_sensor_ids() if board.is_connected else ["-"] * self.sensor_ch_max for board in self.board], [])

    def _is_sr300_connected(self) -> bool:

        found_valid = False

        for board in BoardKind:
            if not self.get_board_connection_status(board):
                continue

            b = board.value

            for sensor_type in (
                    self.sensor_type_ch1[b],
                    self.sensor_type_ch2[b],
            ):
                if sensor_type == self.SENSOR_TYPE_INVALID:
                    continue

                found_valid = True

                if sensor_type == self.SENSOR_TYPE_SR500:
                    return False

                if sensor_type != self.SENSOR_TYPE_SR300:
                    return False

        # SR300 が1個以上あり、SR500が無い場合のみ True
        return found_valid


# --------------------------
# サブドライバクラス(なんで１ファイルに２クラスあるんだよ)
# --------------------------


class SerialCommon:
    # C#の定数名をそのまま
    CODE_TOP           = 0xFE
    CODE_END           = 0xFD
    CODE_ESCAPE        = 0x5C
    ESCAPE_CODE_TOP    = 0x00
    ESCAPE_CODE_END    = 0x01
    ESCAPE_CODE_ESCAPE = 0x5C


    def __init__(self):
        self._data_received_handler: Optional[Callable[[list[int]], None]] = None
        self.myDecodedData: list[int] = []
        self.myState: StateKind = StateKind.search_top

    def init_state(self) -> None:
        self.myState = StateKind.search_top

    # C#と同名・同ロジック
    def encode_sr500(self, dest: list[int], src: bytes) -> int:
        dest.append(self.CODE_TOP)
        for b in src:
            self.encode_byte(b, dest)
        dest.append(self.CODE_END)
        return len(dest)

    # C#と同名・同ロジック
    def encode_byte(self, data: int, buf: list[int]) -> int:
        size = 2
        if   data == self.CODE_TOP:
            buf.append(self.ESCAPE_CODE_ESCAPE); buf.append(self.ESCAPE_CODE_TOP)
        elif data == self.CODE_END:
            buf.append(self.ESCAPE_CODE_ESCAPE); buf.append(self.ESCAPE_CODE_END)
        elif data == self.CODE_ESCAPE:
            buf.append(self.ESCAPE_CODE_ESCAPE); buf.append(self.ESCAPE_CODE_ESCAPE)
        else:
            buf.append(data); size = 1
        return size

    # ★ここがご指摘の箇所：C#と同じく SearchEnd 中に CODE_END を受けたら DataReceived() を呼ぶ★
    def decode_sr500(self, data: bytes) -> None:
        """
        C#版と同一ロジック。SearchEnd中にCODE_END(0xFD)を受けたら
        DataReceived(self.myDecodedData) をコールする。
        """
        for tmpData in data:
            if self.myState == StateKind.search_top:
                if tmpData == self.CODE_TOP:
                    self.myDecodedData.clear()
                    self.myState = StateKind.search_end

            elif self.myState == StateKind.search_end:
                if tmpData == self.CODE_END:
                    if self._data_received_handler:
                        # C#は list<byte> を渡す → Pythonでは int のリストで渡す
                        #print("CALL DataReceived len=", len(self.myDecodedData), flush=True)
                        self._data_received_handler(list(self.myDecodedData))
                    self.myState = StateKind.search_top
                elif tmpData == self.CODE_ESCAPE:
                    self.myState = StateKind.escape
                else:
                    self.myDecodedData.append(tmpData)

            elif self.myState == StateKind.escape:
                if tmpData == self.ESCAPE_CODE_TOP:
                    self.myDecodedData.append(self.CODE_TOP)
                elif tmpData == self.ESCAPE_CODE_END:
                    self.myDecodedData.append(self.CODE_END)
                elif tmpData == self.ESCAPE_CODE_ESCAPE:
                    self.myDecodedData.append(self.CODE_ESCAPE)
                self.myState = StateKind.search_end

            else:
                self.myDecodedData.clear()
                self.myState = StateKind.search_top

