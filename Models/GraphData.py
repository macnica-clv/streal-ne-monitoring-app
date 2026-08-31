from typing import List, Deque


class GraphData:
    def __init__(self, max_plot_num: int = 30000, max_plot_clear: bool = False):
        self._seconds : Deque[float] = Deque(maxlen=max_plot_num)
        self._nanoseconds : Deque[float] = Deque(maxlen=max_plot_num)
        self._sensors : List[SensorGraphData] = []
        self._sensor_ch_offset: int = 0
        self._max_plot_num = max_plot_num
        self._max_plot_clear = max_plot_clear

    def init_sensors(self, sensor_num: int, ch_offset: int):
        # リストを初期化して、センサ数だけ要素を用意する（測定開始時）
        self._seconds.clear()
        self._nanoseconds.clear()
        self._sensors.clear()
        for i in range(1, sensor_num + 1):
            self._sensors.append(SensorGraphData(self._max_plot_num, self._max_plot_clear))
        self._sensor_ch_offset = ch_offset

    def get_ch_offset(self):
        return self._sensor_ch_offset

    def add_time(self, second, nanosecond):
        # 左端から再描画する場合はクリアする
        if self._max_plot_clear and (len(self._seconds) > self._max_plot_num):
            self._seconds.clear()
            self._nanoseconds.clear()
        self._seconds.append(second)
        self._nanoseconds.append(nanosecond)

    def add_data(self, ch, strain: int, temp: float, status: int, strain_value: float):
        self._sensors[ch].add_data(strain, temp, status, strain_value)

    def get_sensor_num(self):
        return len(self._sensors)

    def get_seconds(self):
        return list(self._seconds)
    def get_nanoseconds(self):
        return list(self._nanoseconds)
    def get_time(self):
        return [sec + ns / (10 ** 9) for sec, ns in zip(list(self._seconds), list(self._nanoseconds))]

    def get_strains(self, ch):
        return self.get_data(ch, SensorGraphData.id_strain)
    def get_temps(self, ch):
        return self.get_data(ch, SensorGraphData.id_temp)
    def get_status(self, ch):
        return self.get_data(ch, SensorGraphData.id_status)
    def get_strain_values(self, ch):
        return self.get_data(ch, SensorGraphData.id_strain_value)

    def get_data(self, ch, idx):
        return self._sensors[ch].get_data(idx) if (ch < len(self._sensors)) else []


class SensorGraphData:
    id_strain = 0
    id_temp = 1
    id_status = 2
    id_strain_value = 3

    def __init__(self, max_plot_num: int, max_plot_clear: bool):
        self._strain: Deque[int] = Deque(maxlen=max_plot_num)
        self._temp: Deque[float] = Deque(maxlen=max_plot_num)
        self._status: Deque[int] = Deque(maxlen=max_plot_num)
        self._strain_values: Deque[float] = Deque(maxlen=max_plot_num)

        self._max_plot_num = max_plot_num
        self._max_plot_clear = max_plot_clear

    def add_data(self, strain: int, temp: float, status: int, strain_value: float):
        # 左端から再描画する場合はクリアする
        if self._max_plot_clear and (len(self._strain) > self._max_plot_num):
            self._strain.clear()
            self._temp.clear()
            self._status.clear()
            self._strain_values.clear()
        self._strain.append(strain)
        self._temp.append(temp)
        self._status.append(status)
        self._strain_values.append(strain_value)

    def get_data(self, idx: int) -> list:
        if idx == self.id_strain:
            return list(self._strain)
        if idx == self.id_temp:
            return list(self._temp)
        if idx == self.id_status:
            return list(self._status)
        if idx == self.id_strain_value:
            return list(self._strain_values)
        else:
            return []

