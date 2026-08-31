import argparse
import signal


def _install_signal_handlers(controller):
    def _handle_signal(signum, _frame):
        print(f"Received signal {signum}. Shutting down.", flush=True)
        controller.shutdown()

    for name in ("SIGINT", "SIGTERM"):
        sig = getattr(signal, name, None)
        if sig is None:
            continue
        signal.signal(sig, _handle_signal)


def main():
    from Controllers.HeadlessController import HeadlessController

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        "--console",
        "--cui",
        dest="enable_console",
        action="store_true",
        help="Enable the stdin console while the headless controller is running.",
    )
    parser.add_argument(
        "--app-control-host",
        default="127.0.0.1",
        help="Host for the app control server.",
    )
    parser.add_argument(
        "--app-control-port",
        type=int,
        default=18765,
        help="Port for the app control server.",
    )
    parser.add_argument(
        "--poll-interval-ms",
        type=int,
        default=500,
        help="Polling interval for status refresh.",
    )
    args = parser.parse_args()

    controller = HeadlessController(
        enable_console=args.enable_console,
        host=args.app_control_host,
        port=args.app_control_port,
        poll_interval_ms=args.poll_interval_ms,
    )
    controller.start()
    _install_signal_handlers(controller)
    controller.wait_forever()


if __name__ == "__main__":
    main()
