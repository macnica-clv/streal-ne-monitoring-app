# Monitoring Unit Application

作成者 / Author: Macnica,Inc

著作権 / Copyright: Copyright (c) Macnica,Inc. All rights reserved.

## 概要 / Overview

日本語:
モニタリングユニット NEシリーズと SR300 / SR500 センサの接続、設定、計測、可視化を行う PySide6 ベースのデスクトップアプリケーションです。USB / LAN 接続、リアルタイムチャート表示、レジスタ設定、ログ保存、テーマ・言語・ネットワーク設定に対応しています。

English:
This is a PySide6-based desktop application for connecting to Monitoring Unit NE Series devices and SR300 / SR500 sensors, configuring them, acquiring measurements, and visualizing data. It supports USB / LAN communication, real-time chart display, register configuration, log saving, and theme, language, and network settings.

## 主な機能 / Key Features

- USB / LAN 接続によるデバイス通信 / Device communication over USB / LAN
- SR300 / SR500 センサ対応 / Support for SR300 / SR500 sensors
- ひずみ・温度のリアルタイム表示 / Real-time strain and temperature visualization
- Moving Average、FFT などのチャート処理 / Chart processing such as moving average and FFT
- オートバランス、ズーム、レンジ調整、グラフキャプチャ / Auto balance, zoom, range adjustment, and graph capture
- レジスタの読み書き、ROM 反映、プリセット保存・読込 / Register read/write, ROM write, and preset save/load
- 測定ログの自動保存 / Automatic measurement log saving
- テーマ、ショートカット、言語、ネットワーク設定 / Theme, shortcut, language, and network settings
- マニュアル PDF の参照 / Access to the PDF manual

## 動作環境 / Requirements

| 項目 / Item | 内容 / Details |
| --- | --- |
| Python | 3.12（推奨 / recommended）。3.10 - 3.12 に対応 / supports 3.10 - 3.12（3.10 および 3.12 で動作確認済み / verified on 3.10 and 3.12） |
| OS | Windows / macOS / Linux |
| GUI 版 / GUI build | デスクトップ環境が必要 / Requires a desktop environment |
| ヘッドレス版 / Headless build | `pyserial` のみで動作 / Runs with `pyserial` only |
| 開発環境 / Development environment | マクニカでは **PyCharm + Miniforge3** を使用（他の IDE ・エディタ、venv / uv でも実行可能） / **PyCharm + Miniforge3** is used at Macnica (other IDEs, editors, venv, or uv also work) |
| ハードウェア / Hardware | 起動・画面確認のみであればデバイス不要 / A device is not required just to launch the app |

## セットアップと起動 / Setup and Launch

### 1. 環境構築 / Set up the environment

以下のいずれか 1 つの方法を選んでください。/ Choose **one** of the following methods.

日本語:
マクニカでは **PyCharm + Miniforge3（conda）** の組み合わせで開発環境を構築しています。同じ構成にする場合は **D. PyCharm** の手順をご参照ください。それ以外の環境でも A - C の方法でビルド・実行できます。

English:
At Macnica, the development environment is set up with **PyCharm + Miniforge3 (conda)**. To reproduce that setup, follow the steps in **D. PyCharm**. The application can also be built and run in other environments using methods A - C.

#### A. venv + pip（conda を使わない場合 / without conda）

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### B. uv

```bash
uv venv --python 3.12
uv pip install -r requirements.txt
```

以降のコマンドは `uv run python main.py` のように `uv run` を付けて実行してください。
Prefix the commands below with `uv run`, for example `uv run python main.py`.

#### C. conda / Miniforge3

日本語:
`environment.yml` は conda-forge チャネルを使用しています。Miniforge3 または Miniconda / Anaconda のプロンプトから実行してください。マクニカでは **Miniforge3** を使用しています。

English:
`environment.yml` uses the conda-forge channel. Run the commands from a Miniforge3 (or Miniconda / Anaconda) prompt. **Miniforge3** is the distribution used at Macnica.

```bash
conda env create -f environment.yml
conda activate Hiz-mil
```

ヘッドレス専用の環境を作る場合 / To create a headless-only environment:

```bash
conda env create -f environment_headless.yml
conda activate Hiz-mil-headless
```

