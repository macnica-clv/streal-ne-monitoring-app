import builtins


_INSTALLED = False


def install():
    global _INSTALLED
    if _INSTALLED:
        return

    from Utils.AppControl import (
        get_network_address,
        get_sensor_type,
        ping,
        set_network_address,
        set_transfer_mode,
        transfer_mode_off,
        transfer_mode_on,
    )

    # Legacy-safe names exposed to the Python Console for manual app control.
    # Python Console から手動操作するための、互換性を意識した名前。
    builtins.hizmil_ping = ping
    builtins.hizmil_set_transfer_mode = set_transfer_mode
    builtins.hizmil_get_sensor_type = get_sensor_type
    builtins.hizmil_get_network_address = get_network_address
    builtins.hizmil_set_network_address = set_network_address
    builtins.hizmil_transfer_mode_on = transfer_mode_on
    builtins.hizmil_transfer_mode_off = transfer_mode_off

    # Convenience aliases added in this change; `ping_hizmil()` is just a connectivity check.
    # 今回追加した簡易エイリアス。`ping_hizmil()` は疎通確認専用。
    builtins.ping_hizmil = ping
    builtins.set_transfer_mode = set_transfer_mode
    builtins.get_sensor_type = get_sensor_type
    builtins.get_network_address = get_network_address
    builtins.set_network_address = set_network_address
    builtins.transfer_mode_on = transfer_mode_on
    builtins.transfer_mode_off = transfer_mode_off

    _INSTALLED = True


install()
