# Hiz-mil API カスタマイズガイド

## 目的

このドキュメントは、Hiz-mil アプリケーションをカスタムする開発者が「何をしたい時に、どの API を呼べばよいか」を判断できるようにするためのガイドです。

Hiz-mil は NEシリーズユニットに接続された SR300/SR500 センサーを制御する PC アプリケーションです。アプリ内の UI を変更せずに制御したい場合は、まず `HeadlessController` / `CuiController` の Controller API を使うのが基本です。

## API レイヤ

Hiz-mil には大きく 3 つの API レイヤがあります。

| レイヤ | 主な対象 | 使う場面 | 推奨度 |
|---|---|---|---|
| Controller API | `Controllers\HeadlessController.py`, `Controllers\CuiController.py` | アプリ内カスタム、Headless/CUI 操作、デバッグ操作 | 推奨 |
| AppControl API | `Utils\AppControl.py` | 別プロセスから Hiz-mil を操作する簡易制御 | 用途限定で推奨 |
| Driver API | `Models\Hizmil_Driver*.py` | 通信ドライバを直接扱う低レベル制御 | 必要な場合のみ |

通常のカスタムでは Controller API を使ってください。Controller API は接続確認、board/channel の解決、入力値のパース、状態更新をまとめて扱います。

### 命名規則

API 名は Windows アプリ向けの「SHRX099HS 評価キット 通信ドライバマニュアル」(S2DA0488) の命名に合わせています。マニュアルの `Connect` / `StartMeasure` / `ReadRegPage` などの PascalCase を、Python の慣習に合わせて `connect` / `start_measure` / `read_reg_page` の snake_case にしたものが API 名です。Controller / AppControl / Driver の 3 層で同じ名前を使います。

同名で意味が異なるものが 1 つだけあります。マニュアルの `GetStatus` はひずみセンサーの状態取得なので、Controller API でも `get_status(board, channel)` がセンサー状態取得です。Hiz-mil アプリ全体の状態スナップショット取得はマニュアルに対応する API がないため、`get_app_status()` という別名にしています。

## 基本概念

### Board と Channel

Hiz-mil は最大 2 台の NEシリーズユニットを扱います。

| 指定 | 意味 |
|---|---|
| `board1` / `1` / `b1` | 1 台目の NEシリーズユニット |
| `board2` / `2` / `b2` | 2 台目の NEシリーズユニット |
| `ch1` / `1` / `c1` | 指定 board の 1ch |
| `ch2` / `2` / `c2` | 指定 board の 2ch |

ドライバ内部では論理チャンネルに変換されます。

```python
logical_ch = driver.get_ch(board_kind, channel_index)
```

通常は `get_status("board1", "ch1")` のように Controller API に board/channel を渡せばよく、直接 `logical_ch` を計算する必要はありません。

### ResultKind

通信 API の多くは `ResultKind` を返します。

| 値 | 意味 |
|---|---|
| `ResultKind.ok` | 成功 |
| `ResultKind.parameter_error` | 引数不正 |
| `ResultKind.response_error` | 応答異常 |
| `ResultKind.timeout` | 応答タイムアウト |

### ConnectionStatus

接続 API は `ConnectionStatus` を返します。

| 値 | 意味 |
|---|---|
| `ConnectionStatus.success` | 接続成功 |
| `ConnectionStatus.sensor_not_detected` | センサー未検出、または期待したセンサー種別ではない |
| `ConnectionStatus.board_not_detected` | ボード未検出 |
| `ConnectionStatus.other_error` | その他エラー |
| `ConnectionStatus.mixed_sensor` | SR300/SR500 が混在している |

## 推奨: Controller API

### 起動

Headless で使う場合は次のように起動します。

```powershell
python main.py --headless
```

標準入力から CUI コマンドも使う場合は `--console` を付けます。

```powershell
python main.py --headless --console
```

アプリ内から直接使う場合は `HeadlessController` または既存の `CuiController` インスタンスのメソッドを直接呼びます。

```python
from Controllers.HeadlessController import HeadlessController

controller = HeadlessController(enable_console=False)
controller.start()

result = controller.connect("usb", ["COM3", "COM4"])
print(result)
```

### 接続・切断

