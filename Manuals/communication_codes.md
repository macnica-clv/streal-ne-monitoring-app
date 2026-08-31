# <span style="color:#2563eb">通信フレーミングコードまとめ</span>

現在のデバイス通信フレームは、<span style="color:#0f766e">SR300/SR500</span> および <span style="color:#0f766e">USB/LAN</span> で共通の <span style="color:#7c3aed">`SerialCommon`</span> 実装を使用しています。

定義箇所:

- <span style="color:#7c3aed">`Models/Hizmil_Driver.py`</span>

## <span style="color:#2563eb">コード一覧</span>

| 種類 | 定数名 | 値 |
|---|---|---|
| <span style="color:#1d4ed8">開始コード</span> | <span style="color:#7c3aed">`CODE_TOP`</span> | <span style="color:#1d4ed8">`0xFE`</span> |
| <span style="color:#047857">終端コード</span> | <span style="color:#7c3aed">`CODE_END`</span> | <span style="color:#047857">`0xFD`</span> |
| <span style="color:#b45309">エスケープコード</span> | <span style="color:#7c3aed">`CODE_ESCAPE`</span> | <span style="color:#b45309">`0x5C`</span> |
| <span style="color:#6d28d9">開始コード用エスケープ値</span> | <span style="color:#7c3aed">`ESCAPE_CODE_TOP`</span> | <span style="color:#6d28d9">`0x00`</span> |
| <span style="color:#0e7490">終端コード用エスケープ値</span> | <span style="color:#7c3aed">`ESCAPE_CODE_END`</span> | <span style="color:#0e7490">`0x01`</span> |
| <span style="color:#92400e">エスケープコード用エスケープ値</span> | <span style="color:#7c3aed">`ESCAPE_CODE_ESCAPE`</span> | <span style="color:#92400e">`0x5C`</span> |

## <span style="color:#2563eb">送信フレーム形式</span>

送信時は <span style="color:#7c3aed">`encode_sr500()`</span> で、ペイロードを以下の形式にエンコードします。

```text
0xFE + エスケープ済みペイロード + 0xFD
```

つまり、フレームの先頭に開始コード <span style="color:#1d4ed8">`0xFE`</span>、末尾に終端コード <span style="color:#047857">`0xFD`</span> を付与します。

## <span style="color:#2563eb">エスケープ規則</span>

ペイロード中に <span style="color:#1d4ed8">開始コード</span>、<span style="color:#047857">終端コード</span>、<span style="color:#b45309">エスケープコード</span> と同じ値が含まれる場合は、<span style="color:#7c3aed">`encode_byte()`</span> で次のように置換されます。

| 元データ | 送信されるバイト列 |
|---|---|
| <span style="color:#1d4ed8">`0xFE`</span> | <span style="color:#b45309">`0x5C`</span> <span style="color:#6d28d9">`0x00`</span> |
| <span style="color:#047857">`0xFD`</span> | <span style="color:#b45309">`0x5C`</span> <span style="color:#0e7490">`0x01`</span> |
| <span style="color:#b45309">`0x5C`</span> | <span style="color:#b45309">`0x5C`</span> <span style="color:#92400e">`0x5C`</span> |

## <span style="color:#2563eb">受信時の復元</span>

受信時は <span style="color:#7c3aed">`decode_sr500()`</span> が内部状態を持ってデコードします。

1. <span style="color:#1d4ed8">`0xFE`</span> を受けるまで待機します。
2. <span style="color:#1d4ed8">`0xFE`</span> を受けるとフレーム収集を開始します。
3. <span style="color:#047857">`0xFD`</span> を受けると 1 フレーム完了としてコールバックします。
4. <span style="color:#b45309">`0x5C`</span> を受けると、次の 1 バイトをエスケープ値として扱います。

復元規則は次の通りです。

| 受信されたエスケープ列 | 復元後の値 |
|---|---|
| <span style="color:#b45309">`0x5C`</span> <span style="color:#6d28d9">`0x00`</span> | <span style="color:#1d4ed8">`0xFE`</span> |
| <span style="color:#b45309">`0x5C`</span> <span style="color:#0e7490">`0x01`</span> | <span style="color:#047857">`0xFD`</span> |
| <span style="color:#b45309">`0x5C`</span> <span style="color:#92400e">`0x5C`</span> | <span style="color:#b45309">`0x5C`</span> |

## <span style="color:#2563eb">使用箇所</span>

<span style="color:#0f766e">USB/LAN</span> と <span style="color:#0f766e">SR300/SR500</span> の各ドライバで、同じ <span style="color:#7c3aed">`SerialCommon`</span> のエンコード/デコード処理が使われています。

- <span style="color:#0f766e">SR500 USB</span>: <span style="color:#7c3aed">`Models/Hizmil_Driver_USB.py`</span>
- <span style="color:#0f766e">SR300 USB</span>: <span style="color:#7c3aed">`Models/Hizmil_Driver_SR300_USB.py`</span>
- <span style="color:#0f766e">SR500 LAN</span>: <span style="color:#7c3aed">`Models/Hizmil_Driver_LAN.py`</span>
- <span style="color:#0f766e">SR300 LAN</span>: <span style="color:#7c3aed">`Models/Hizmil_Driver_SR300_LAN.py`</span>
