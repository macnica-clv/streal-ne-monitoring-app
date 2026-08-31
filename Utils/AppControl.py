import json
import os
import socket
import socketserver
import threading


APP_CONTROL_HOST = os.environ.get("HIZMIL_APP_CONTROL_HOST", "127.0.0.1")
APP_CONTROL_PORT = int(os.environ.get("HIZMIL_APP_CONTROL_PORT", "18765"))
APP_CONTROL_TIMEOUT_SEC = float(os.environ.get("HIZMIL_APP_CONTROL_TIMEOUT_SEC", "3.0"))

_active_command_controller = globals().get("_active_command_controller")


class AppControlError(RuntimeError):
    pass


def _deserialize_connection_status(result_name: str):
    from Models.Hizmil_Driver import ConnectionStatus

    return ConnectionStatus[result_name]


def register_command_controller(controller):
    global _active_command_controller
    _active_command_controller = controller


def unregister_command_controller(controller=None):
    global _active_command_controller
    if controller is None or _active_command_controller is controller:
        _active_command_controller = None


def get_active_command_controller():
    return _active_command_controller


def _serialize_result_kind(result):
    return result.name if hasattr(result, "name") else str(result)


def _deserialize_result_kind(result_name: str):
    from Models.Hizmil_Driver import ResultKind

    return ResultKind[result_name]


def _normalize_json_value(value):
    if hasattr(value, "name"):
        return value.name
    if isinstance(value, (bytes, bytearray)):
        return list(value)
    return value


