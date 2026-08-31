def float_to_q_format(float_value: float, n_bits_fraction: int, total_bits: int = 16) -> int:
    """
    浮動小数点数 (float) を指定された符号つきQフォーマット (Qm.n, 全体16ビット固定) に変換する。

    Args:
        float_value (float): 変換したい浮動小数点数。
        n_bits_fraction (int): 小数部のビット数 (n)。例: Q0.16なら 16, Q1.15なら 15。
        total_bits (int): 全体のビット幅（デフォルト16ビット）。

    Returns:
        int: 変換された符号つきQフォーマットのHex値。
    """

    # 1. スケーリング
    # Qm.nフォーマットでは、2^n を掛けて値をスケーリング。
    # 例: Q0.16なら 2^16 = 65536 を掛ける
    scaled_value = float_value * (2 ** n_bits_fraction)

    # 2. 丸め (最も近い整数へ)
    int_value = int(round(scaled_value))

    # 3. クランプ（範囲制限）
    # 16ビット符号付き整数の最大値と最小値を計算します。
    max_value = (2 ** (total_bits - 1)) - 1
    min_value = -(2 ** (total_bits - 1))

    # 計算された値がQフォーマットの表現範囲を超えていないかチェックし、超えていれば制限。
    if int_value > max_value:
        # オーバーフロー
        print(f"警告: 値 {float_value} は Qm.{n_bits_fraction} の最大値 {max_value} を超えました。値をクランプします。")
        int_value = max_value
    elif int_value < min_value:
        # アンダーフロー
        print(f"警告: 値 {float_value} は Qm.{n_bits_fraction} の最小値 {min_value} を下回りました。値をクランプします。")
        int_value = min_value

    # 4. 2の補数表現（Pythonの整数は自動で処理されますが、16ビット整数として解釈される値を出力）
    # Pythonのintはビット幅を気にしなくて良いため、そのままint_valueを返す。
    # ただし、負の値の場合、ハードウェアや他の言語で16ビットとして扱う際には
    # 2の補数として解釈される。
    # ここでは、その16ビットの範囲内にある整数値を返すことで要件を満たす。

    # 符号付き16ビットの範囲 (0xFFFF = -1, 0x8000 = -32768) に収めるためにマスクを適用する場合
    # return int_value & 0xFFFF
    # を使うが、単にPythonの整数として返す場合は以下でOK。
    return int_value


def q_format_to_float(q_int_value: int, n_bits_fraction: int, total_bits: int = 16) -> float:
    """
    指定された符号つきQフォーマット (Qm.n, 全体16ビット固定) の整数値を浮動小数点数 (float) に変換する。

    Args:
        q_int_value (int): 符号つきQフォーマットで表現された固定小数点数（Pythonの整数型）。
        n_bits_fraction (int): 小数部のビット数 (n)。例: Q0.16なら 16, Q1.15なら 15。
        total_bits (int): 全体のビット幅（デフォルト16ビット）。

    Returns:
        float: 復元された浮動小数点数。
    """

    # 1. 16ビット符号付き整数として値を解釈（2の補数処理）
    # Pythonの整数はビット幅を気にしなくて良いが、
    # 16ビット符号付き整数として解釈するために、負の値かどうかをチェックし、
    # 必要であれば2の補数から元の値に戻す処理を行う。
    # ここでは、簡潔にstructモジュールを使って16ビット符号付き整数として解釈する。
    # '>' はビッグエンディアン、'h' は符号付き2バイト（16ビット）整数を意味する。

    # 2の補数から元の値への復元 (Pythonのint型はこれを意識しなくても計算可能だが、
    # 意図を明確にするために16ビット範囲に収める)
    if total_bits == 16:
        # 16ビットのマスク (0xFFFF)
        mask = 0xFFFF
        # 符号ビットが立っているかチェック (0x8000)
        if q_int_value & (1 << (total_bits - 1)):
            # 負の値の場合、2の補数表現をPythonの負の整数に変換
            # 例: 0xFFFF -> -1, 0x8000 -> -32768
            signed_int_value = q_int_value - (1 << total_bits)
        else:
            # 正の値の場合、そのまま使用
            signed_int_value = q_int_value
    else:
        # 16ビット以外のビット幅に対応する場合 (汎用的にint()の値をそのまま使用)
        signed_int_value = q_int_value

    # 2. スケーリングの逆操作 (2^n で割る)
    # 浮動小数点数に戻すには、2^n_bits_fraction で除算。
    float_value = signed_int_value / (2 ** n_bits_fraction)

    return float_value


def float_to_q_format_unsigned(float_value: float, n_bits_fraction: int, total_bits: int = 16) -> int:
    """
    浮動小数点数 (float) を指定された符号なしQフォーマット (Qm.n) に変換する。

    Args:
        float_value (float): 変換したい浮動小数点数。
        n_bits_fraction (int): 小数部のビット数 (n)。
        total_bits (int): 全体のビット幅（デフォルト16ビット）。

    Returns:
        int: 変換されたQフォーマットの固定小数点数（Pythonの整数型）。
    """

    # 1. 負の値チェック
    if float_value < 0:
        print(f"警告: 符号なしQフォーマットは負の値を扱えません。入力 {float_value} は0にクランプされます。")
        float_value = 0.0

    # 2. スケーリング
    scaled_value = float_value * (2 ** n_bits_fraction)

    # 3. 丸め
    int_value = int(round(scaled_value))

    # 4. クランプ（範囲制限）
    # 16ビット符号なし整数の最大値と最小値を計算する。
    max_value = (2 ** total_bits) - 1  # 2^16 - 1 = 65535
    min_value = 0

    if int_value > max_value:
        # オーバーフロー
        print(
            f"警告: 値 {float_value} は Q{total_bits - n_bits_fraction}.{n_bits_fraction} の最大値 {max_value} を超えました。値をクランプします。")
        int_value = max_value
    elif int_value < min_value:
        # アンダーフロー (負の値は既に0にクランプされているため、この分岐は通常発生しない)
        int_value = min_value

    # 符号なしの値として返却
    return int_value


def q_format_to_float_unsigned(q_int_value: int, n_bits_fraction: int) -> float:
    """
    指定された符号なしQフォーマット (Qm.n) の整数値を浮動小数点数 (float) に変換する。

    Args:
        q_int_value (int): Qフォーマットで表現された固定小数点数（Pythonの整数型）。
        n_bits_fraction (int): 小数部のビット数 (n)。

    Returns:
        float: 復元された浮動小数点数。
    """

    # 符号なしの値なので、そのまま除算（逆スケーリング）を行う。
    float_value = q_int_value / (2 ** n_bits_fraction)

    return float_value
