import argparse
import signal
import sys, os

# if getattr(sys, 'frozen', False):
#     os.environ['DYLD_FRAMEWORK_PATH'] = os.path.join(os.path.dirname(sys.executable), '..', 'Frameworks')
#     os.environ['DYLD_LIBRARY_PATH'] = os.path.join(os.path.dirname(sys.executable), '..', 'Frameworks')

# TBD：Poetry, requirement.txtで代用できないか調べる
sys.path.append("./Views")


def _install_signal_handlers(controller):
    def _handle_signal(signum, _frame):
        print(f"Received signal {signum}. Shutting down.", flush=True)
        controller.shutdown()

    for name in ("SIGINT", "SIGTERM"):
        sig = getattr(signal, name, None)
        if sig is None:
            continue
        signal.signal(sig, _handle_signal)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        "--console",
        "--cui",
        dest="enable_console",
        action="store_true",
        help="Enable console commands while the GUI is running.",
    )
    parser.add_argument(
        "--headless",
        dest="enable_headless",
        action="store_true",
        help="Run without importing the GUI stack.",
    )
    parser.add_argument(
        "--app-control-host",
        default="127.0.0.1",
        help="Host for the app control server in headless mode.",
    )
    parser.add_argument(
        "--app-control-port",
        type=int,
        default=18765,
        help="Port for the app control server in headless mode.",
    )
    parser.add_argument(
        "--poll-interval-ms",
        type=int,
        default=500,
        help="Polling interval for status refresh in headless mode.",
    )
    args, remaining = parser.parse_known_args()
    sys.argv = [sys.argv[0], *remaining]

    if args.enable_headless:
        from Controllers.HeadlessController import HeadlessController

        controller = HeadlessController(
            enable_console=args.enable_console,
            host=args.app_control_host,
            port=args.app_control_port,
            poll_interval_ms=args.poll_interval_ms,
        )
        controller.start()
        _install_signal_handlers(controller)
        controller.wait_forever()
    else:
        from Controllers.MainController import MainController

        main_ctrl = MainController(enable_console=args.enable_console)

