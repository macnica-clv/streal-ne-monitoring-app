import os, dataclasses, datetime, threading, re

from typing import List, IO, Deque


class Log:
    def __init__(self, max_row: int, name:str = "", prefix:str = "", use_count: bool = True):
        self._log_queue = Deque()
        self._log_file = None
        self._dst_dir = ""
        self._log_count = 0
        self._is_saving = False

        self._name = name
        self._prefix = re.sub(r'[\\/:*?"<>|]+', '', prefix)
        self._use_count = use_count
        self._max_row = max_row
        self._header = ""

    def make_dst_dir(self, dst:str = None, dir_name:str = "") -> str:
        """
        ログの保存先を作成する
        :param dst: ディレクトリの作成先
        :param dir_name: ディレクトリ名（既存のディレクトリ名でも良い）
        :return: 実際に作成されたディレクトリのパス
        """
        if dir_name == "":
            dir_name = self._prefix + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        if (dst is not None) and os.path.isdir(dst):
            path = os.path.join(dst, dir_name)
        else:
            path = dir_name
        os.makedirs(path, exist_ok=True)

        self._dst_dir = path
        return path

    def set_dst_dir(self, dst: str):
        self._dst_dir = dst

    def open_log(self) -> None:
        self._log_count += 1
        name = self._name if self._name != "" else datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{self._prefix}{name}"
        filename += f"_{self._log_count:04}.csv" if self._use_count else ".csv"

        if os.path.isdir(self._dst_dir):
            self._log_file = open(os.path.join(self._dst_dir, filename), "w")
        else:
            self._log_file = open(filename, "w")
        self._log_file.write(self._header)

    def set_name(self, name:str):
        self._name = name

    def set_max_row(self, max_row:int):
        self._max_row = max_row

    def set_header(self, header:str):
        self._header = header

    def start(self) -> None:
        self._log_queue.clear()
        self._log_count = 0
        self.open_log()
        self._is_saving = True

    def stop(self) -> None:
        self._is_saving = False
        # 保存終了を待つ
        save_and_close(self._log_file, list(self._log_queue))

    def save(self, log):
        if self._is_saving:
            if self._log_file is None:
                self.open_log()

            self._log_queue.append(log)

            # 上限に達したら保存処理を別スレッドで行う
            if len(self._log_queue) >= self._max_row:
                save_thread = threading.Thread(target=save_and_close, args=(self._log_file, list(self._log_queue)))
                save_thread.start()
                self._log_file = None
                self._log_queue.clear()

def save_and_close(file:IO, logs:List[str]):
    try:
        if file:
            file.writelines(logs)
            file.close()
    except Exception as e:
        print(f"File save error: {e}")

@dataclasses.dataclass
class SingleSensorData:
    is_valid: bool
    status: int
    temp: float
    strain: int
    strain_value: float

@dataclasses.dataclass
class SingleMeasData:
    second: int
    nanosecond: int
    sensor_data: list[SingleSensorData]

class MeasureLog(Log):
    def __init__(self, name:str = "", prefix:str = "", header_row:int = 0, max_row:int = 30000):
        super().__init__(name=name, prefix=prefix, max_row=max_row)
        self.header_row = header_row
        self.time_fmt = "%Y/%m/%d %H:%M:%S"

    def set_header_row(self, row: int):
        self.header_row = row

    def time_to_str(self, second:int, nanosecond:int) -> str:
        if not second == 0:
            dt = datetime.datetime.fromtimestamp(second)
            return f"{dt.strftime(self.time_fmt)}.{nanosecond:09}"
        else:
            return "-"

    def str_to_time(self, time_str:str) -> tuple[int, int]:
        if time_str == "-":
            return 0, 0
        else:
            sec_str, nano_sec_str = time_str.split(".", 1)
            try:
                dt = datetime.datetime.strptime(sec_str, self.time_fmt)
                nano_sec = int(nano_sec_str)
            except ValueError:
                return 0, 0
            return int(dt.timestamp()), nano_sec

    def add_data(self, single_data:SingleMeasData) -> None:
        log = self.time_to_str(single_data.second, single_data.nanosecond) + ","
        for data in single_data.sensor_data:
            log += f"{data.status},{data.temp:.3f},{data.strain},{data.strain_value:.3f}," if data.is_valid else "-,-,-,-,"
        self.save(log + "\n")

    def load_log(self, filepath) -> list[SingleMeasData]:
        if not os.path.isfile(filepath):
            return []
        with open(filepath, "r") as f:
            # ヘッダ行を除外する
            lines = f.readlines()[self.header_row:]

        data_list: list[SingleMeasData] = []
        for line in lines:
            items = line.split(',')
            if len(items) < 1:
                continue
            second, nanosecond = self.str_to_time(items[0])

            # センサごとのデータを纏める
            meas_data = SingleMeasData(second, nanosecond, [])
            for i in range(1, len(items[1:]), 4):
                if (i + 3) > len(items[1:]):
                    break
                status, result1 = self.str_to_val(items[i], int)
                temp, result2 = self.str_to_val(items[i + 1], float)
                strain, result3 = self.str_to_val(items[i + 2], float)
                strain_value, result4 = self.str_to_val(items[i + 3], float)
                # 1つでも数値に変換出来たら有効なデータと見なす
                is_valid = result1 or result2 or result3 or result4
                meas_data.sensor_data.append(SingleSensorData(is_valid, status, temp, strain, strain_value))
            data_list.append(meas_data)
        return data_list

    @staticmethod
    def str_to_val(val_str, val_type):
        try:
            return val_type(val_str), True
        except ValueError:
            return 0, False

