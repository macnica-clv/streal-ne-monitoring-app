import subprocess
import os
import glob

def smart_update():
    project_root = os.getcwd()
    ts_file = "./Lang/lang_jp.ts"
    
    # 全ファイルを収集
    extensions = ("**/*.py", "**/*.ui", "**/*.qml")
    all_files = [f for ext in extensions for f in glob.glob(ext, recursive=True)]
    
    # tr() や .ui ファイルなど、翻訳対象が含まれる可能性のあるファイルだけを抽出
    valid_files = []
    for f in all_files:
        if f.endswith('.ui') or f.endswith('.qml'):
            valid_files.append(f"./{f.replace(os.sep, '/')}")
        else:
            # .pyファイルの中身をチェック
            with open(f, 'r', encoding='utf-8', errors='ignore') as content:
                if 'tr(' in content.read():
                    valid_files.append(f"./{f.replace(os.sep, '/')}")

    if not valid_files:
        print("翻訳対象となるキーワードを含むファイルが見つかりませんでした。")
        return

    # リストファイルを作成
    with open("valid_files.lst", "w", encoding="utf-8") as lst:
        lst.write("\n".join(valid_files))

    # 一括実行
    print(f"有効な {len(valid_files)} ファイルを抽出対象にします...")
    command = ["pyside6-lupdate", "-no-obsolete", "@valid_files.lst", "-ts", ts_file]
    
    result = subprocess.run(command, capture_output=True, text=True, encoding='cp932', errors='replace')
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)

if __name__ == "__main__":
    smart_update()