import builtins
import ipaddress
import json
import sys
import threading
from decimal import Decimal

from PySide6 import QtCore

from Models.Board import BoardKind
from Models.Hizmil_Driver import ConnectionStatus, ModeKind, ResultKind
from Models.Sensor import RegData
from Utils.AppControl import AppControlServer, register_command_controller, unregister_command_controller


ACTIVE_CUI_CONTROLLER = None


def get_active_cui_controller():
    return ACTIVE_CUI_CONTROLLER


def get_active_driver():
    controller = get_active_cui_controller()
    return None if controller is None else controller.driver


def set_transfer_mode(mode):
    controller = get_active_cui_controller()
    if controller is None:
        raise RuntimeError("CuiController is not initialized.")
    return controller.set_transfer_mode(mode)


def get_sensor_type(board):
    controller = get_active_cui_controller()
    if controller is None:
        raise RuntimeError("CuiController is not initialized.")
    return controller.get_sensor_type(board)


def get_network_address(board, network_type):
    controller = get_active_cui_controller()
    if controller is None:
        raise RuntimeError("CuiController is not initialized.")
    return controller.get_network_address(board, network_type)


def set_network_address(board, network_type, address):
    controller = get_active_cui_controller()
    if controller is None:
        raise RuntimeError("CuiController is not initialized.")
    return controller.set_network_address(board, network_type, address)


def transfer_mode_on():
    return set_transfer_mode("on")


def transfer_mode_off():
    return set_transfer_mode("off")


class ConsoleCommandBridge(QtCore.QObject):
    commandReceived = QtCore.Signal(str)


class MainThreadCommandBridge(QtCore.QObject):
    commandReceived = QtCore.Signal(object)


