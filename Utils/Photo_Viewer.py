from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene


class PhotoViewer(QGraphicsView):
    """
    QGraphicsViewを継承し、ズームとパンの機能を追加したカスタムビュー
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # QGraphicsSceneをセットアップ
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self.setMinimumSize(200, 200)

        # 画像表示用のアイテム
        self._pixmap_item = None

        # ドラッグ（パン）操作の設定
        # QGraphicsView.ScrollHandDragにより、左ボタンドラッグで移動可能になる
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setMouseTracking(True)

        # ズームのアンチエイリアス処理を有効にする（見た目を滑らかに）
        #self.setRenderHint(QGraphicsView.RenderHint.Antialiasing | QGraphicsView.RenderHint.SmoothPixmapTransform)

        # 画面の端から端までスクロールできるように設定
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)

        # ホイールによるズーム速度
        self._zoom_factor = 1.15

    def set_image(self, file_path):
        """指定されたファイルパスの画像をロードして表示する"""
        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            print(f"Error: Could not load image from {file_path}")
            return

        # 既存のアイテムを削除
        self._scene.clear()

        # QGraphicsPixmapItemとして画像アイテムを作成し、シーンに追加
        self._pixmap_item = self._scene.addPixmap(pixmap)

        # シーンのサイズを画像サイズに合わせる
        self._scene.setSceneRect(QRectF(self._pixmap_item.pixmap().rect()))

    def fit_image(self):
        # ビューを画像全体が見えるようにフィットさせる
        self.fitInView(self._pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)

    def wheelEvent(self, event):
        """マウスホイールイベントを処理し、ズーム操作を行う"""

        # ズームのピボット（中心点）をマウスカーソル位置に設定
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        # event.angleDelta().y()はPySide6でも使えます
        if event.angleDelta().y() > 0:
            # ホイールアップ（拡大）
            self.scale(self._zoom_factor, self._zoom_factor)
        else:
            # ホイールダウン（縮小）
            self.scale(1.0 / self._zoom_factor, 1.0 / self._zoom_factor)

        # ズーム後はピボットを中央に戻す
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)