def _json_safe(value):
    if isinstance(value, dict):
        return {key: _json_safe(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if hasattr(value, "name"):
        return value.name
    if isinstance(value, (bytes, bytearray)):
        return list(value)
    return value


def _dispatch_request(request: dict, controller=None) -> dict:
    command = request.get("command")
    if command == "ping":
        return {"ok": True, "result": "pong"}

    if controller is None:
        controller = get_active_command_controller()
    if controller is None:
        return {"ok": False, "error": "CUI control is not initialized."}

    if command == "connect":
        if not hasattr(controller, "connect"):
            return {"ok": False, "error": "The active controller does not support connect."}
        try:
            result = controller.connect(
                request.get("method"),
                request.get("targets"),
            )
            status = controller.get_app_status() if hasattr(controller, "get_app_status") else None
        except Exception as exc:
            return {"ok": False, "error": str(exc)}
        return {"ok": True, "result": {"result": _serialize_result_kind(result), "status": _json_safe(status)}}

    if command == "disconnect":
        if not hasattr(controller, "disconnect"):
            return {"ok": False, "error": "The active controller does not support disconnect."}
        try:
            result = controller.disconnect()
            status = controller.get_app_status() if hasattr(controller, "get_app_status") else None
        except Exception as exc:
            return {"ok": False, "error": str(exc)}
        return {"ok": True, "result": {"result": result, "status": _json_safe(status)}}

    if command == "start_measure":
        if not hasattr(controller, "start_measure"):
            return {"ok": False, "error": "The active controller does not support start_measure."}
        try:
            result = controller.start_measure(
                interval=request.get("interval"),
                sampling_rate=request.get("sampling_rate"),
                sampling_unit=request.get("sampling_unit"),
                mode=request.get("mode", "all"),
            )
            status = controller.get_app_status() if hasattr(controller, "get_app_status") else None
        except Exception as exc:
            return {"ok": False, "error": str(exc)}
        return {"ok": True, "result": {"result": _serialize_result_kind(result), "status": _json_safe(status)}}

    if command == "stop_measure":
        if not hasattr(controller, "stop_measure"):
            return {"ok": False, "error": "The active controller does not support stop_measure."}
        try:
            result = controller.stop_measure()
            status = controller.get_app_status() if hasattr(controller, "get_app_status") else None
        except Exception as exc:
            return {"ok": False, "error": str(exc)}
        return {"ok": True, "result": {"result": _serialize_result_kind(result), "status": _json_safe(status)}}

    if command == "get_app_status":
        if not hasattr(controller, "get_app_status"):
            return {"ok": False, "error": "The active controller does not support get_app_status."}
        try:
            result = controller.get_app_status()
        except Exception as exc:
            return {"ok": False, "error": str(exc)}
        return {"ok": True, "result": _json_safe(result)}

    if command == "shutdown_app":
        if not hasattr(controller, "shutdown_app"):
            return {"ok": False, "error": "The active controller does not support shutdown_app."}
        try:
            result = controller.shutdown_app()
        except Exception as exc:
            return {"ok": False, "error": str(exc)}
        return {"ok": True, "result": result}

    if command == "set_transfer_mode":
        try:
            result = controller.set_transfer_mode(request.get("mode"))
        except Exception as exc:
            return {"ok": False, "error": str(exc)}
        return {"ok": True, "result": str(result)}

    if command == "get_sensor_type":
        try:
            result, ch1_type, ch2_type = controller.get_sensor_type(request.get("board"))
        except Exception as exc:
            return {"ok": False, "error": str(exc)}
        return {
            "ok": True,
            "result": {
                "result": _serialize_result_kind(result),
                "ch1_type": ch1_type,
                "ch2_type": ch2_type,
            },
        }

    if command == "get_network_address":
        try:
            result, address = controller.get_network_address(
                request.get("board"),
                request.get("network_type"),
            )
        except Exception as exc:
            return {"ok": False, "error": str(exc)}
        return {
            "ok": True,
            "result": {
                "result": _serialize_result_kind(result),
                "address": list(address),
            },
        }

    if command == "set_network_address":
        try:
            result, address = controller.set_network_address(
                request.get("board"),
                request.get("network_type"),
                request.get("address"),
            )
        except Exception as exc:
            return {"ok": False, "error": str(exc)}
        return {
            "ok": True,
            "result": {
                "result": _serialize_result_kind(result),
                "address": list(address),
            },
        }

    return {"ok": False, "error": f"Unknown command: {command}"}


class _AppControlTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def dispatch(self, request: dict) -> dict:
        return _dispatch_request(request)


class _AppControlRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        raw = self.rfile.readline()
        if not raw:
            return

        try:
            request = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            response = {"ok": False, "error": f"Invalid JSON: {exc}"}
        else:
            response = self.server.dispatch(request)

        self.wfile.write((json.dumps(response) + "\n").encode("utf-8"))


class AppControlServer:
    def __init__(self, host: str = APP_CONTROL_HOST, port: int = APP_CONTROL_PORT):
        self.host = host
        self.port = port
        self._server = None
        self._thread = None

    def start(self):
        if self._server is not None:
            return True

        try:
            self._server = _AppControlTCPServer((self.host, self.port), _AppControlRequestHandler)
        except OSError as exc:
            print(f"App control server start failed: {exc}", flush=True)
            self._server = None
            return False

        self._thread = threading.Thread(
            target=self._server.serve_forever,
            name="AppControlServer",
            daemon=True,
        )
        self._thread.start()
        return True

    def stop(self):
        if self._server is None:
            return

        self._server.shutdown()
        self._server.server_close()
        self._server = None
        self._thread = None


def _send_request(command: str, **payload):
    request = {"command": command, **payload}
    controller = get_active_command_controller()
    if controller is not None:
        response = _dispatch_request(request, controller=controller)
        if not response.get("ok"):
            raise AppControlError(response.get("error", "Unknown app control error."))
        return response.get("result")

    try:
        with socket.create_connection((APP_CONTROL_HOST, APP_CONTROL_PORT), timeout=APP_CONTROL_TIMEOUT_SEC) as sock:
            sock.sendall((json.dumps(request) + "\n").encode("utf-8"))
            buffer = b""
            while not buffer.endswith(b"\n"):
                chunk = sock.recv(4096)
                if not chunk:
                    break
                buffer += chunk
    except OSError as exc:
        raise AppControlError(
            f"Could not connect to Hiz-mil app control server at {APP_CONTROL_HOST}:{APP_CONTROL_PORT}: {exc}"
        ) from exc

    if not buffer:
        raise AppControlError("No response from Hiz-mil app control server.")

    response = json.loads(buffer.decode("utf-8"))
    if not response.get("ok"):
        raise AppControlError(response.get("error", "Unknown app control error."))

    return response.get("result")


def ping():
    # Added for Python Console use: confirms the app control endpoint is reachable.
    # Python Console 用に追加。アプリ制御エンドポイントへ疎通できるか確認する。
    return _send_request("ping")


def configure_app_control(host=None, port=None, timeout_sec=None):
    global APP_CONTROL_HOST, APP_CONTROL_PORT, APP_CONTROL_TIMEOUT_SEC

    if host is not None:
        APP_CONTROL_HOST = str(host)
    if port is not None:
        APP_CONTROL_PORT = int(port)
    if timeout_sec is not None:
        APP_CONTROL_TIMEOUT_SEC = float(timeout_sec)


def connect(method, targets):
    if isinstance(targets, str):
        normalized_targets = [targets]
    elif targets is None:
        normalized_targets = []
    else:
        normalized_targets = list(targets)
    response = _send_request("connect", method=_normalize_json_value(method), targets=normalized_targets)
    return _deserialize_connection_status(response["result"]), response["status"]


def disconnect():
    response = _send_request("disconnect")
    return response["result"], response["status"]


def start_measure(interval=None, sampling_rate=None, sampling_unit=None, mode="all"):
    payload = {"mode": mode}
    if interval is not None:
        payload["interval"] = interval
    if sampling_rate is not None:
        payload["sampling_rate"] = sampling_rate
    if sampling_unit is not None:
        payload["sampling_unit"] = sampling_unit
    response = _send_request("start_measure", **payload)
    return _deserialize_result_kind(response["result"]), response["status"]


def stop_measure():
    response = _send_request("stop_measure")
    return _deserialize_result_kind(response["result"]), response["status"]


def get_app_status():
    return _send_request("get_app_status")


def shutdown_app():
    return _send_request("shutdown_app")


def set_transfer_mode(mode):
    return _send_request("set_transfer_mode", mode=mode)


def get_sensor_type(board):
    response = _send_request("get_sensor_type", board=_normalize_json_value(board))
    return (
        _deserialize_result_kind(response["result"]),
        response["ch1_type"],
        response["ch2_type"],
    )


def get_network_address(board, network_type):
    response = _send_request(
        "get_network_address",
        board=_normalize_json_value(board),
        network_type=_normalize_json_value(network_type),
    )
    return _deserialize_result_kind(response["result"]), bytearray(response["address"])


def set_network_address(board, network_type, address):
    response = _send_request(
        "set_network_address",
        board=_normalize_json_value(board),
        network_type=_normalize_json_value(network_type),
        address=_normalize_json_value(address),
    )
    return _deserialize_result_kind(response["result"]), bytearray(response["address"])


def transfer_mode_on():
    return set_transfer_mode("on")


def transfer_mode_off():
    return set_transfer_mode("off")
