from dataclasses import dataclass, field
from enum import Enum

from PySide6.QtCore import QSettings

from Utils.ResourceLoader import rel_to_abs, get_config_path


class ConnectionMethodKind(Enum):
    usb = 0
    lan = 1

@dataclass
class ConfigDataHome:
    connection_method: int = 0
    com1: str = ""
    com2: str = ""
    ip_addr1: str = ""
    ip_addr2: str = ""

@dataclass
class ConfigSampling:
    sampling_rate:str = "1000"
    sampling_unit:int = 0
    buffer_mode: bool = False
    buffer_interval_ms: str = "100"
    buffer_transfer_mode: int = 2

@dataclass
class ConfigDataChartFilter:
    filter_moving_average:bool = False
    filter_moving_average_window:int = 0
    filter_fft:bool = False
    filter_fft_resolution:int = 0
    filter_fft_window:str = ""
    filter_standard_deviation:bool = False
    filter_standard_deviation_window:int = 0

@dataclass
class ConfigDataChartSensorSettings:
    sensor_strain_line_color:list[int] = field(default_factory=list)
    sensor_temp_line_color: list[int] = field(default_factory=list)
    sensor_line_width:list[int] = field(default_factory=list)
    sensor_line_offset:list[int] = field(default_factory=list)

@dataclass
class ConfigDataChartSensorDataDisplay:
    chart_unit:int = 0
    show_sensor_name:bool = True
    show_temperature:bool = True
    show_current_value:bool = True
    show_init_value:bool = True
    show_delta_value:bool = True
    show_status:bool = True
    sensor_name:list[str]= field(default_factory=str)
    strain_line_view:list[bool]= field(default_factory=list)
    temp_line_view: list[bool] = field(default_factory=list)

@dataclass
class ConfigDataChart:
    sampling:ConfigSampling
    filter:ConfigDataChartFilter
    sensor_settings:ConfigDataChartSensorSettings
    sensor_data_display:ConfigDataChartSensorDataDisplay

@dataclass
class ConfigThemeSettings:
    window_theme: int = 0

@dataclass
class ConfigShortcutSettings:
    meas_start: str = ""
    meas_stop: str = ""
    auto_range: str = ""
    save_log: str = ""
    capture: str = ""

@dataclass
class ConfigLanguageSettings:
    language: int = 0

@dataclass
class ConfigLogSettings:
    log_auto_save: bool = False
    log_save_ma: bool = False
    log_save_fft: bool = False
    log_save_std: bool = False
    log_filename_prefix: str = ""
    log_save_dst: str = ""
    log_sampling_num: int = 1000
    capture_save_dst: str = ""

@dataclass
class ConfigNetworkSettings:
    device1_ip: str = ""
    device2_ip: str = ""

