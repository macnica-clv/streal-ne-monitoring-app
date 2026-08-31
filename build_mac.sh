#!/bin/bash

# --- 設定 ---
APP_NAME="Hiz-mil"
SPEC_FILE="Hiz-mil.spec"

echo "🚀 ビルドを開始します..."

# 1. 古いビルドデータの削除
echo "🧹 古いファイルを削除中..."
rm -rf build dist

# 2. PyInstallerを実行
echo "📦 PyInstallerを実行中..."
pyinstaller --noconfirm $SPEC_FILE

# 3. 署名処理（これがないと起動しない）
echo "✍️  バイナリに署名を追加中..."
# 内部の全ライブラリに署名
find dist/$APP_NAME.app -name "*.dylib" -exec codesign --force --deep --sign - {} \;
# アプリ本体に署名
codesign --force --deep --sign - dist/$APP_NAME.app

# 4. 隔離属性の解除
echo "🔓 セキュリティ制限を解除中..."
xattr -cr dist/$APP_NAME.app

echo "✅ ビルドが完了しました！ dist フォルダを確認してください。"