class CuiController:
    DEFAULT_USB_TARGETS = ["", ""]
    DEFAULT_LAN_TARGETS = ["0.0.0.0", "0.0.0.0"]

    def __init__(self, main_controller, enable_console: bool = False):
        global ACTIVE_CUI_CONTROLLER

        self.main_controller = main_controller
        self._enable_console = enable_console
        self._last_error = None
        self._console_bridge = ConsoleCommandBridge()
        self._console_bridge.commandReceived.connect(self.handle_console_command)
        self._main_thread_bridge = MainThreadCommandBridge()
        self._main_thread_bridge.commandReceived.connect(self._execute_on_main_thread)
        self._console_thread = None
        self.app_control_server = AppControlServer()

        ACTIVE_CUI_CONTROLLER = self
        register_command_controller(self)
        self.register_console_helpers()

    @property
    def driver(self):
        return self.main_controller.driver

    @property
    def window(self):
        return self.main_controller.window

    def start(self):
        self.app_control_server.start()
        self.start_console_interface()

    def stop(self):
        global ACTIVE_CUI_CONTROLLER

        self.app_control_server.stop()
        unregister_command_controller(self)
        if ACTIVE_CUI_CONTROLLER is self:
            ACTIVE_CUI_CONTROLLER = None

    def refresh_driver(self):
        self.register_console_helpers()

    def start_console_interface(self):
        if not self._enable_console:
            return
        if self._console_thread is not None:
            return
        if not hasattr(sys.stdin, "isatty") or not sys.stdin.isatty():
            print("Console mode requested, but stdin is not interactive.", flush=True)
            return

        self._console_thread = threading.Thread(
            target=self.console_input_loop,
            name="ConsoleCommandThread",
            daemon=True,
        )
        self._console_thread.start()
        self.print_console_help()

    def console_input_loop(self):
        while True:
            line = sys.stdin.readline()
            if line == "":
                break

            command = line.strip()
            if command:
                self._console_bridge.commandReceived.emit(command)

    def print_console_help(self):
        print("Console commands:", flush=True)
        print("  help", flush=True)
        print("  status", flush=True)
        print("  get_status <board1|board2> <ch1|ch2>", flush=True)
        print("  get_version", flush=True)
        print("  set_time", flush=True)
        print("  connect <usb|lan> <target1> [target2]", flush=True)
        print("  disconnect", flush=True)
        print("  start_measure <interval_us> [all|no_status|strain_only]", flush=True)
        print("  stop_measure", flush=True)
        print("  write_reg <board1|board2> <ch1|ch2> <page> <addr:data> [addr:data ...]", flush=True)
        print("  read_reg_page <board1|board2> <ch1|ch2> <page>", flush=True)
        print("  set_rom <board1|board2> <ch1|ch2>", flush=True)
        print("  read_reg <board1|board2> <ch1|ch2> <page> <addr> [addr ...]", flush=True)
        print("  set_transfer_mode <off|on|1|2>", flush=True)
        print("  get_sensor_type <board1|board2>", flush=True)
        print("  get_network_address <board1|board2> <ip|subnet|gateway|mac>", flush=True)
        print("  set_network_address <board1|board2> <ip|subnet|gateway|mac> <address>", flush=True)
        print("  offset_calibration <board1|board2> <ch1|ch2> [external_temp]", flush=True)
        print("  temp_calibration <board1|board2> <ch1|ch2> [external_temp]", flush=True)
        print("  get_sampling_count", flush=True)
        print("  get_sampling_data", flush=True)
        print("  exit", flush=True)

    def handle_console_command(self, command: str):
        parts = command.split()
        if not parts:
            return

        name = parts[0].lower()
        if name in ("help", "?"):
            self.print_console_help()
            return
        if name == "status":
            print(json.dumps(self.get_app_status(), ensure_ascii=False, indent=2), flush=True)
            return
        if name == "get_version":
            self.handle_get_version_command(parts[1:])
            return
        if name == "set_time":
            self.handle_set_time_command(parts[1:])
            return
        if name == "connect":
            if len(parts) < 3:
                print("Usage: connect <usb|lan> <target1> [target2]", flush=True)
                return
            target2 = parts[3] if len(parts) >= 4 else None
            try:
                result = self.connect(parts[1], [parts[2], target2])
            except (RuntimeError, ValueError) as exc:
                print(str(exc), flush=True)
                return
            print(f"connect {parts[1]} -> {result}", flush=True)
            return
        if name == "disconnect":
            result = self.disconnect()
            print(f"disconnect -> {result}", flush=True)
            return
        if name == "start_measure":
            self.handle_start_measure_command(parts[1:])
            return
        if name == "measure_start":
            if len(parts) < 3:
                print("Usage: measure_start <rate> <Hz|sps|ms> [all|no_status|strain_only]", flush=True)
                return
            mode = parts[3] if len(parts) >= 4 else "all"
            try:
                result = self.start_measure(
                    sampling_rate=parts[1],
                    sampling_unit=parts[2],
                    mode=mode,
                )
            except Exception as exc:
                print(str(exc), flush=True)
                return
            print(f"measure_start -> {result}", flush=True)
            return
        if name in ("measure_stop", "stop_measure"):
            try:
                result = self.stop_measure()
            except Exception as exc:
                print(str(exc), flush=True)
                return
            print(f"{name} -> {result}", flush=True)
            return
        if name in ("exit", "quit"):
            self.window.close()
            return
        if name in ("get_status", "gs"):
            self.handle_channel_getstatus_command(parts[1:])
            return
        if name == "write_reg":
            self.handle_write_reg_command(parts[1:])
            return
        if name == "read_reg_page":
            self.handle_read_reg_page_command(parts[1:])
            return
        if name == "set_rom":
            self.handle_set_rom_command(parts[1:])
            return
        if name == "read_reg":
            self.handle_read_reg_command(parts[1:])
            return
        if name in ("transfer_mode", "set_transfer_mode", "tm"):
            self.handle_transfer_mode_command(parts[1:])
            return
        if name in ("sensor_type", "get_sensor_type", "st"):
            self.handle_sensor_type_command(parts[1:])
            return
        if name == "get_network_address":
            self.handle_network_address_command(["get", *parts[1:]])
            return
        if name == "set_network_address":
            self.handle_network_address_command(["set", *parts[1:]])
            return
        if name in ("network_addr", "netaddr", "na"):
            self.handle_network_address_command(parts[1:])
            return
        if name == "offset_calibration":
            self.handle_offset_calibration_command(parts[1:])
            return
        if name == "temp_calibration":
            self.handle_temp_calibration_command(parts[1:])
            return
        if name == "get_sampling_count":
            self.handle_get_sampling_count_command(parts[1:])
            return
        if name == "get_sampling_data":
            self.handle_get_sampling_data_command(parts[1:])
            return

        print(f"Unknown console command: {command}", flush=True)
        self.print_console_help()

    def handle_channel_getstatus_command(self, args: list[str]):
        if len(args) != 2:
            print("Usage: get_status <board1|board2> <ch1|ch2>", flush=True)
            return

        try:
            result, status_data, sensor_status = self.get_status(args[0], args[1])
        except (RuntimeError, ValueError) as exc:
            print(str(exc), flush=True)
            return

        if result != ResultKind.ok:
            print(f"get_status {args[0]} {args[1]} -> {result}", flush=True)
            return

        print(
            f"get_status {args[0]} {args[1]} -> {result} "
            f"raw_status=0x{status_data.status:02X} "
            f"status={self.format_error_status(sensor_status.status)} "
            f"connection={self.format_connection_status(sensor_status.connection_status)} "
            f"temp={status_data.temp:.3f} "
            f"strain={status_data.strain} "
            f"strain_value={sensor_status.current_strain_value:.3f}",
            flush=True,
        )

    def handle_get_version_command(self, args: list[str]):
        if args:
            print("Usage: get_version", flush=True)
            return

        try:
            result, versions = self.get_version()
        except (RuntimeError, ValueError, NotImplementedError) as exc:
            print(str(exc), flush=True)
            return

        version_text = " ".join(
            f"board{i + 1}={self.format_version_value(version)}"
            for i, version in enumerate(versions)
        )
        print(f"get_version -> {result} {version_text}", flush=True)

    def handle_set_time_command(self, args: list[str]):
        if args:
            print("Usage: set_time", flush=True)
            return

        try:
            result = self.set_time()
        except (RuntimeError, ValueError, NotImplementedError) as exc:
            print(str(exc), flush=True)
            return

        print(f"set_time -> {result}", flush=True)

    def handle_start_measure_command(self, args: list[str]):
        if not 1 <= len(args) <= 2:
            print("Usage: start_measure <interval_us> [all|no_status|strain_only]", flush=True)
            return

        mode = args[1] if len(args) == 2 else "all"
        try:
            interval = self.parse_int(args[0], "interval")
            result = self.start_measure(interval=interval, mode=mode)
        except Exception as exc:
            print(str(exc), flush=True)
            return

        print(f"start_measure -> {result}", flush=True)

    def handle_write_reg_command(self, args: list[str]):
        if len(args) < 4:
            print("Usage: write_reg <board1|board2> <ch1|ch2> <page> <addr:data> [addr:data ...]", flush=True)
            return

        try:
            page = self.parse_page(args[2])
            reg_data = self.parse_register_data(args[3:])
            result = self.write_reg(args[0], args[1], page, reg_data)
        except (RuntimeError, ValueError, NotImplementedError) as exc:
            print(str(exc), flush=True)
            return

        print(f"write_reg {args[0]} {args[1]} {page} -> {result} {self.format_register_data(reg_data)}", flush=True)

    def handle_read_reg_page_command(self, args: list[str]):
        if len(args) != 3:
            print("Usage: read_reg_page <board1|board2> <ch1|ch2> <page>", flush=True)
            return

        try:
            page = self.parse_page(args[2])
            result, reg_data = self.read_reg_page(args[0], args[1], page)
        except (RuntimeError, ValueError, NotImplementedError) as exc:
            print(str(exc), flush=True)
            return

        print(f"read_reg_page {args[0]} {args[1]} {page} -> {result} {self.format_register_data(reg_data)}", flush=True)

    def handle_set_rom_command(self, args: list[str]):
        if len(args) != 2:
            print("Usage: set_rom <board1|board2> <ch1|ch2>", flush=True)
            return

        try:
            result = self.set_rom(args[0], args[1])
        except (RuntimeError, ValueError, NotImplementedError) as exc:
            print(str(exc), flush=True)
            return

        print(f"set_rom {args[0]} {args[1]} -> {result}", flush=True)

    def handle_read_reg_command(self, args: list[str]):
        if len(args) < 4:
            print("Usage: read_reg <board1|board2> <ch1|ch2> <page> <addr> [addr ...]", flush=True)
            return

        try:
            page = self.parse_page(args[2])
            addresses = self.parse_register_addresses(args[3:])
            result, reg_data = self.read_reg(args[0], args[1], page, addresses)
        except (RuntimeError, ValueError, NotImplementedError) as exc:
            print(str(exc), flush=True)
            return

        print(f"read_reg {args[0]} {args[1]} {page} -> {result} {self.format_register_data(reg_data)}", flush=True)

    def handle_offset_calibration_command(self, args: list[str]):
        self._handle_calibration_command("offset_calibration", self.offset_calibration, args)

    def handle_temp_calibration_command(self, args: list[str]):
        self._handle_calibration_command("temp_calibration", self.temp_calibration, args)

    def _handle_calibration_command(self, command_name: str, func, args: list[str]):
        if not 2 <= len(args) <= 3:
            print(f"Usage: {command_name} <board1|board2> <ch1|ch2> [external_temp]", flush=True)
            return

        try:
            ex_temp, ex_temp_enable = self.parse_optional_temperature(args[2:])
            result = func(args[0], args[1], ex_temp=ex_temp, ex_temp_enable=ex_temp_enable)
        except (RuntimeError, ValueError, NotImplementedError, ZeroDivisionError) as exc:
            print(str(exc), flush=True)
            return

        suffix = f" external_temp={ex_temp}" if ex_temp_enable else ""
        print(f"{command_name} {args[0]} {args[1]} -> {result}{suffix}", flush=True)

    def handle_get_sampling_count_command(self, args: list[str]):
        if args:
            print("Usage: get_sampling_count", flush=True)
            return

        try:
            result, count = self.get_sampling_count()
        except (RuntimeError, ValueError, NotImplementedError) as exc:
            print(str(exc), flush=True)
            return

        print(f"get_sampling_count -> {result} count={count}", flush=True)

    def handle_get_sampling_data_command(self, args: list[str]):
        if args:
            print("Usage: get_sampling_data", flush=True)
            return

        try:
            result, value = self.get_sampling_data()
        except (RuntimeError, ValueError, NotImplementedError) as exc:
            print(str(exc), flush=True)
            return

        print(f"get_sampling_data -> {result} value={value}", flush=True)

    def handle_transfer_mode_command(self, args: list[str]):
        if len(args) != 1:
            print("Usage: set_transfer_mode <off|on|1|2>", flush=True)
            return
        if not self.driver.is_connected():
            print("Driver is not connected.", flush=True)
            return

        value = args[0].lower()
        try:
            result = self.set_transfer_mode(value)
        except ValueError:
            print("Usage: set_transfer_mode <off|on|1|2>", flush=True)
            return
        print(f"set_transfer_mode {value} -> {result}", flush=True)

    def handle_sensor_type_command(self, args: list[str]):
        if len(args) != 1:
            print("Usage: get_sensor_type <board1|board2>", flush=True)
            return

        try:
            result, ch1_type, ch2_type = self.get_sensor_type(args[0])
        except (RuntimeError, ValueError) as exc:
            print(str(exc), flush=True)
            return

        print(
            f"get_sensor_type {args[0]} -> {result} "
            f"ch1={self.format_sensor_type(ch1_type)} "
            f"ch2={self.format_sensor_type(ch2_type)}",
            flush=True,
        )

    def handle_network_address_command(self, args: list[str]):
        if len(args) < 3:
            print(
                "Usage: get_network_address <board1|board2> <ip|subnet|gateway|mac>",
                flush=True,
            )
            print("Usage: set_network_address <board1|board2> <ip|subnet|gateway|mac> <address>", flush=True)
            return

        action = args[0].lower()
        if action == "get":
            if len(args) != 3:
                print("Usage: get_network_address <board1|board2> <ip|subnet|gateway|mac>", flush=True)
                return
            try:
                result, address = self.get_network_address(args[1], args[2])
                network_type = self.parse_network_type(args[2])
            except (RuntimeError, ValueError) as exc:
                print(str(exc), flush=True)
                return

            address_text = self.format_network_address(network_type, address) if result == ResultKind.ok else "-"
            print(f"get_network_address {args[1]} {args[2]} -> {result} {address_text}", flush=True)
            return

        if action == "set":
            if len(args) != 4:
                print("Usage: set_network_address <board1|board2> <ip|subnet|gateway|mac> <address>", flush=True)
                return
            try:
                result, response_address = self.set_network_address(args[1], args[2], args[3])
                network_type = self.parse_network_type(args[2])
            except (RuntimeError, ValueError) as exc:
                print(str(exc), flush=True)
                return

            address_text = (
                self.format_network_address(network_type, response_address)
                if result == ResultKind.ok
                else "-"
            )
            print(f"set_network_address {args[1]} {args[2]} -> {result} {address_text}", flush=True)
            return

        print(
            "Usage: get_network_address <board1|board2> <ip|subnet|gateway|mac>",
            flush=True,
        )
        print("Usage: set_network_address <board1|board2> <ip|subnet|gateway|mac> <address>", flush=True)

    def register_console_helpers(self):
        builtins.hizmil_app = self.main_controller
        builtins.hizmil_cui = self
        builtins.hizmil_driver = self.driver
        builtins.hizmil_connect = self.connect
        builtins.hizmil_disconnect = self.disconnect
        builtins.hizmil_get_version = self.get_version
        builtins.hizmil_set_time = self.set_time
        builtins.hizmil_start_measure = self.start_measure
        builtins.hizmil_stop_measure = self.stop_measure
        builtins.hizmil_get_app_status = self.get_app_status
        builtins.hizmil_get_status = self.get_status
        builtins.hizmil_write_reg = self.write_reg
        builtins.hizmil_read_reg_page = self.read_reg_page
        builtins.hizmil_set_rom = self.set_rom
        builtins.hizmil_read_reg = self.read_reg
        builtins.hizmil_get_sampling_count = self.get_sampling_count
        builtins.hizmil_get_sampling_data = self.get_sampling_data
        builtins.hizmil_offset_calibration = self.offset_calibration
        builtins.hizmil_temp_calibration = self.temp_calibration
        builtins.hizmil_shutdown_app = self.shutdown_app
        builtins.hizmil_set_transfer_mode = set_transfer_mode
        builtins.hizmil_get_sensor_type = get_sensor_type
        builtins.hizmil_get_network_address = get_network_address
        builtins.hizmil_set_network_address = set_network_address
        builtins.hizmil_transfer_mode_on = transfer_mode_on
        builtins.hizmil_transfer_mode_off = transfer_mode_off

    @QtCore.Slot(object)
    def _execute_on_main_thread(self, payload: object):
        try:
            payload["result"] = payload["func"](*payload["args"], **payload["kwargs"])
        except Exception as exc:
            payload["error"] = exc
        finally:
            payload["event"].set()

    def _invoke_on_main_thread(self, func, *args, **kwargs):
        if QtCore.QThread.currentThread() == self._main_thread_bridge.thread():
            return func(*args, **kwargs)

        payload = {
            "func": func,
            "args": args,
            "kwargs": kwargs,
            "event": threading.Event(),
        }
        self._main_thread_bridge.commandReceived.emit(payload)
        payload["event"].wait()
        if "error" in payload:
            raise payload["error"]
        return payload.get("result")

    def _parse_connection_method(self, method) -> int:
        if isinstance(method, int):
            if method in (0, 1):
                return method
        elif isinstance(method, str):
            key = method.strip().lower()
            mapping = {
                "0": 0,
                "usb": 0,
                "1": 1,
                "lan": 1,
            }
            if key in mapping:
                return mapping[key]
        raise ValueError(f"Invalid connection method: {method}")

    def _normalize_targets(self, method: int, targets) -> list[str]:
        default_targets = self.DEFAULT_USB_TARGETS if method == 0 else self.DEFAULT_LAN_TARGETS
        if isinstance(targets, str):
            normalized = [targets]
        elif targets is None:
            normalized = []
        else:
            normalized = list(targets)

        while len(normalized) < 2:
            normalized.append(default_targets[len(normalized)])
        normalized = normalized[:2]

        resolved = []
        for index, target in enumerate(normalized):
            if target is None:
                value = default_targets[index]
            else:
                value = str(target).strip()
                if method == 1 and value == "":
                    value = default_targets[index]
            resolved.append(value)
        return resolved

    def _parse_measure_mode(self, mode) -> ModeKind:
        if isinstance(mode, ModeKind):
            return mode
        if isinstance(mode, int):
            if mode == ModeKind.all.value:
                return ModeKind.all
        if isinstance(mode, str):
            key = mode.strip().lower()
            if key in ("1", "all"):
                return ModeKind.all
        raise ValueError("GUI mode only supports measurement mode 'all'.")

    def _calc_interval(self, sampling_rate, sampling_unit) -> int:
        rate = Decimal(str(sampling_rate))
        if rate <= 0:
            raise ValueError("sampling_rate must be greater than 0.")

        unit = "hz" if sampling_unit is None else str(sampling_unit).strip().lower()
        if unit in ("hz", "sps"):
            interval = 1000000 // rate
        elif unit == "ms":
            interval = rate * 1000
        else:
            raise ValueError(f"Unsupported sampling unit: {sampling_unit}")
        return int(interval)

    def _set_sampling_controls(self, sampling_rate, sampling_unit):
        chart_page = self.main_controller.chart_controller.chart_page
        if sampling_unit is None:
            unit_text = "Hz"
        else:
            unit_key = str(sampling_unit).strip().lower()
            unit_text = {
                "hz": "Hz",
                "sps": "sps",
                "ms": "ms",
            }.get(unit_key, str(sampling_unit))
        unit_index = chart_page.ui.sampling_rate_unit.findText(unit_text)
        if unit_index < 0:
            raise ValueError(f"Unsupported sampling unit: {sampling_unit}")

        chart_page.ui.sampling_rate_edit.setText(str(sampling_rate))
        chart_page.ui.sampling_rate_unit.setCurrentIndex(unit_index)

    def _do_connect(self, method: int, targets: list[str]):
        return self.main_controller.init_driver(method, targets)

    def _do_measure_start(self, interval=None, sampling_rate=None, sampling_unit="Hz"):
        if not self.driver.is_connected():
            raise RuntimeError("Driver is not connected.")
        if interval is None:
            if sampling_rate is None:
                raise ValueError("interval or sampling_rate must be specified.")
            self._set_sampling_controls(sampling_rate, sampling_unit)
        else:
            if int(interval) <= 0:
                raise ValueError("interval must be greater than 0.")
            if sampling_rate is None:
                sampling_rate = Decimal("1000000") / Decimal(str(interval))
                sampling_unit = "Hz"
            self._set_sampling_controls(sampling_rate, sampling_unit)

        return self.main_controller.chart_controller.measure_start()

    def _collect_status_snapshot(self):
        driver = self.driver
        snapshot = {
            "connected": driver.is_connected(),
            "measuring": bool(getattr(driver, "is_measuring", False)),
            "board_type": self.main_controller.board_type,
            "driver": type(driver).__name__,
            "targets": list(getattr(self.main_controller, "_com", [])),
            "versions": [],
            "board_connected": [],
            "sensor_ids": [],
            "sensor_status": [],
            "sensor_data": [],
            "sensor_type_ch1": list(getattr(driver, "sensor_type_ch1", [])),
            "sensor_type_ch2": list(getattr(driver, "sensor_type_ch2", [])),
            "last_error": self._last_error,
        }

        boards = getattr(driver, "board", [])
        if boards:
            snapshot["versions"] = driver.get_version_value()
            snapshot["board_connected"] = [
                driver.get_board_connection_status(BoardKind.board1),
                driver.get_board_connection_status(BoardKind.board2),
            ]

        if driver.is_connected():
            sensor_status = driver.get_sensor_status_all()
            snapshot["sensor_ids"] = driver.get_sensor_ids()
            snapshot["sensor_status"] = [sensor.connection_status.value for sensor in sensor_status]
            snapshot["sensor_data"] = [
                {
                    "temp": sensor.temp,
                    "current_strain": sensor.current_strain,
                    "init_strain": sensor.init_strain,
                    "current_strain_value": sensor.current_strain_value,
                    "init_strain_value": sensor.init_strain_value,
                    "status": sensor.status.name,
                    "connection_status": sensor.connection_status.name,
                }
                for sensor in sensor_status
            ]

        return snapshot

    def connect(self, method, targets):
        method_id = self._parse_connection_method(method)
        normalized_targets = self._normalize_targets(method_id, targets)
        result = self._invoke_on_main_thread(self._do_connect, method_id, normalized_targets)
        self._last_error = None if result == ConnectionStatus.success else result.name
        return result

    def disconnect(self):
        result = self._invoke_on_main_thread(self.main_controller.disconnect_driver)
        if result:
            self._last_error = None
        return result

    def get_version(self):
        return self._invoke_on_main_thread(self._get_version_impl)

    def _get_version_impl(self):
        self.ensure_connected()
        versions = [0] * BoardKind.board_num.value
        result = self.driver.get_version(versions)
        self._last_error = None if result == ResultKind.ok else result.name
        return result, versions

    def set_time(self):
        return self._invoke_on_main_thread(self._set_time_impl)

    def _set_time_impl(self):
        self.ensure_connected()
        result = self.driver.set_time()
        self._last_error = None if result == ResultKind.ok else result.name
        return result

    def start_measure(self, interval=None, sampling_rate=None, sampling_unit="Hz", mode="all"):
        self._parse_measure_mode(mode)
        result = self._invoke_on_main_thread(
            self._do_measure_start,
            interval,
            sampling_rate,
            sampling_unit,
        )
        self._last_error = None if result == ResultKind.ok else result.name
        return result

    def stop_measure(self):
        if not self.driver.is_connected():
            raise RuntimeError("Driver is not connected.")
        result = self._invoke_on_main_thread(self.main_controller.chart_controller.measure_stop)
        self._last_error = None if result == ResultKind.ok else result.name
        return result

    def get_app_status(self):
        snapshot = self._invoke_on_main_thread(self._collect_status_snapshot)
        return json.loads(json.dumps(snapshot))

    def shutdown_app(self):
        threading.Thread(
            target=lambda: self._invoke_on_main_thread(self.window.close),
            name="GuiShutdown",
            daemon=True,
        ).start()
        return True

    def set_transfer_mode(self, mode):
        return self._invoke_on_main_thread(self._set_transfer_mode_impl, mode)

    def _set_transfer_mode_impl(self, mode):
        if not self.driver.is_connected():
            raise RuntimeError("Driver is not connected.")

        mapping = {
            "off": 0x01,
            "1": 0x01,
            "on": 0x02,
            "2": 0x02,
        }

        if isinstance(mode, str):
            key = mode.strip().lower()
            if key not in mapping:
                raise ValueError(f"Invalid transfer mode: {mode}")
            mode_value = mapping[key]
        elif isinstance(mode, int):
            mode_value = mode
        else:
            raise ValueError(f"Invalid transfer mode type: {type(mode).__name__}")

        return self.driver.set_transfer_mode(mode_value)

    def get_sensor_type(self, board):
        return self._invoke_on_main_thread(self._get_sensor_type_impl, board)

    def _get_sensor_type_impl(self, board):
        board_kind = self.parse_board(board)
        self.ensure_board_connected(board_kind)
        return self.driver.get_sensor_type(board_kind)

    def get_status(self, board, channel):
        return self._invoke_on_main_thread(self._get_status_impl, board, channel)

    def _get_status_impl(self, board, channel):
        ch = self.resolve_channel(board, channel)
        result, status_data = self.driver.get_status(ch)
        sensor_status = self.driver.get_sensor_status(ch)
        self._last_error = None if result == ResultKind.ok else result.name
        return result, status_data, sensor_status

    def write_reg(self, board, channel, page, data):
        return self._invoke_on_main_thread(self._write_reg_impl, board, channel, page, data)

    def _write_reg_impl(self, board, channel, page, data):
        ch = self.resolve_channel(board, channel)
        result = self.driver.write_reg(ch, int(page), list(data))
        self._last_error = None if result == ResultKind.ok else result.name
        return result

    def read_reg_page(self, board, channel, page):
        return self._invoke_on_main_thread(self._read_reg_page_impl, board, channel, page)

    def _read_reg_page_impl(self, board, channel, page):
        ch = self.resolve_channel(board, channel)
        result, reg_data = self.driver.read_reg_page(ch, int(page))
        self._last_error = None if result == ResultKind.ok else result.name
        return result, list(reg_data)

    def set_rom(self, board, channel):
        return self._invoke_on_main_thread(self._set_rom_impl, board, channel)

    def _set_rom_impl(self, board, channel):
        ch = self.resolve_channel(board, channel)
        result = self.driver.set_rom(ch)
        self._last_error = None if result == ResultKind.ok else result.name
        return result

    def read_reg(self, board, channel, page, addresses):
        return self._invoke_on_main_thread(self._read_reg_impl, board, channel, page, addresses)

    def _read_reg_impl(self, board, channel, page, addresses):
        ch = self.resolve_channel(board, channel)
        result, reg_data = self.driver.read_reg(ch, int(page), list(addresses))
        self._last_error = None if result == ResultKind.ok else result.name
        return result, list(reg_data)

    def get_network_address(self, board, network_type):
        return self._invoke_on_main_thread(self._get_network_address_impl, board, network_type)

    def _get_network_address_impl(self, board, network_type):
        board_kind = self.parse_board(board)
        self.ensure_board_connected(board_kind)
        network_type_value = self.parse_network_type(network_type)
        return self.driver.get_network_address(board_kind, network_type_value)

    def set_network_address(self, board, network_type, address):
        return self._invoke_on_main_thread(self._set_network_address_impl, board, network_type, address)

    def _set_network_address_impl(self, board, network_type, address):
        board_kind = self.parse_board(board)
        self.ensure_board_connected(board_kind)
        network_type_value = self.parse_network_type(network_type)
        parsed_address = self.parse_network_address(network_type_value, address)
        result, response = self.driver.set_network_address(board_kind, network_type_value, parsed_address)
        self._last_error = None if result == ResultKind.ok else result.name
        return result, response

    def get_sampling_count(self):
        return self._invoke_on_main_thread(self._get_sampling_count_impl)

    def _get_sampling_count_impl(self):
        self.ensure_connected()
        try:
            result = self.driver.get_sampling_count()
        except NotImplementedError as exc:
            raise NotImplementedError(
                f"{type(self.driver).__name__}.get_sampling_count is not implemented."
            ) from exc
        if not isinstance(result, tuple) or len(result) != 2:
            raise NotImplementedError(f"{type(self.driver).__name__}.get_sampling_count is not implemented.")
        status, count = result
        self._last_error = None if status == ResultKind.ok else status.name
        return status, count

    def get_sampling_data(self):
        return self._invoke_on_main_thread(self._get_sampling_data_impl)

    def _get_sampling_data_impl(self):
        self.ensure_connected()
        try:
            result = self.driver.get_sampling_data()
        except NotImplementedError as exc:
            raise NotImplementedError(
                f"{type(self.driver).__name__}.get_sampling_data is not implemented."
            ) from exc
        if not isinstance(result, tuple) or len(result) != 2:
            raise NotImplementedError(f"{type(self.driver).__name__}.get_sampling_data is not implemented.")
        status, value = result
        self._last_error = None if status == ResultKind.ok else status.name
        return status, value

    def offset_calibration(self, board, channel, ex_temp=0.0, ex_temp_enable=False):
        return self._invoke_on_main_thread(
            self._offset_calibration_impl,
            board,
            channel,
            ex_temp,
            ex_temp_enable,
        )

    def _offset_calibration_impl(self, board, channel, ex_temp, ex_temp_enable):
        ch = self.resolve_channel(board, channel)
        result = self.driver.offset_calibration(ch, float(ex_temp), bool(ex_temp_enable))
        self._last_error = None if result == ResultKind.ok else result.name
        return result

    def temp_calibration(self, board, channel, ex_temp=0.0, ex_temp_enable=False):
        return self._invoke_on_main_thread(
            self._temp_calibration_impl,
            board,
            channel,
            ex_temp,
            ex_temp_enable,
        )

    def _temp_calibration_impl(self, board, channel, ex_temp, ex_temp_enable):
        ch = self.resolve_channel(board, channel)
        result = self.driver.temp_calibration(ch, float(ex_temp), bool(ex_temp_enable))
        self._last_error = None if result == ResultKind.ok else result.name
        return result

    def ensure_board_connected(self, board: BoardKind):
        self.ensure_connected()
        if not self.driver.get_board_connection_status(board):
            raise RuntimeError(f"{board.name} is not connected.")

    def ensure_connected(self):
        if not self.driver.is_connected():
            raise RuntimeError("Driver is not connected.")

    def resolve_channel(self, board, channel) -> int:
        board_kind = self.parse_board(board)
        self.ensure_board_connected(board_kind)
        channel_index = self.parse_sensor_channel(channel)
        return self.driver.get_ch(board_kind, channel_index)

    def parse_board(self, board) -> BoardKind:
        if isinstance(board, BoardKind):
            if board == BoardKind.board_num:
                raise ValueError("board_num cannot be used here.")
            return board

        if isinstance(board, int):
            mapping = {
                1: BoardKind.board1,
                2: BoardKind.board2,
            }
            if board in mapping:
                return mapping[board]

        if isinstance(board, str):
            key = board.strip().lower()
            mapping = {
                "1": BoardKind.board1,
                "board1": BoardKind.board1,
                "b1": BoardKind.board1,
                "2": BoardKind.board2,
                "board2": BoardKind.board2,
                "b2": BoardKind.board2,
            }
            if key in mapping:
                return mapping[key]

        raise ValueError(f"Invalid board: {board}")

    def parse_sensor_channel(self, channel) -> int:
        if isinstance(channel, int):
            mapping = {
                1: 0,
                2: 1,
            }
            if channel in mapping:
                return mapping[channel]

        if isinstance(channel, str):
            key = channel.strip().lower()
            mapping = {
                "1": 0,
                "ch1": 0,
                "c1": 0,
                "sensor1": 0,
                "2": 1,
                "ch2": 1,
                "c2": 1,
                "sensor2": 1,
            }
            if key in mapping:
                return mapping[key]

        raise ValueError(f"Invalid sensor channel: {channel}")

    def parse_int(self, value, label: str) -> int:
        try:
            return int(str(value), 0)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid {label}: {value}") from exc

    def parse_page(self, page) -> int:
        value = self.parse_int(page, "page")
        if not self.driver.PAGE_LOWER_LIMIT <= value <= self.driver.PAGE_UPPER_LIMIT:
            raise ValueError(f"Invalid page: {page}")
        return value

    def parse_register_address(self, address) -> int:
        value = self.parse_int(address, "register address")
        if not self.driver.ADDR_LOWER_LIMIT <= value <= self.driver.ADDR_UPPER_LIMIT:
            raise ValueError(f"Invalid register address: {address}")
        return value

    def parse_register_data(self, tokens: list[str]) -> list[RegData]:
        if not tokens:
            raise ValueError("At least one register pair is required.")

        reg_data = []
        for token in tokens:
            delimiter = ":" if ":" in token else "=" if "=" in token else None
            if delimiter is None:
                raise ValueError(f"Invalid register pair: {token}")
            addr_text, data_text = token.split(delimiter, 1)
            reg_data.append(
                RegData(
                    addr=self.parse_register_address(addr_text),
                    data=self.parse_int(data_text, "register data"),
                )
            )
        return reg_data

    def parse_register_addresses(self, tokens: list[str]) -> list[int]:
        if not tokens:
            raise ValueError("At least one register address is required.")
        return [self.parse_register_address(token) for token in tokens]

    def parse_optional_temperature(self, args: list[str]) -> tuple[float, bool]:
        if not args:
            return 0.0, False
        if len(args) != 1:
            raise ValueError("Only one external temperature can be specified.")
        try:
            return float(args[0]), True
        except ValueError as exc:
            raise ValueError(f"Invalid external temperature: {args[0]}") from exc

    def parse_network_type(self, network_type) -> int:
        if isinstance(network_type, int):
            if network_type in (
                self.driver.NETWORK_ADDR_TYPE_IP,
                self.driver.NETWORK_ADDR_TYPE_SUBNET_MASK,
                self.driver.NETWORK_ADDR_TYPE_GATEWAY,
                self.driver.NETWORK_ADDR_TYPE_MAC,
            ):
                return network_type
        elif isinstance(network_type, str):
            key = network_type.strip().lower()
            mapping = {
                "1": self.driver.NETWORK_ADDR_TYPE_IP,
                "ip": self.driver.NETWORK_ADDR_TYPE_IP,
                "2": self.driver.NETWORK_ADDR_TYPE_SUBNET_MASK,
                "subnet": self.driver.NETWORK_ADDR_TYPE_SUBNET_MASK,
                "subnet_mask": self.driver.NETWORK_ADDR_TYPE_SUBNET_MASK,
                "mask": self.driver.NETWORK_ADDR_TYPE_SUBNET_MASK,
                "3": self.driver.NETWORK_ADDR_TYPE_GATEWAY,
                "gateway": self.driver.NETWORK_ADDR_TYPE_GATEWAY,
                "4": self.driver.NETWORK_ADDR_TYPE_MAC,
                "mac": self.driver.NETWORK_ADDR_TYPE_MAC,
            }
            if key in mapping:
                return mapping[key]

        raise ValueError(f"Invalid network type: {network_type}")

    def parse_network_address(self, network_type: int, address) -> bytearray:
        expected_size = self.driver.get_network_address_size(network_type)
        if expected_size == 0:
            raise ValueError(f"Unsupported network type: {network_type}")

        if isinstance(address, str):
            if network_type == self.driver.NETWORK_ADDR_TYPE_MAC:
                normalized = address.replace(":", "").replace("-", "").replace(".", "")
                if len(normalized) != 12:
                    raise ValueError(f"Invalid MAC address: {address}")
                try:
                    parsed = bytearray(bytes.fromhex(normalized))
                except ValueError as exc:
                    raise ValueError(f"Invalid MAC address: {address}") from exc
            else:
                try:
                    parsed = bytearray(ipaddress.IPv4Address(address).packed)
                except ipaddress.AddressValueError as exc:
                    raise ValueError(f"Invalid IPv4 address: {address}") from exc
        else:
            try:
                parsed = bytearray(address)
            except TypeError as exc:
                raise ValueError(f"Invalid address type: {type(address).__name__}") from exc

        if len(parsed) != expected_size:
            raise ValueError(f"Invalid address length: expected {expected_size} bytes, got {len(parsed)}")

        return parsed

    def format_sensor_type(self, sensor_type: int) -> str:
        mapping = {
            self.driver.SENSOR_TYPE_INVALID: "INVALID(0x00)",
            self.driver.SENSOR_TYPE_SR300: "SR300(0x03)",
            self.driver.SENSOR_TYPE_SR500: "SR500(0x05)",
        }
        return mapping.get(sensor_type, f"UNKNOWN(0x{sensor_type:02X})")

    def format_error_status(self, status) -> str:
        if hasattr(status, "name"):
            return status.name
        return str(status)

    def format_connection_status(self, connection_status) -> str:
        if hasattr(connection_status, "name"):
            return connection_status.name
        return str(connection_status)

    def format_version_value(self, version_value: int) -> str:
        if not version_value:
            return "-"
        components = [
            (version_value >> 24) & 0xFF,
            (version_value >> 16) & 0xFF,
            (version_value >> 8) & 0xFF,
            version_value & 0xFF,
        ]
        return f"{'.'.join(map(str, components))}(0x{version_value:08X})"

    def format_register_data(self, reg_data: list[RegData]) -> str:
        if not reg_data:
            return "[]"
        return "[" + ", ".join(
            f"0x{reg.addr:02X}=0x{(reg.data & 0xFFFF):04X}" for reg in reg_data
        ) + "]"

    def format_network_address(self, network_type: int, address: bytearray | bytes | list[int]) -> str:
        data = bytearray(address)
        if network_type == self.driver.NETWORK_ADDR_TYPE_MAC:
            return ":".join(f"{byte:02X}" for byte in data)
        return ".".join(str(byte) for byte in data)