class Config:
    CONFIG_SECTION_CONNECTION = "Connection"
    CONFIG_KEY_METHOD = "Method"
    CONFIG_KEY_COM1 = "Com1"
    CONFIG_KEY_COM2 = "Com2"
    CONFIG_KEY_IPADDR1 = "IP1"
    CONFIG_KEY_IPADDR2 = "IP2"

    CONFIG_SECTION_SAMPLING = "Sampling"
    CONFIG_KEY_RATE = "Rate"
    CONFIG_KEY_UNIT = "Unit"
    CONFIG_KEY_BUFFER_MODE = "BufferMode"
    CONFIG_KEY_BUFFER_INTERVAL_MS = "BufferIntervalMs"
    CONFIG_KEY_BUFFER_TRANSFER_MODE = "BufferTransferMode"

    CONFIG_SECTION_CHART_FILTER = "ChartFilter"
    CONFIG_KEY_MOVING_AVERAGE = "MovingAverage"
    CONFIG_KEY_MOVING_AVERAGE_WINDOW = "MovingAverageWindow"
    CONFIG_KEY_FFT = "FFT"
    CONFIG_KEY_FFT_RESOLUTION = "FFTResolution"
    CONFIG_KEY_FFT_WINDOW = "FFTWindow"
    CONFIG_KEY_STANDARD_DEVIATION = "StandardDeviation"
    CONFIG_KEY_STANDARD_DEVIATION_WINDOW = "StandardDeviationWindow"

    CONFIG_SECTION_SENSOR_SETTINGS = "SensorSettings"
    CONFIG_KEY_STRAIN_COLOR = "StrainColor"
    CONFIG_KEY_TEMP_COLOR = "TempColor"
    CONFIG_KEY_WIDTH = "Width"
    CONFIG_KEY_OFFSET = "Offset"

    CONFIG_SECTION_CHART_DISPLAY = "ChartDisplay"
    CONFIG_KEY_MODE = "Unit"
    CONFIG_KEY_SHOW_SENSOR_NAME = "ShowSensorName"
    CONFIG_KEY_SHOW_TEMP = "ShowTemp"
    CONFIG_KEY_SHOW_CURRENT = "ShowCurrent"
    CONFIG_KEY_SHOW_INIT = "ShowInit"
    CONFIG_KEY_SHOW_DELTA = "ShowDelta"
    CONFIG_KEY_SHOW_STATUS = "ShowStatus"
    CONFIG_KEY_SENSOR_NAME = "Name"
    CONFIG_KEY_STRAIN_LINE_VIEW = "StrainLine"
    CONFIG_KEY_TEMP_LINE_VIEW = "TempLine"

    CONFIG_SECTION_OTHER_SETTINGS = "OtherSettings"
    CONFIG_KEY_WINDOW_THEME = "WindowTheme"
    CONFIG_KEY_SC_MEAS_START = "SCMeasStart"
    CONFIG_KEY_SC_MEAS_STOP = "SCMeasStop"
    CONFIG_KEY_SC_AUTO_RANGE = "SCAutoRange"
    CONFIG_KEY_SC_SAVE_LOG = "SCSaveLog"
    CONFIG_KEY_SC_CAPTURE = "SCCapture"
    CONFIG_KEY_LANGUAGE = "Language"
    CONFIG_KEY_LOG_AUTO_SAVE = "LogAutoSave"
    CONFIG_KEY_LOG_SAVE_MA = "LogSaveMA"
    CONFIG_KEY_LOG_SAVE_FFT = "LogSaveFFT"
    CONFIG_KEY_LOG_SAVE_STD = "LogSaveStd"
    CONFIG_KEY_LOG_FILENAME_PREFIX = "LogFileNamePrefix"
    CONFIG_KEY_LOG_SAVE_DST = "LogSaveDst"
    CONFIG_KEY_LOG_SAMPLE_NUM = "LogSampleNum"
    CONFIG_KEY_CAPTURE_SAVE_DST = "CaptureSaveDst"

    def __init__(self):
        self.config_file_path = get_config_path("config.ini")
        self.settings = QSettings(self.config_file_path, QSettings.Format.IniFormat)

    def load_config_home(self)-> ConfigDataHome:
        config_home = ConfigDataHome()
        try:
            self.settings.beginGroup(self.CONFIG_SECTION_CONNECTION)
            config_home.connection_method = int(self.settings.value(self.CONFIG_KEY_METHOD, 0))
            config_home.com1 = str(self.settings.value(self.CONFIG_KEY_COM1, ""))
            config_home.com2 = str(self.settings.value(self.CONFIG_KEY_COM2, ""))
            config_home.ip_addr1 = str(self.settings.value(self.CONFIG_KEY_IPADDR1, ""))
            config_home.ip_addr2 = str(self.settings.value(self.CONFIG_KEY_IPADDR2, ""))
            self.settings.endGroup()
        except Exception:
            print("Failed to load config file(ConfigDataHome)")
        return config_home

    def save_config_home(self, config:ConfigDataHome):
        try:
            self.settings.beginGroup(self.CONFIG_SECTION_CONNECTION)
            self.settings.setValue(self.CONFIG_KEY_METHOD, config.connection_method)
            self.settings.setValue(self.CONFIG_KEY_COM1, config.com1)
            self.settings.setValue(self.CONFIG_KEY_COM2, config.com2)
            self.settings.setValue(self.CONFIG_KEY_IPADDR1, config.ip_addr1)
            self.settings.setValue(self.CONFIG_KEY_IPADDR2, config.ip_addr2)
            self.settings.endGroup()
        except Exception:
            print("Failed to save config file(ConfigDataHome)")

    def load_config_sampling(self)-> ConfigSampling:
        config_sampling = ConfigSampling()
        try:
            self.settings.beginGroup(self.CONFIG_SECTION_SAMPLING)
            config_sampling.sampling_rate = str(self.settings.value(self.CONFIG_KEY_RATE, 1000))
            config_sampling.sampling_unit = int(self.settings.value(self.CONFIG_KEY_UNIT, 0))
            config_sampling.buffer_mode = self.settings.value(self.CONFIG_KEY_BUFFER_MODE, False, bool)
            config_sampling.buffer_interval_ms = str(self.settings.value(self.CONFIG_KEY_BUFFER_INTERVAL_MS, 100))
            config_sampling.buffer_transfer_mode = int(self.settings.value(self.CONFIG_KEY_BUFFER_TRANSFER_MODE, 2))
            self.settings.endGroup()
        except Exception:
            print("Failed to load config file(ConfigSampling)")
        return config_sampling

    def save_config_sampling(self, config:ConfigSampling):
        try:
            self.settings.beginGroup(self.CONFIG_SECTION_SAMPLING)
            self.settings.setValue(self.CONFIG_KEY_RATE, config.sampling_rate)
            self.settings.setValue(self.CONFIG_KEY_UNIT, config.sampling_unit)
            self.settings.setValue(self.CONFIG_KEY_BUFFER_MODE, config.buffer_mode)
            self.settings.setValue(self.CONFIG_KEY_BUFFER_INTERVAL_MS, config.buffer_interval_ms)
            self.settings.setValue(self.CONFIG_KEY_BUFFER_TRANSFER_MODE, config.buffer_transfer_mode)
            self.settings.endGroup()
        except Exception:
            print("Failed to save config file(ConfigSampling)")

    def load_config_filter(self) -> ConfigDataChartFilter:
        config_filter = ConfigDataChartFilter()
        try:
            self.settings.beginGroup(self.CONFIG_SECTION_CHART_FILTER)
            config_filter.filter_moving_average = True if self.settings.value(self.CONFIG_KEY_MOVING_AVERAGE, "false") == "true" else False
            config_filter.filter_moving_average_window = int(self.settings.value(self.CONFIG_KEY_MOVING_AVERAGE_WINDOW, "2"))
            config_filter.filter_fft = True if self.settings.value(self.CONFIG_KEY_FFT, "false") == "true" else False
            config_filter.filter_fft_resolution = int(self.settings.value(self.CONFIG_KEY_FFT_RESOLUTION, "256"))
            config_filter.filter_fft_window = str(self.settings.value(self.CONFIG_KEY_FFT_WINDOW, ""))
            config_filter.filter_standard_deviation = True if self.settings.value(self.CONFIG_KEY_STANDARD_DEVIATION, "false") == "true" else False
            config_filter.filter_standard_deviation_window = int(self.settings.value(self.CONFIG_KEY_STANDARD_DEVIATION_WINDOW, "1"))
            self.settings.endGroup()
        except Exception:
            print("Failed to load config file(ConfigDataChartFilter)")
        return config_filter

    def save_config_filter(self, config:ConfigDataChartFilter):
        try:
            self.settings.beginGroup(self.CONFIG_SECTION_CHART_FILTER)
            self.settings.setValue(self.CONFIG_KEY_MOVING_AVERAGE, config.filter_moving_average)
            self.settings.setValue(self.CONFIG_KEY_MOVING_AVERAGE_WINDOW, config.filter_moving_average_window)
            self.settings.setValue(self.CONFIG_KEY_FFT, config.filter_fft)
            self.settings.setValue(self.CONFIG_KEY_FFT_RESOLUTION, config.filter_fft_resolution)
            self.settings.setValue(self.CONFIG_KEY_FFT_WINDOW, config.filter_fft_window)
            self.settings.setValue(self.CONFIG_KEY_STANDARD_DEVIATION, config.filter_standard_deviation)
            self.settings.setValue(self.CONFIG_KEY_STANDARD_DEVIATION_WINDOW, config.filter_standard_deviation_window)
            self.settings.endGroup()
        except Exception:
            print("Failed to save config file(ConfigDataChartFilter)")

    def load_config_sensor_settings(self)-> ConfigDataChartSensorSettings:
        config_sensor_settings = ConfigDataChartSensorSettings()
        try:
            self.settings.beginGroup(self.CONFIG_SECTION_SENSOR_SETTINGS)
            strain_color_list_string = self.settings.value(self.CONFIG_KEY_STRAIN_COLOR, "")
            temp_color_list_string = self.settings.value(self.CONFIG_KEY_TEMP_COLOR, "")
            width_list_string = self.settings.value(self.CONFIG_KEY_WIDTH, "")
            offset_list_string = self.settings.value(self.CONFIG_KEY_OFFSET, "")
            if strain_color_list_string:
                strain_color_list = [int(item) for item in strain_color_list_string]
            else:
                strain_color_list = [2, 4, 0, 3]
            if temp_color_list_string:
                temp_color_list = [int(item) for item in temp_color_list_string]
            else:
                temp_color_list = [2, 4, 0, 3]
            if width_list_string:
                width_list = [int(item) for item in width_list_string]
            else:
                width_list = [3, 3, 3, 3]
            if offset_list_string:
                offset_list = [int(item) for item in offset_list_string]
            else:
                offset_list = [0, 0, 0, 0]
            config_sensor_settings.sensor_strain_line_color = strain_color_list
            config_sensor_settings.sensor_temp_line_color = temp_color_list
            config_sensor_settings.sensor_line_width = width_list
            config_sensor_settings.sensor_line_offset = offset_list
            self.settings.endGroup()
        except Exception:
            print("Failed to load config file(ConfigDataChartSensorSettings)")
        return config_sensor_settings

    def save_config_sensor_settings(self, config:ConfigDataChartSensorSettings):
        try:
            self.settings.beginGroup(self.CONFIG_SECTION_SENSOR_SETTINGS)
            self.settings.setValue(self.CONFIG_KEY_STRAIN_COLOR, config.sensor_strain_line_color)
            self.settings.setValue(self.CONFIG_KEY_TEMP_COLOR, config.sensor_temp_line_color)
            self.settings.setValue(self.CONFIG_KEY_WIDTH, config.sensor_line_width)
            self.settings.setValue(self.CONFIG_KEY_OFFSET, config.sensor_line_offset)
            self.settings.endGroup()
        except Exception:
            print("Failed to save config file(ConfigDataChartSensorSettings)")

    def load_config_chart_display(self)-> ConfigDataChartSensorDataDisplay:
        config_chart_display = ConfigDataChartSensorDataDisplay()
        try:
            self.settings.beginGroup(self.CONFIG_SECTION_CHART_DISPLAY)
            config_chart_display.chart_unit = int(self.settings.value(self.CONFIG_KEY_MODE, 0))
            config_chart_display.show_sensor_name = True if self.settings.value(self.CONFIG_KEY_SHOW_SENSOR_NAME, "true") == "true" else False
            config_chart_display.show_temperature = True if self.settings.value(self.CONFIG_KEY_SHOW_TEMP, "true") == "true" else False
            config_chart_display.show_current_value = True if self.settings.value(self.CONFIG_KEY_SHOW_CURRENT, "true") == "true" else False
            config_chart_display.show_init_value = True if self.settings.value(self.CONFIG_KEY_SHOW_INIT, "true") == "true" else False
            config_chart_display.show_delta_value = True if self.settings.value(self.CONFIG_KEY_SHOW_DELTA, "true") == "true" else False
            config_chart_display.show_status = True if self.settings.value(self.CONFIG_KEY_SHOW_STATUS, "true") == "true" else False

            name_list_string = self.settings.value(self.CONFIG_KEY_SENSOR_NAME, "")
            if not name_list_string:
                name_list_string = ["#1", "#2", "#3", "#4"]
            config_chart_display.sensor_name = name_list_string
            line_view_list_string = self.settings.value(self.CONFIG_KEY_STRAIN_LINE_VIEW, "")
            line_view_list:list[bool] = []
            if line_view_list_string:
                for line_view in line_view_list_string:
                    line_view_list.append(True if line_view == "true" else False)
            else:
                line_view_list = [True, True, True, True]
            config_chart_display.strain_line_view = line_view_list
            line_view_list_string = self.settings.value(self.CONFIG_KEY_TEMP_LINE_VIEW, "")
            line_view_list: list[bool] = []
            if line_view_list_string:
                for line_view in line_view_list_string:
                    line_view_list.append(True if line_view == "true" else False)
            else:
                line_view_list = [True, True, True, True]
            config_chart_display.temp_line_view = line_view_list
            self.settings.endGroup()
        except Exception:
            print("Failed to load config file(ConfigDataChartSensorDataDisplay)")
        return config_chart_display

    def save_config_chart_display(self, config:ConfigDataChartSensorDataDisplay):
        try:
            self.settings.beginGroup(self.CONFIG_SECTION_CHART_DISPLAY)
            self.settings.setValue(self.CONFIG_KEY_MODE, config.chart_unit)
            self.settings.setValue(self.CONFIG_KEY_SHOW_SENSOR_NAME, config.show_sensor_name)
            self.settings.setValue(self.CONFIG_KEY_SHOW_TEMP, config.show_temperature)
            self.settings.setValue(self.CONFIG_KEY_SHOW_CURRENT, config.show_current_value)
            self.settings.setValue(self.CONFIG_KEY_SHOW_INIT, config.show_init_value)
            self.settings.setValue(self.CONFIG_KEY_SHOW_DELTA, config.show_delta_value)
            self.settings.setValue(self.CONFIG_KEY_SHOW_STATUS, config.show_status)
            self.settings.setValue(self.CONFIG_KEY_SENSOR_NAME, config.sensor_name)
            self.settings.setValue(self.CONFIG_KEY_STRAIN_LINE_VIEW, config.strain_line_view)
            self.settings.setValue(self.CONFIG_KEY_TEMP_LINE_VIEW, config.temp_line_view)
            self.settings.endGroup()
        except Exception:
            print("Failed to save config file(ConfigDataChartSensorDataDisplay)")

    def load_config_theme(self) -> ConfigThemeSettings:
        config = ConfigThemeSettings()
        try:
            self.settings.beginGroup(self.CONFIG_SECTION_OTHER_SETTINGS)
            config.window_theme = self.settings.value(self.CONFIG_KEY_WINDOW_THEME, 0, int)
            self.settings.endGroup()
        except Exception:
            print("Failed to load config file(ConfigDataOtherSettings)")
        return config

    def save_config_theme(self, config: ConfigThemeSettings):
        try:
            self.settings.beginGroup(self.CONFIG_SECTION_OTHER_SETTINGS)
            self.settings.setValue(self.CONFIG_KEY_WINDOW_THEME, config.window_theme)
            self.settings.endGroup()
        except Exception:
            print("Failed to save config file(ConfigDataOtherSettings)")

    def load_config_shortcut(self) -> ConfigShortcutSettings:
        config = ConfigShortcutSettings()
        try:
            self.settings.beginGroup(self.CONFIG_SECTION_OTHER_SETTINGS)
            config.meas_start = str(self.settings.value(self.CONFIG_KEY_SC_MEAS_START, ""))
            config.meas_stop = str(self.settings.value(self.CONFIG_KEY_SC_MEAS_STOP, ""))
            config.auto_range = str(self.settings.value(self.CONFIG_KEY_SC_AUTO_RANGE, ""))
            config.save_log = str(self.settings.value(self.CONFIG_KEY_SC_SAVE_LOG, ""))
            config.capture = str(self.settings.value(self.CONFIG_KEY_SC_CAPTURE, ""))
            self.settings.endGroup()
        except Exception:
            print("Failed to load config file(ConfigDataOtherSettings)")
        return config

    def save_config_shortcut(self, config: ConfigShortcutSettings):
        try:
            self.settings.beginGroup(self.CONFIG_SECTION_OTHER_SETTINGS)
            self.settings.setValue(self.CONFIG_KEY_SC_MEAS_START, config.meas_start)
            self.settings.setValue(self.CONFIG_KEY_SC_MEAS_STOP, config.meas_stop)
            self.settings.setValue(self.CONFIG_KEY_SC_AUTO_RANGE, config.auto_range)
            self.settings.setValue(self.CONFIG_KEY_SC_SAVE_LOG, config.save_log)
            self.settings.setValue(self.CONFIG_KEY_SC_CAPTURE, config.capture)
            self.settings.endGroup()
        except Exception:
            print("Failed to load config file(ConfigDataOtherSettings)")

    def load_config_language(self) -> ConfigLanguageSettings:
        config = ConfigLanguageSettings()
        try:
            self.settings.beginGroup(self.CONFIG_SECTION_OTHER_SETTINGS)
            config.language = self.settings.value(self.CONFIG_KEY_LANGUAGE, 0, int)
            self.settings.endGroup()
        except Exception:
            print("Failed to load config file(ConfigDataOtherSettings)")
        return config

    def save_config_language(self, config: ConfigLanguageSettings):
        try:
            self.settings.beginGroup(self.CONFIG_SECTION_OTHER_SETTINGS)
            self.settings.setValue(self.CONFIG_KEY_LANGUAGE, config.language)
            self.settings.endGroup()
        except Exception:
            print("Failed to load config file(ConfigDataOtherSettings)")

    def load_config_log(self) -> ConfigLogSettings:
        config = ConfigLogSettings()
        try:
            self.settings.beginGroup(self.CONFIG_SECTION_OTHER_SETTINGS)
            config.log_auto_save = self.settings.value(self.CONFIG_KEY_LOG_AUTO_SAVE, False, bool)
            config.log_save_ma = self.settings.value(self.CONFIG_KEY_LOG_SAVE_MA, False, bool)
            config.log_save_fft = self.settings.value(self.CONFIG_KEY_LOG_SAVE_FFT, False, bool)
            config.log_save_std = self.settings.value(self.CONFIG_KEY_LOG_SAVE_STD, False, bool)
            config.log_filename_prefix = self.settings.value(self.CONFIG_KEY_LOG_FILENAME_PREFIX, "", str)
            config.log_save_dst = self.settings.value(self.CONFIG_KEY_LOG_SAVE_DST, "", str)
            config.log_sampling_num = self.settings.value(self.CONFIG_KEY_LOG_SAMPLE_NUM, 30000, int)
            config.capture_save_dst = self.settings.value(self.CONFIG_KEY_CAPTURE_SAVE_DST, "", str)
            self.settings.endGroup()
        except Exception:
            print("Failed to load config file(ConfigDataOtherSettings)")
        return config

    def save_config_log(self, config: ConfigLogSettings):
        try:
            self.settings.beginGroup(self.CONFIG_SECTION_OTHER_SETTINGS)
            self.settings.setValue(self.CONFIG_KEY_LOG_AUTO_SAVE, config.log_auto_save)
            self.settings.setValue(self.CONFIG_KEY_LOG_SAVE_MA, config.log_save_ma)
            self.settings.setValue(self.CONFIG_KEY_LOG_SAVE_FFT, config.log_save_fft)
            self.settings.setValue(self.CONFIG_KEY_LOG_SAVE_STD, config.log_save_std)
            self.settings.setValue(self.CONFIG_KEY_LOG_FILENAME_PREFIX, config.log_filename_prefix)
            self.settings.setValue(self.CONFIG_KEY_LOG_SAVE_DST, config.log_save_dst)
            self.settings.setValue(self.CONFIG_KEY_LOG_SAMPLE_NUM, config.log_sampling_num)
            self.settings.setValue(self.CONFIG_KEY_CAPTURE_SAVE_DST, config.capture_save_dst)
            self.settings.endGroup()
        except Exception:
            print("Failed to load config file(ConfigDataOtherSettings)")

    def load_config_network(self) -> ConfigNetworkSettings:
        config = ConfigNetworkSettings()
        try:
            self.settings.beginGroup(self.CONFIG_SECTION_CONNECTION)
            config.device1_ip = str(self.settings.value(self.CONFIG_KEY_IPADDR1, ""))
            config.device2_ip = str(self.settings.value(self.CONFIG_KEY_IPADDR2, ""))
            self.settings.endGroup()
        except Exception:
            print("Failed to load config file(ConfigNetworkSettings)")
        return config

    def save_config_network(self, config: ConfigNetworkSettings):
        try:
            self.settings.beginGroup(self.CONFIG_SECTION_CONNECTION)
            self.settings.setValue(self.CONFIG_KEY_IPADDR1, config.device1_ip)
            self.settings.setValue(self.CONFIG_KEY_IPADDR2, config.device2_ip)
            self.settings.endGroup()
        except Exception:
            print("Failed to save config file(ConfigNetworkSettings)")