| やりたいこと | API | 例 |
|---|---|---|
| USB 接続 | `connect(method, targets)` | `connect("usb", ["COM3", "COM4"])` |
| LAN 接続 | `connect(method, targets)` | `connect("lan", ["192.168.0.10", "192.168.0.11"])` |
| UART 接続 | `connect(method, targets)` | `connect("uart", ["COM3", "COM4"])` |
| 切断 | `disconnect()` | `disconnect()` |
| アプリ終了 | `shutdown_app()` | `shutdown_app()` |

`targets` は board1, board2 の順に指定します。2 台目を使わない場合は `None`、空文字、または LAN では `0.0.0.0` を指定します。

### 状態取得

| やりたいこと | API | 戻り値 |
|---|---|---|
| アプリ全体の状態スナップショット取得 | `get_app_status()` | `dict` |
| FW バージョン取得 | `get_version()` | `(ResultKind, versions)` |
| 指定 ch の状態取得 | `get_status(board, channel)` | `(ResultKind, StrealData, SensorStatus)` |
| センサー種別取得 | `get_sensor_type(board)` | `(ResultKind, ch1_type, ch2_type)` |

例:

```python
result, versions = controller.get_version()
result, streal, sensor_status = controller.get_status("board1", "ch1")
result, ch1_type, ch2_type = controller.get_sensor_type("board1")
```

センサー種別の値は `0x03` が SR300、`0x05` が SR500、`0x00` が invalid です。

### 計測制御

| やりたいこと | API | 例 |
|---|---|---|
| 計測開始 | `start_measure(interval=None, sampling_rate=None, sampling_unit="Hz", mode="all")` | `start_measure(sampling_rate=100, sampling_unit="Hz")` |
| 計測停止 | `stop_measure()` | `stop_measure()` |
| サンプリング件数取得(最大4096件) | `get_sampling_count()` | `get_sampling_count()` |
| サンプリングデータ取得要求 | `get_sampling_data()` | `get_sampling_data()` |

`interval` は us 単位です。`sampling_rate` を使う場合は `sampling_unit` に `Hz`、`sps`、`ms` を指定できます。

計測モード:

| 指定 | 意味 |
|---|---|
| `all` / `1` | 全データ |
| `no_status` / `2` | status なし |
| `strain_only` / `3` | ひずみのみ |

例:

```python
controller.set_time()
controller.set_transfer_mode("on")
controller.start_measure(sampling_rate=100, sampling_unit="Hz", mode="all")

result, count = controller.get_sampling_count()
result, notified_count = controller.get_sampling_data()

controller.stop_measure()
```

### 計測通知を受け取る

計測データ通知をカスタム処理したい場合は、Controller の `driver` に通知ハンドラを登録します。

```python
def on_measure(board, data_list):
    for data in data_list:
        print(board, data.seconds, data.nanoseconds, data.sensor_data)

controller.driver.on_notify_measure(on_measure)
```

`on_notify_measure` のハンドラには `BoardKind` と `list[MeasureData]` が渡されます。

### レジスタ操作

| やりたいこと | API | 例 |
|---|---|---|
| レジスタ書き込み | `write_reg(board, channel, page, data)` | `write_reg("board1", "ch1", 0, [RegData(0x01, 0x1234)])` |
| page 全体読み込み | `read_reg_page(board, channel, page)` | `read_reg_page("board1", "ch1", 0)` |
| 指定アドレス読み込み | `read_reg(board, channel, page, addresses)` | `read_reg("board1", "ch1", 0, [0x01, 0x02])` |
| ROM 反映 | `set_rom(board, channel)` | `set_rom("board1", "ch1")` |

`page` は `0` から `2`、レジスタアドレスは `0x00` から `0x1F` です。

例:

```python
from Models.Sensor import RegData

result = controller.write_reg(
    "board1",
    "ch1",
    0,
    [RegData(addr=0x01, data=0x1234)],
)

result, regs = controller.read_reg("board1", "ch1", 0, [0x01])
result = controller.set_rom("board1", "ch1")
```

### ネットワーク設定

| やりたいこと | API | 例 |
|---|---|---|
| IP/Subnet/Gateway/MAC 取得 | `get_network_address(board, network_type)` | `get_network_address("board1", "ip")` |
| IP/Subnet/Gateway/MAC 設定 | `set_network_address(board, network_type, address)` | `set_network_address("board1", "ip", "192.168.0.10")` |

