# Hiz-mil UI 開発ガイド

## 目的

このドキュメントは、Hiz-mil の画面（`.ui` ファイル）を編集する開発者向けの手順書です。Qt Designer での編集から、Python コードへの変換、リソースと翻訳の再生成までを扱います。

アプリケーションを動かすだけであれば、この手順は不要です。`Readme.md` の環境構築のみで動作します。

## 1. ツール環境の準備

### なぜ実行環境と分けるのか

`environment.yml` で作る `Hiz-mil` 環境には、Qt Designer が入っていません。conda-forge の `pyside6` パッケージが同梱している実行ファイルは 2 つだけです。

| 環境 | 含まれる Qt ツール |
|---|---|
| `Hiz-mil`（実行環境） | `pyside6-uic`, `pyside6-rcc` |
| `qt-tools`（ツール環境） | 上記に加えて `pyside6-designer`, `pyside6-lupdate`, `pyside6-lrelease`, `pyside6-linguist` ほか |

Qt Designer や `pyside6-lupdate` は PyPI 版の `pyside6-essentials` にのみ含まれます。このパッケージは conda-forge には存在しないため、`environment.yml` に追記することはできません。

`pip:` セクションで PyPI 版を `Hiz-mil` 環境に混ぜることも避けてください。conda 版と PyPI 版は同じ `site-packages/PySide6/` に展開され、Qt 本体の持ち方も異なる（conda 版は `Library/bin/`、PyPI 版は wheel 同梱）ため、片方がもう片方を上書きして壊れます。

### 作成手順

```bash
conda create -n qt-tools python=3.12 -y
conda activate qt-tools
pip install "pyside6-essentials>=6.5,<7"
```

`environment.yml` の `pyside6` と同じメジャーバージョンに揃えてください。生成コードのヘッダにツールのバージョンが埋め込まれるため、バージョンがずれると無関係な差分が発生します。

実行ファイルの絶対パスは次のコマンドで確認できます。PyCharm の外部ツール登録に使います。

```bash
conda activate qt-tools
python -c "import shutil; print(shutil.which('pyside6-designer'))"
```

| OS | 一般的なパス |
|---|---|
| Windows | `<Miniforge3>\envs\qt-tools\Scripts\pyside6-designer.exe` |
| macOS / Linux | `<Miniforge3>/envs/qt-tools/bin/pyside6-designer` |

## 2. ファイルの対応関係

`.ui` から生成される Python ファイルの出力先は 2 系統あります。**変換時はこの表を確認してください。**

| `.ui`（編集対象） | 生成先（自動生成・直接編集禁止） |
|---|---|
| `UI/Chart_Page.ui` | `Views/Chart_Page.py` |
| `UI/Home_Page.ui` | `Views/Home_Page.py` |
| `UI/Main_Window.ui` | `Views/Main_Window.py` |
| `UI/Register_Page.ui` | `Views/UI/Register_Page.py` |
| `UI/Register_Page_SR300.ui` | `Views/UI/Register_Page_SR300.py` |
| `UI/Setting_Page.ui` | `Views/UI/Setting_Page.py` |
| `UI/Setting_Tab/Color_Setting.ui` | `Views/UI/Color_Setting.py` |
| `UI/Setting_Tab/Language_Setting.ui` | `Views/UI/Language_Setting.py` |
| `UI/Setting_Tab/Log_Setting.ui` | `Views/UI/Log_Setting.py` |
| `UI/Setting_Tab/Shortcut_Setting.ui` | `Views/UI/Shortcut_Setting.py` |
| `UI/Setting_Tab/network_setting.ui` | `Views/UI/network_setting.py` |
| `UI/Setting_Tab/version.ui` | `Views/UI/version.py` |

`Setting_Tab/` 配下の `.ui` は、生成先ではディレクトリ階層が畳まれて `Views/UI/` 直下に出力される点に注意してください。

## 3. 作業の流れ

1. Qt Designer で `.ui` を編集して保存する
2. `pyside6-uic` で対応する `.py` に変換する（上の表の出力先へ）
3. アプリを起動して表示を確認する
4. 文言を追加・変更した場合は翻訳ファイルを更新する（第 6 節）

## 4. PyCharm 外部ツールの設定

`Settings` > `Tools` > `External Tools` > `+` で登録します。

