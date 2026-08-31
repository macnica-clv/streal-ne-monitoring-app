import serial.tools.list_ports

def get_com_port_list(vid=None, pid=None):
    """
    指定のVID/PIDのみのCOMリストを返す
    vid/pidは16進数（例: 0x1234）で指定
    """
    com_list = []
    for port in serial.tools.list_ports.comports():
        # ポートのVID/PID取得
        if vid is not None and pid is not None:
            # Noneチェックは、デバイスによってはNoneになる場合あり
            if port.vid is not None and port.pid is not None:
                if port.vid == vid and port.pid == pid:
                    com_list.append(port.device)
        elif vid is not None:
            if port.vid is not None:
                if port.vid == vid:
                    com_list.append(port.device)
        else:
            # 絞り込みなしで全部
            com_list.append(port.device)
    return com_list