`network_type` は次を指定できます。

| 指定 | 意味 |
|---|---|
| `ip` / `1` | IP address |
| `subnet` / `subnet_mask` / `mask` / `2` | Subnet mask |
| `gateway` / `3` | Gateway |
| `mac` / `4` | MAC address |

例:

```python
result, ip = controller.get_network_address("board1", "ip")
result, response = controller.set_network_address("board1", "ip", "192.168.0.10")
result, mac = controller.get_network_address("board1", "mac")
```

MAC address は `"001122334455"`、`"00:11:22:33:44:55"`、`"00-11-22-33-44-55"` の形式を受け付けます。

### システム制御

| やりたいこと | API | 例 |
|---|---|---|
| NEシリーズユニット 時刻設定 | `set_time()` | `set_time()` |
| バッファ転送モード設定 | `set_transfer_mode(mode)` | `set_transfer_mode("on")` |

`set_time()` は PC の現在時刻を NEシリーズユニット に送ります。任意日時を指定する API ではありません。

転送モードは、計測データを本体側バッファに蓄積するかどうかを設定します。

| 指定 | 数値指定 | 意味 |
|---|---:|---|
| `on` | `2` | バッファON。計測データを本体側バッファに蓄積します。 |
| `off` | `1` | バッファOFF。バッファ蓄積を使わない通常転送です。 |

ヘルパー API を使う場合は、`transfer_mode_on()` がバッファON、`transfer_mode_off()` がバッファOFFです。

### キャリブレーション

| やりたいこと | API | 例 |
|---|---|---|
| 0 点オフセットキャリブレーション | `offset_calibration(board, channel, ex_temp=0.0, ex_temp_enable=False)` | `offset_calibration("board1", "ch1")` |
| 温度キャリブレーション | `temp_calibration(board, channel, ex_temp=0.0, ex_temp_enable=False)` | `temp_calibration("board1", "ch1", 25.0, True)` |

キャリブレーション API は単独の通信コマンドではなく、レジスタ書き込み、状態取得、ROM 反映などを組み合わせた上位 API です。

## CUI コマンド

`--console` 付きで起動した場合、標準入力から次のコマンドを実行できます。

| コマンド | 内容 |
|---|---|
| `status` | 状態スナップショット取得 |
| `connect <usb\|uart\|lan> <target1> [target2]` | 接続 |
| `disconnect` | 切断 |
| `get_version` | バージョン取得 |
| `set_time` | 時刻設定 |
| `start_measure <interval_us> [all\|no_status\|strain_only]` | 計測開始 |
| `stop_measure` | 計測停止 |
| `get_status <board1\|board2> <ch1\|ch2>` | 指定 ch の状態取得 |
| `write_reg <board> <ch> <page> <addr:data> [addr:data ...]` | レジスタ書き込み |
| `read_reg_page <board> <ch> <page>` | page 読み込み |
| `read_reg <board> <ch> <page> <addr> [addr ...]` | 指定アドレス読み込み |
| `set_rom <board> <ch>` | ROM 反映 |
| `set_transfer_mode <off\|on\|1\|2>` | バッファ転送モード設定 (`on`/`2` = バッファON、`off`/`1` = バッファOFF) |
| `get_sensor_type <board>` | センサー種別取得 |
| `get_network_address <board> <ip\|subnet\|gateway\|mac>` | ネットワークアドレス取得 |
| `set_network_address <board> <ip\|subnet\|gateway\|mac> <address>` | ネットワークアドレス設定 |
| `offset_calibration <board> <ch> [external_temp]` | 0 点オフセットキャリブレーション |
| `temp_calibration <board> <ch> [external_temp]` | 温度キャリブレーション |
| `get_sampling_count` | サンプリング件数取得(最大4096件) |
| `get_sampling_data` | サンプリングデータ取得要求 |
| `exit` | 終了 |

## AppControl API

別プロセスから Hiz-mil を操作する場合は `Utils.AppControl` を使えます。Hiz-mil 側で `HeadlessController` または `CuiController` が起動している必要があります。

