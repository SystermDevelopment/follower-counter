import sys
import json
import os
from datetime import datetime

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

DAILY_JSON = "./data/daily_followers.json"

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.fullscreen = True  # フルスクリーン状態の管理フラグ
        self.sns_data = self.init_sns_data()
        self.initUI()
        self.fetch_sns_data()
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

    def init_sns_data(self):
        """SNSごとのデータを取得してリスト形式で返す"""
        return [
            ("Instagram", "N/A", "フォロワー数"),
            ("Qiita", "N/A", "合計いいね数"),
            ("X", "N/A", "フォロワー数"),
            ("Facebook", "N/A", "フォロワー数"),
        ]
    
    def fetch_sns_data(self):
        """SNSごとのデータをAPIから取得し、パラメーターをセット"""
        self.update_instagram()
        self.update_qiita()
        self.update_x()
        self.update_facebook()

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

        diff_label = QLabel("前日比: -")
        diff_label.setFont(QFont("Arial", 16))
        diff_label.setAlignment(Qt.AlignCenter)
        diff_label.setObjectName("diff_label")

        # レイアウトに各ウィジェットを追加
        layout.addWidget(icon_label)
        layout.addWidget(name_label)
        layout.addWidget(count_label)
        layout.addWidget(diff_label)
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
            diff_label = frame.findChildren(QLabel, "diff_label")[0]

            if name_label.text() == sns_name:
                label_type = "フォロワー数" if sns_name != "Qiita" else "合計いいね数"
                count_label.setText(f"{label_type}: {new_value}")
                self.save_today_follower(sns_name, new_value)
            
                # 前日比計算＆表示
                diff_str = self.show_follower_diff(sns_name, new_value)
                diff_label.setText(f"前日比: {diff_str}")            

    def save_today_follower(self, sns_name, newvalue):
        """本日の日付でフォロワー数をJSONに記録・上書きする"""
        today = datetime.now().strftime("%Y-%m-%d")
        try:
            dir_path = os.path.dirname(DAILY_JSON)
            os.makedirs(dir_path, exist_ok=True)
            # 既存データの読み込み
            try:
                with open(DAILY_JSON, "r") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {}

            # 今日の日付のデータがなければ作成
            if today not in data:
                data[today] = {}

            # SNSごとの値を上書き
            data[today][sns_name] = newvalue

            # 保存
            with open(DAILY_JSON, "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"フォロワー数保存エラー: {e}")

    def get_yesterday_follower(self, sns_name):
        """前日の日付のフォロワー数をJSONから取得"""
        from datetime import timedelta

        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        yesterday_str = yesterday.strftime("%Y-%m-%d")

        try:
            with open(DAILY_JSON, "r") as f:
                data = json.load(f)
            # 前日データがあればSNS名で取得
            if yesterday_str in data and sns_name in data[yesterday_str]:
                return data[yesterday_str][sns_name]
            else:
                return None  # データなし
        except (FileNotFoundError, json.JSONDecodeError):
            return None  # ファイルなしや破損時もNone
        
    def show_follower_diff(self, sns_name, today_count):
        """本日と前日を比較し、前日比を返す（文字列で）"""
        yesterday_count = self.get_yesterday_follower(sns_name)
        if yesterday_count is None:
            return "前日データなし"
        try:
            diff = int(today_count) - int(yesterday_count)
            sign = "+" if diff > 0 else ""
            return f"{sign}{diff}"
        except Exception:
            return "計算エラー"