> **社内プロキシ環境での注意 / Note for corporate proxy environments**
>
> TLS 検査プロキシの配下では、`conda env create` が次のエラーで失敗することがあります。
> Behind a TLS-inspecting proxy, `conda env create` may fail with:
>
> ```
> CondaSSLError: [SSL: CERTIFICATE_VERIFY_FAILED] self-signed certificate in certificate chain
> ```
>
> 外部ネットワークに直接接続できる回線で実行するか、社内 CA 証明書を conda に登録してください。
> Run the command on a network with direct internet access, or register your corporate CA bundle with conda:
>
> ```bash
> conda config --set ssl_verify /path/to/corporate-ca-bundle.pem
> ```

#### D. PyCharm（マクニカでの開発環境 / development environment used at Macnica）

日本語:
マクニカでは **PyCharm + Miniforge3** の組み合わせで開発環境を構築しています。

1. [Miniforge3](https://github.com/conda-forge/miniforge) をインストールします。
2. `File` > `Open` で clone したフォルダを開きます。
3. Miniforge Prompt（Windows）またはターミナルでリポジトリのルートに移動し、conda 環境を作成します。

   ```bash
   conda env create -f environment.yml
   ```

4. `Settings` > `Project: Hiz-mil` > `Python Interpreter` > `Add Interpreter` > `Add Local Interpreter` > `Conda Environment` を選びます。`Conda executable` に Miniforge3 の conda（例: `C:\Users\<user>\miniforge3\Scripts\conda.exe`）を指定し、`Use existing environment` で手順 3 で作成した `Hiz-mil` を選択します。
5. 本リポジトリには実行構成 `Hiz-mil`（GUI）と `Hiz-mil Headless`（ヘッドレス）が含まれており、PyCharm の実行構成一覧に自動的に表示されます。どちらもプロジェクトのインタープリタを使う設定なので、手順 4 を済ませていればそのまま実行できます。
6. 実行構成を新規に作る場合は、`Run` > `Edit Configurations` > `+` > `Python` で `Script path` に `main.py`、`Working directory` にリポジトリのルートを指定します。ヘッドレスで起動する場合は `Parameters` に `--headless` を入力します。

conda を使わず venv で構築する場合は、手順 3 - 4 の代わりに `Add Local Interpreter` > `Virtualenv Environment` の `New` で Python 3.12 を指定し、`requirements.txt` を開いたときに表示される `Install requirements` をクリックするか、PyCharm の Terminal で `pip install -r requirements.txt` を実行してください。

English:
At Macnica the development environment is built with **PyCharm + Miniforge3**.

1. Install [Miniforge3](https://github.com/conda-forge/miniforge).
2. Open the cloned folder via `File` > `Open`.
3. In the Miniforge Prompt (Windows) or a terminal, change to the repository root and create the conda environment:

   ```bash
   conda env create -f environment.yml
   ```

4. Go to `Settings` > `Project: Hiz-mil` > `Python Interpreter` > `Add Interpreter` > `Add Local Interpreter` > `Conda Environment`. Set `Conda executable` to the Miniforge3 conda (e.g. `C:\Users\<user>\miniforge3\Scripts\conda.exe`) and choose `Use existing environment` > `Hiz-mil`, created in step 3.
5. This repository ships the run configurations `Hiz-mil` (GUI) and `Hiz-mil Headless`, which PyCharm picks up automatically. Both use the project interpreter, so they run as-is once step 4 is complete.
6. To create a run configuration from scratch, use `Run` > `Edit Configurations` > `+` > `Python`, set `Script path` to `main.py` and `Working directory` to the repository root. Add `--headless` to `Parameters` to start in headless mode.

To use venv instead of conda, replace steps 3 - 4 with `Add Local Interpreter` > `Virtualenv Environment` > `New` using Python 3.12, then click `Install requirements` in the banner shown when opening `requirements.txt`, or run `pip install -r requirements.txt` in the PyCharm terminal.

### 2. 起動 / Launch

```bash
python main.py
```

起動オプション / Launch options:

| コマンド / Command | 説明 / Description |
| --- | --- |
| `python main.py` | GUI で起動 / Start the GUI |
| `python main.py --console` | GUI 起動中にコンソールコマンドを有効化 / Start the GUI with console commands enabled |
| `python main.py --headless` | GUI を読み込まずに起動 / Start without loading the GUI stack |
| `python main_headless.py` | ヘッドレス専用のエントリポイント / Headless-only entry point |

ヘッドレス起動時の追加オプション / Additional options for headless mode:

| オプション / Option | 既定値 / Default | 説明 / Description |
| --- | --- | --- |
| `--app-control-host` | `127.0.0.1` | アプリ制御サーバのホスト / Host of the app control server |
| `--app-control-port` | `18765` | アプリ制御サーバのポート / Port of the app control server |
| `--poll-interval-ms` | `500` | ステータス更新の間隔 (ms) / Status refresh interval in ms |

### 3. ヘッドレスのみを使う場合 / Headless-only installation

GUI を使わない場合は、より軽量な依存関係だけをインストールできます。
If you do not need the GUI, install the lighter dependency set instead.

```bash
pip install -r requirements-headless.txt
python main_headless.py
```

### 4. 動作確認 / Verifying the setup

構文チェック / Syntax check:

```bash
python -m compileall Controllers Models Utils Views main.py main_headless.py
```

ヘッドレス起動の疎通確認 / Headless connectivity check（別のターミナルで `python main.py --headless` を起動した状態で実行 / run while `python main.py --headless` is running in another terminal）:

```bash
python -c "from Utils.AppControl import ping, get_app_status; print(ping()); print(get_app_status())"
```

`pong` とステータスの JSON が表示されれば正常です。
The setup is working if `pong` and a status JSON are printed.

### 5. 実行ファイルのビルド / Building an executable

```bash
pip install -r requirements-build.txt
```

| プラットフォーム / Platform | コマンド / Command |
| --- | --- |
| Windows | `pyinstaller --noconfirm Hiz-mil.exe.spec` |
| Linux | `pyinstaller --noconfirm Hiz-mil_linux.spec` |
| macOS | `./build_mac.sh`（内部で `Hiz-mil.spec` を使用 / uses `Hiz-mil.spec` internally） |

生成物は `dist/` 配下に出力されます。/ The output is placed under `dist/`.

### 6. UI の編集 / Editing the UI

日本語:
`UI/*.ui` の編集には Qt Designer が必要ですが、conda-forge の `pyside6` パッケージには含まれていません（同梱されるのは `pyside6-uic` と `pyside6-rcc` のみ）。ツール専用の環境を別に作成してください。

English:
Editing `UI/*.ui` requires Qt Designer, which is not included in the conda-forge `pyside6` package (only `pyside6-uic` and `pyside6-rcc` are). Create a separate environment for the tools:

```bash
conda create -n qt-tools python=3.12 -y
conda activate qt-tools
pip install "pyside6-essentials>=6.5,<7"
```

`.ui` と生成先ファイルの対応表、PyCharm の外部ツール設定、リソースと翻訳の再生成手順は [Manuals/ui_development_guide.md](Manuals/ui_development_guide.md) にまとめています。
The `.ui`-to-generated-file mapping, PyCharm external tool settings, and the steps for regenerating resources and translations are documented in [Manuals/ui_development_guide.md](Manuals/ui_development_guide.md).

### トラブルシューティング / Troubleshooting

| 症状 / Symptom | 対処 / Resolution |
| --- | --- |
| Windows でインストール時に `OSError: [WinError 206]` が発生する / `OSError: [WinError 206]` during installation on Windows | パスが長すぎます。リポジトリと仮想環境を浅い階層（例: `C:\dev\Hiz-mil`）に置くか、Windows の長いパスのサポートを有効にしてください。/ The path is too long. Place the repository and virtual environment in a shallow directory (e.g. `C:\dev\Hiz-mil`), or enable long path support in Windows. |
| PowerShell で `Activate.ps1` が実行できない / `Activate.ps1` cannot be run in PowerShell | 実行ポリシーの制限です。`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` を実行してから再度試すか、`.venv\Scripts\python.exe main.py` のように直接実行してください。 / This is an execution policy restriction. Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and retry, or call the interpreter directly, e.g. `.venv\Scripts\python.exe main.py`. |
| `ModuleNotFoundError: No module named 'PySide6'` | 仮想環境が有効化されていません。`requirements.txt` をインストールした環境を選択してください。/ The virtual environment is not active. Select the environment where `requirements.txt` was installed. |
| Linux でシリアルポートを開けない / Cannot open the serial port on Linux | 実行ユーザーを `dialout` グループに追加してください（例: `sudo usermod -aG dialout $USER`）。再ログインが必要です。/ Add the user to the `dialout` group (e.g. `sudo usermod -aG dialout $USER`) and log in again. |
| COM ポートが一覧に表示されない / No COM port is listed | USB ケーブルとデバイスドライバの導入状況を確認してください。/ Check the USB cable and that the device driver is installed. |

## ソフトウェアをカスタマイズする場合 / Customizing the Software

日本語:
本アプリケーションを改造・拡張する場合は、`Manuals/` 配下のドキュメントを参照してください。

English:
If you intend to modify or extend the application, refer to the documents under `Manuals/`.

| ドキュメント / Document | 内容 / Contents |
| --- | --- |
| [Manuals/api_customize_guide.md](Manuals/api_customize_guide.md) | UI を変更せずにアプリを制御するための API ガイド。Controller / AppControl / Driver の 3 レイヤ、接続・計測制御・レジスタ操作の呼び出し方、CUI コマンド。<br>API guide for controlling the application without changing the UI: the Controller / AppControl / Driver layers, how to drive connection, measurement and register access, and the CUI commands. |
| [Manuals/ui_development_guide.md](Manuals/ui_development_guide.md) | 画面（`.ui`）の編集手順。Qt Designer の準備、`.ui` と生成ファイルの対応表、リソースと翻訳の再生成。<br>How to edit the screens (`.ui`): setting up Qt Designer, the `.ui`-to-generated-file mapping, and regenerating resources and translations. |
| [Manuals/communication_codes.md](Manuals/communication_codes.md) | デバイス通信のフレーミング仕様。開始・終端・エスケープコードと、送信時のエンコードおよび受信時の復元規則。<br>Framing specification for device communication: the start, end and escape codes, and the encode and restore rules. |

日本語:
まずは [Manuals/api_customize_guide.md](Manuals/api_customize_guide.md) から読むことをおすすめします。通信フレーミングの仕様は、`Models/Hizmil_Driver.py` のドライバ層を直接扱う場合にのみ必要です。

English:
Start with [Manuals/api_customize_guide.md](Manuals/api_customize_guide.md). The framing specification is only needed when working directly with the driver layer in `Models/Hizmil_Driver.py`.

## 使用している Python ライブラリ / Python Libraries Used

### 外部ライブラリ / Third-Party Libraries

| ライブラリ / Library | 用途 / Purpose |
| --- | --- |
| `PySide6` | GUI、Qt Widgets、QML、設定保存、翻訳処理 / GUI, Qt Widgets, QML, settings storage, and translation handling |
| `pyqtgraph` | リアルタイムグラフ描画 / Real-time graph rendering |
| `pandas` | ログや表データの処理 / Log and tabular data handling |
| `numpy` | 数値配列処理、グラフ計算 / Numerical array processing and chart calculations |
| `scipy` | FFT、信号処理 / FFT and signal processing |
| `pyserial` | COM ポート列挙、USB シリアル通信 / COM port enumeration and USB serial communication |
| `pyinstaller` | 実行ファイル化、配布用ビルド（ビルド時のみ / build time only） / Executable packaging and distribution builds |
| `bottleneck`, `numexpr` | pandas / チャート計算の高速化（任意 / optional） / Speeds up pandas and chart computations |

補足 / Note:

日本語:
実際にインストールする依存関係は、用途に応じて次のファイルに定義されています。

| ファイル / File | 用途 / Purpose |
| --- | --- |
| `requirements.txt` | GUI 版の実行 / Running the GUI application |
| `requirements-headless.txt` | ヘッドレス版の実行 / Running in headless mode |
| `requirements-build.txt` | PyInstaller による実行ファイルのビルド / Building an executable with PyInstaller |
| `environment.yml` | conda での GUI 環境構築 / Creating the GUI environment with conda |
| `environment_headless.yml` | conda でのヘッドレス環境構築 / Creating the headless environment with conda |

`bottleneck` と `numexpr` は未インストールでも動作します。

English:
The dependencies to install are defined in the files listed above, depending on how the application is used. `bottleneck` and `numexpr` are optional and the application runs without them.

### 主な標準ライブラリ / Main Standard Library Modules

`argparse`, `os`, `sys`, `threading`, `socket`, `datetime`, `decimal`, `dataclasses`, `queue`, `subprocess`, `webbrowser`

## 設定ファイル / Configuration Files

日本語:
実行時の設定ファイル `config.ini` とプリセットファイル `preset.ini` は、Qt の `QStandardPaths.AppDataLocation` 配下に保存されます。

English:
At runtime, the configuration file `config.ini` and the preset file `preset.ini` are stored under Qt's `QStandardPaths.AppDataLocation`.

## 開発における生成AIの利用について / Use of Generative AI in Development

日本語:
本ソフトウェアの一部のソースコードおよび画像素材は、生成AI(AIコーディングエージェント等)を利用して作成されています。利用にあたっては、この点も踏まえてご評価ください。

English:
Some source code and image assets in this software were created with the assistance of generative AI (including AI coding agents). Please take this into account when evaluating or reviewing this software.

## 想定用途と制約 / Intended Use and Limitations

日本語:
本ソフトウェアは、評価・検証・技術参考を主な目的として公開しています。本番環境、高信頼用途、安全関連用途での利用を前提としていません。これらの用途で利用する場合は、利用者自身の責任において十分な検証とリスク評価を行ってください。

English:
This software is published primarily for evaluation, verification, and technical reference purposes. It is not intended for use in production environments, high-reliability systems, or safety-related applications. If used for such purposes, users are responsible for performing sufficient validation and risk assessment.

## セキュリティに関する注意事項 / Security Notice

日本語:
本ソフトウェアは、商用製品や本番運用システムと同等水準のセキュリティ対策・脆弱性評価を実施していない場合があります。セキュリティ上の問題を発見した場合は GitHub Issue でご報告いただけますが、対応や修正提供を保証するものではありません。Issue には機密情報を記載しないでください。

English:
This software may not have undergone the same level of security review as commercial or production-grade systems. If you discover a security issue, you may report it via a GitHub Issue; however, a response or fix is not guaranteed. Please do not include confidential information in Issue reports.

## 貢献・行動規範 / Contributing and Code of Conduct

日本語:
本リポジトリは、現時点で体系的な外部コントリビューション受け入れ体制を整えていません。Issue でのご意見・不具合報告は歓迎しますが、取り込みや対応時期は保証されません。Issue やコメントでは、他の利用者に敬意を持った態度でご参加ください。

English:
This repository does not currently have a formal process for accepting external contributions. Feedback and bug reports via Issues are welcome, but merging or addressing them is not guaranteed. Please engage respectfully when using Issues or comments.

## 問い合わせ / Contact

日本語:
本ソフトウェアについて、個別のお問い合わせ対応は行っておりません。ご意見・不具合報告は GitHub Issue にてお願いします。

English:
We do not provide individualized support for this software. Please use GitHub Issues for feedback or bug reports.

## 免責事項 / Disclaimer

日本語:
本ソフトウェアは現状有姿のまま提供されます。Macnica, Inc. は、本ソフトウェアの品質、性能、正確性、完全性、有用性、安全性、特定目的適合性および第三者権利非侵害について、明示または黙示を問わず一切保証しません。また、脆弱性、不具合その他の問題が存在しないことも保証しません。本ソフトウェアの利用または利用不能に起因して生じた損害について、Macnica, Inc. は責任を負いません。利用者は、自己の責任において本ソフトウェアの評価、選定、導入および運用を行ってください。

English:
This software is provided "as is". Macnica, Inc. makes no warranties, express or implied, regarding the quality, performance, accuracy, completeness, usefulness, safety, fitness for a particular purpose, or non-infringement of third-party rights of this software, and does not warrant that it is free of vulnerabilities or defects. Macnica, Inc. is not liable for any damages arising from the use or inability to use this software. Users are responsible for evaluating, selecting, deploying, and operating this software at their own risk.

## 作成者 / Author

Macnica,Inc

## 著作権 / Copyright

Copyright (c) Macnica,Inc. All rights reserved.