```python
from Utils.AppControl import (
    connect,
    start_measure,
    stop_measure,
    get_app_status,
    disconnect,
)

result, status = connect("lan", ["192.168.0.10", "0.0.0.0"])
result, status = start_measure(sampling_rate=100, sampling_unit="Hz", mode="all")
status = get_app_status()
result, status = stop_measure()
disconnected, status = disconnect()
```

現在の `AppControl` で公開されている主な API は次の通りです。

| API | 内容 |
|---|---|
| `ping()` | 疎通確認 |
| `configure_app_control(host=None, port=None, timeout_sec=None)` | 接続先設定 |
| `connect(method, targets)` | 接続 |
| `disconnect()` | 切断 |
| `start_measure(interval=None, sampling_rate=None, sampling_unit=None, mode="all")` | 計測開始 |
| `stop_measure()` | 計測停止 |
| `get_app_status()` | アプリ状態取得 |
| `shutdown_app()` | アプリ終了 |
| `set_transfer_mode(mode)` / `transfer_mode_on()` / `transfer_mode_off()` | バッファ転送モード設定 (`transfer_mode_on()` = バッファON、`transfer_mode_off()` = バッファOFF) |
| `get_sensor_type(board)` | センサー種別取得 |
| `get_network_address(board, network_type)` | ネットワークアドレス取得 |
| `set_network_address(board, network_type, address)` | ネットワークアドレス設定 |

`AppControl` は公開範囲が Controller API より狭いです。レジスタ操作、キャリブレーション、サンプリング件数取得、サンプリングデータ取得要求が必要な場合は、現時点では Controller API を直接使ってください。

## Driver API

Driver API は NEシリーズユニット との通信を直接行う低レベル API です。

| クラス | 用途 |
|---|---|
| `HizmilDriverUSB` | SR500 USB |
| `HizmilDriverLAN` | SR500 LAN |
| `HizmilDriverUSBSR300` | SR300 USB |
| `HizmilDriverLANSR300` | SR300 LAN |

主な Driver API:

| API | 内容 |
|---|---|
| `connect(com)` | 接続 |
| `disconnect(com)` | 切断 |
| `get_board_version(board)` | board 単位のバージョン取得 |
| `set_time()` | PC 現在時刻を設定 |
| `start_measure(interval, mode)` | 計測開始 |
| `stop_measure()` | 計測停止 |
| `write_reg(ch, page, data)` | レジスタ書き込み |
| `read_reg_page(ch, page)` | page 読み込み |
| `read_reg(ch, page, addr)` | 指定レジスタ読み込み |
| `set_rom(ch)` | ROM 反映 |
| `get_status(ch)` | 指定 ch の状態取得 |
| `set_transfer_mode(buf_setting)` | バッファ転送モード設定 (`2` = バッファON、`1` = バッファOFF) |
| `get_sensor_type(board)` | センサー種別取得 |
| `get_network_address(board, network_type)` | ネットワークアドレス取得 |
| `set_network_address(board, network_type, address)` | ネットワークアドレス設定 |
| `get_sampling_count()` | サンプリング件数取得(最大4096件) |
| `get_sampling_data()` | サンプリングデータ取得要求 |
| `offset_calibration(ch, ex_temp, ex_temp_enable)` | 0 点オフセットキャリブレーション |
| `temp_calibration(ch, ex_temp, ex_temp_enable)` | 温度キャリブレーション |
| `on_notify_measure(handler)` | 計測通知ハンドラ登録 |

Driver API を直接使う場合は、接続状態チェック、board/channel 変換、状態更新を呼び出し側で考慮する必要があります。通常は Controller API を優先してください。

## 推奨フロー

一般的な制御フローは次の通りです。

1. `connect(...)`
2. `get_version()`
3. `set_time()`
4. 必要に応じて `set_transfer_mode(...)`
5. 必要に応じて `get_sensor_type(...)`、`get_network_address(...)`
6. `controller.driver.on_notify_measure(...)` で計測通知ハンドラ登録
7. `start_measure(...)`
8. 計測中は通知ハンドラまたは `get_app_status()` で状態取得
9. 必要に応じて `get_sampling_count()`、`get_sampling_data()`
10. `stop_measure()`
11. `disconnect()`

## 旧 API 名からの移行

Controller API の `debug_*` プレフィックスは廃止し、通信ドライバマニュアル準拠の名前に変更しました。旧名は残していないため、既存のカスタムコードは次の表に従って置き換えてください。

