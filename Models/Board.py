from enum import Enum

from Models.Sensor import Sensor, SensorChKind, SensorTypeKind
from Models.SensorSR300 import SensorSR300
from Models.SensorSR500 import SensorSR500


# --------------------------
# 列挙型の定義
# --------------------------
class BoardKind(Enum):
    board1 = 0
    board2 = 1
    board_num = 2

class Board:
    def __init__(self, board:BoardKind, sensor_num, type:SensorTypeKind):
        self.is_connected = False
        self.board_no = board
        self.version = 0
        self.sensor = []
        for i in range(sensor_num):
            if type == SensorTypeKind.sr500:
                self.sensor.append(SensorSR500())
            else:
                self.sensor.append(SensorSR300())

    def get_board_no(self) -> BoardKind:
        return self.board_no

    def get_sensor_num(self) -> int:
        num = 0
        for i in range(SensorChKind.sensor_num.value):
            if self.sensor[i].isConnected:
                num += 1
        return num

    def get_sensor_ids(self) -> list[str]:
        return [sensor.get_sensor_id() if sensor.is_enable else "-" for sensor in self.sensor]

