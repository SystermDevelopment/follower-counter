import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QFrame,
    QVBoxLayout,
    QLabel
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

import API.QiitaAPI as QiitaAPI  # Qiita APIをインポート
import API.xAPI as xAPI  # X APIをインポート
import API.instagramAPI as InstagramAPI  # Instagram APIをインポート
import API.facebookAPI as FacebookAPI  # Facebook APIをインポート


class Window(QWidget):
    # SNSごとのフォロワー数やいいね数をクラス変数で管理
    instagram_count = InstagramAPI.get_instagram_follower_count()  # Instagramのフォロワー数を取得
    qiita_likes = QiitaAPI.get_qiita_likes_total()  # Qiitaのいいね数を取得
    x_count = xAPI.get_x_follower_count()  # Xのフォロワー数を取得
    facebook_count = FacebookAPI.get_facebook_follower_count()  # Facebookのフォロワー数を取得

    # SNS名とカウント、表示ラベルの対応リスト
    sns_data = [
        ("Instagram", instagram_count, "フォロワー数"),
        ("Qiita", qiita_likes, "合計いいね数"),
        ("X", x_count, "フォロワー数"),
        ("Facebook", facebook_count, "フォロワー数"),
    ]

    def __init__(self):
        super().__init__()
        self.fullscreen = True  # フルスクリーン状態の管理フラグ
        self.initUI()

    def initUI(self):
        self.setWindowTitle("SNSフォロワー数")
        self.showFullScreen()

        grid = QGridLayout()
        self.setLayout(grid)

        # SNSごとにフレームを作成してグリッドに追加
        for i, (sns, count, label) in enumerate(self.sns_data):
            frame = self.createSNSFrame(sns, count, label)
            grid.addWidget(frame, i // 2, i % 2)

        grid.setSpacing(10)
        grid.setContentsMargins(10, 10, 10, 10)

    def createSNSFrame(self, sns, count, label):
        """SNSごとのフレームを生成"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Box | QFrame.Raised)

        layout = QVBoxLayout()

        # アイコン画像のパスを作成し、ラベルに設定
        icon_path = f"./asset/{sns.lower()}.png"
        icon_label = QLabel()
        pixmap = QPixmap(icon_path).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignCenter)

        # SNS名のラベル
        name_label = QLabel(sns)
        name_label.setFont(QFont("Arial", 24, QFont.Bold))
        name_label.setAlignment(Qt.AlignCenter)

        # フォロワー数またはいいね数のラベル
        count_label = QLabel(f"{label}: {count}")
        count_label.setFont(QFont("Arial", 18))
        count_label.setAlignment(Qt.AlignCenter)

        # レイアウトに各ウィジェットを追加
        layout.addWidget(icon_label)
        layout.addWidget(name_label)
        layout.addWidget(count_label)
        frame.setLayout(layout)

        return frame

    def keyPressEvent(self, event):
        # ESCキーでフルスクリーン⇔最大化を切り替え
        if event.key() == Qt.Key_Escape:
            if self.fullscreen:
                self.showMaximized()
            else:
                self.showFullScreen()
            self.fullscreen = not self.fullscreen