### Controller API (`HeadlessController` / `CuiController`)

| 旧名 | 新名 |
|---|---|
| `debug_connect(method, targets)` | `connect(method, targets)` |
| `debug_disconnect()` | `disconnect()` |
| `debug_get_version()` | `get_version()` |
| `debug_set_time()` | `set_time()` |
| `debug_measure_start(...)` / `debug_start_measure(interval, mode)` | `start_measure(...)` に一本化 |
| `debug_measure_stop()` / `debug_stop_measure()` | `stop_measure()` に一本化 |
| `debug_get_status()` | `get_app_status()` |
| `debug_get_channel_status(board, channel)` | `get_status(board, channel)` |
| `debug_get_sensor_type(board)` | `get_sensor_type(board)` |
| `debug_write_reg(...)` | `write_reg(...)` |
| `debug_read_reg_page(...)` | `read_reg_page(...)` |
| `debug_read_reg(...)` | `read_reg(...)` |
| `debug_set_rom(...)` | `set_rom(...)` |
| `debug_set_transfer_mode(mode)` | `set_transfer_mode(mode)` |
| `debug_get_network_address(...)` | `get_network_address(...)` |
| `debug_set_network_address(...)` | `set_network_address(...)` |
| `debug_get_sampling_count()` | `get_sampling_count()` |
| `debug_get_sampling_data()` | `get_sampling_data()` |
| `debug_offset_calibration(...)` | `offset_calibration(...)` |
| `debug_temp_calibration(...)` | `temp_calibration(...)` |
| `debug_shutdown()` | `shutdown_app()` |
| `register_debug_console_helpers()` | `register_console_helpers()` |

`HeadlessController.shutdown()` は従来どおりアプリ内部の停止処理です。外部から終了させる API は `shutdown_app()` です。

### AppControl API (`Utils.AppControl`)

| 旧名 | 新名 |
|---|---|
| `connect_device(method, targets)` | `connect(method, targets)` |
| `disconnect_device()` | `disconnect()` |
| `start_measurement(...)` | `start_measure(...)` |
| `stop_measurement()` | `stop_measure()` |
| `get_status()` | `get_app_status()` |

`ping()`、`configure_app_control()`、`shutdown_app()`、`set_transfer_mode()`、`transfer_mode_on()`、`transfer_mode_off()`、`get_sensor_type()`、`get_network_address()`、`set_network_address()` は変更ありません。

### Python Console 用ヘルパー (`hizmil_*`)

| 旧名 | 新名 |
|---|---|
| `hizmil_connect_device` / `hizmil_disconnect_device` | `hizmil_connect` / `hizmil_disconnect` |
| `hizmil_start_measurement` / `hizmil_stop_measurement` | `hizmil_start_measure` / `hizmil_stop_measure` |
| `hizmil_get_status` | `hizmil_get_app_status` |
| `hizmil_get_channel_status` | `hizmil_get_status` |
| `hizmil_shutdown` | `hizmil_shutdown_app` |

### AppControl の JSON コマンド名

別プロセスから TCP (既定 `127.0.0.1:18765`) で直接 JSON を送っている場合は、コマンド名も変更されています。

| 旧コマンド | 新コマンド |
|---|---|
| `measure_start` | `start_measure` |
| `measure_stop` | `stop_measure` |
| `get_status` | `get_app_status` |
| `shutdown` | `shutdown_app` |

CUI コマンド名 (`connect`、`start_measure`、`get_status` など) は変更ありません。

## 注意事項

- Controller API は Headless/CUI での外部操作用 API として使える。デバッグ専用ではない。
- UI の表示更新を前提にしないカスタムでは `HeadlessController` を使う。
- `CuiController` は GUI 起動中にコンソール操作を追加するための Controller。
- `driver` を直接差し替える場合は、SR300/SR500、USB/LAN の組み合わせを崩さないこと。
- `get_sampling_data()` はデータ通知を開始させる要求であり、戻り値は応答に含まれるサンプリング件数。実データは `on_notify_measure` の通知で受け取る。
- ネットワーク設定を書き換える場合は、対象 board を間違えないこと。特に 2 台構成では `board1` と `board2` の target 順が重要。
