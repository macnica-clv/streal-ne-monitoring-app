import os, sys

from PySide6.QtCore import QStandardPaths


def rel_to_abs(filepath: str) -> str:
    """
    外部ファイルへの相対パスを絶対パスに直す
    :param filepath: ファイルへの相対パス
    :return: ファイルへの絶対パス
    """
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
            if sys.platform == 'Darwin' and '.app' in base_path:
                os.path.abspath(os.path.join(base_path, '../../..'))
        else:
            current_path = os.path.dirname(os.path.abspath(__file__))
            base_path = os.path.abspath(os.path.join(current_path, '..'))

    return os.path.join(base_path, filepath)

def get_config_path(filepath: str) -> str:
    """
    ユーザーの設定ファイル保存用ディレクトリを取得
    """
    app_data_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    if not os.path.exists(app_data_dir):
        os.makedirs(app_data_dir)

    return os.path.join(app_data_dir, filepath)