外部ツールは IDE 全体の設定として保存され、`.idea/` には入らないためリポジトリでは共有できません。開発者ごとに登録が必要です。

共通の設定：

- `作業ディレクトリ` は必ず `$ProjectFileDir$` を使ってください。絶対パスを直接書くと他の開発者や他 OS で動作しません。
- `実行後にファイルを同期する` を ON にしてください。生成された `.py` を PyCharm が読み直します。

### 4-1. Qt Designer

| 項目 | 値 |
|---|---|
| 名前 | `Qt Designer` |
| プログラム | 第 1 節で確認した `pyside6-designer` のパス |
| 引数 | `$FilePath$` |
| 作業ディレクトリ | `$ProjectFileDir$` |
| 実行後にファイルを同期する | ON |
| ツール出力用のコンソールを開く | OFF |

登録後は `UI/*.ui` を右クリック > `External Tools` > `Qt Designer` で開けます。

### 4-2. ui_py Convert（`Views/UI/` 系）

第 2 節の表で生成先が `Views/UI/` になっている 9 ファイル用です。

| 項目 | 値 |
|---|---|
| 名前 | `ui_py Convert (Views/UI)` |
| プログラム | `<Miniforge3>\envs\qt-tools\Scripts\pyside6-uic.exe` |
| 引数 | `$FilePath$ -o Views/UI/$FileNameWithoutExtension$.py` |
| 作業ディレクトリ | `$ProjectFileDir$` |
| 実行後にファイルを同期する | ON |
| ツール出力用のコンソールを開く | ON（変換エラーを確認するため） |

### 4-3. ui_py Convert（`Views/` 系）

`Chart_Page.ui` / `Home_Page.ui` / `Main_Window.ui` の 3 ファイル用です。出力先が異なるため、別の外部ツールとして登録します。

| 項目 | 値 |
|---|---|
| 名前 | `ui_py Convert (Views)` |
| プログラム | `<Miniforge3>\envs\qt-tools\Scripts\pyside6-uic.exe` |
| 引数 | `$FilePath$ -o Views/$FileNameWithoutExtension$.py` |
| 作業ディレクトリ | `$ProjectFileDir$` |
| 実行後にファイルを同期する | ON |
| ツール出力用のコンソールを開く | ON |

`.ui` ごとにどちらを実行するかは第 2 節の表で確認してください。誤ったほうを実行すると、リポジトリに存在しないはずの場所に `.py` が生成されます。

## 5. コマンドラインで実行する場合

外部ツールを使わず、リポジトリのルートから直接実行することもできます。

```bash
conda activate qt-tools
```

```bash
pyside6-designer UI/Main_Window.ui
```

```bash
pyside6-uic UI/Main_Window.ui -o Views/Main_Window.py
pyside6-uic UI/Setting_Tab/version.ui -o Views/UI/version.py
```

## 6. リソースと翻訳の再生成

### リソース（画像・アイコン）

`Views/resources.qrc` に登録されている画像を追加・変更した場合に実行します。

```bash
pyside6-rcc Views/resources.qrc -o Views/resources_rc.py
```

`pyside6-rcc` は `Hiz-mil` 環境にも `qt-tools` 環境にも含まれています。

### 翻訳

`.ui` に文言を追加・変更した場合、翻訳カタログを更新します。リポジトリのルートで実行してください。

```bash
conda activate qt-tools
python update_ts.py
```

`update_ts.py` は内部で `pyside6-lupdate` を呼び出します。**このツールは `Hiz-mil` 環境には含まれていないため、必ず `qt-tools` 環境で実行してください。**

`Lang/lang_jp.ts` を Qt Linguist で翻訳したあと、`.qm` に変換します。

```bash
pyside6-lrelease Lang/lang_jp.ts -qm Lang/lang_jp.qm
```

## 7. 注意事項

- **生成された `.py` を直接編集しないでください。** 次の変換で上書きされます。第 2 節の表の右側にあるファイルがすべて該当します。
- 振る舞いを変更したい場合は、生成コードではなく `Views/*View.py` や `Controllers/*.py` を編集してください。
- SR300 と SR500 の両方に画面が存在する箇所があります。片方だけを変更しないよう注意してください。
- 変換後は必ずアプリを起動して表示を確認してください。`.ui` の編集内容によっては、生成コードの変数名が変わり、参照している側のコードが壊れることがあります。
