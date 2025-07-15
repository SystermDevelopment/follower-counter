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
from PyQt5.QtCore import Qt, QTimer, QTime
 
import API.QiitaAPI as QiitaAPI  # Qiita APIをインポート
import API.xAPI as xAPI  # X APIをインポート
import API.instagramAPI as InstagramAPI  # Instagram APIをインポート
import API.facebookAPI as FacebookAPI  # Facebook APIをインポート


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.fullscreen = True  # フルスクリーン状態の管理フラグ
        self.sns_data = self.fetch_sns_data()
        self.initUI()
        self.setup_timer()  # ← タイマー追加
    
    def setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_time_and_update)
        self.timer.start(60 * 1000)  # 1分ごとに実行（ミリ秒単位）

    def check_time_and_update(self):
        now = QTime.currentTime()
        minute = now.minute()

        if minute % 60 == 0:
            self.update_instagram()
        elif minute % 60 == 15:
            self.update_qiita()
        elif minute % 60 == 30:
            self.update_x()
            pass
        elif minute % 60 == 45:
            self.update_facebook()

    def fetch_sns_data(self):
        """SNSごとのデータを取得してリスト形式で返す"""
        instagram_count = self.safe_api_call(InstagramAPI.get_instagram_follower_count)
        qiita_likes = self.safe_api_call(QiitaAPI.get_qiita_likes_total)
        x_count = self.safe_api_call(xAPI.get_x_follower_count)
        facebook_count = self.safe_api_call(FacebookAPI.get_facebook_follower_count)

        return [
            ("Instagram", instagram_count, "フォロワー数"),
            ("Qiita", qiita_likes, "合計いいね数"),
            ("X", x_count, "フォロワー数"),
            ("Facebook", facebook_count, "フォロワー数"),
        ]

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

    def safe_api_call(self, api_func, default_value="N/A"):
        """
        APIコールを安全に実行し、エラー時はデフォルト値を返す
        
        Args:
            api_func: 実行するAPI関数
            default_value: エラー時の戻り値
        
        Returns:
            APIの結果またはデフォルト値
        """
        try:
            result = api_func()
            return "N/A" if result == -1 else result
        except (ConnectionError, TimeoutError, ValueError) as e:
            print(f"API呼び出しエラー: {e}")
            return default_value
        except Exception as e:
            print(f"予期しないエラー: {e}")
            return default_value

    def update_instagram(self):
        count = self.safe_api_call(InstagramAPI.get_instagram_follower_count)
        self.update_label("Instagram", count)

    def update_qiita(self):
        likes = self.safe_api_call(QiitaAPI.get_qiita_likes_total)
        self.update_label("Qiita", likes)

    def update_x(self):
        count = self.safe_api_call(xAPI.get_x_follower_count)
        self.update_label("X", count)

    def update_facebook(self):
        count = self.safe_api_call(FacebookAPI.get_facebook_follower_count)
        self.update_label("Facebook", count)

    
    def update_label(self, sns_name, new_value):
        for i in range(self.layout().count()):
            frame = self.layout().itemAt(i).widget()
            name_label = frame.findChildren(QLabel)[1]
            count_label = frame.findChildren(QLabel)[2]

            if name_label.text() == sns_name:
                label_type = "フォロワー数" if sns_name != "Qiita" else "合計いいね数"
                count_label.setText(f"{label_type}: {new_value}")