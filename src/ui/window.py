import sys
import json
import os
from pathlib import Path
from datetime import datetime, timedelta

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

from utils.sound import play_increase_sound  # 音声再生関数をインポート
from utils.logger import setup_logger

import api.qiita as QiitaAPI  # Qiita APIをインポート
import api.x as xAPI  # X APIをインポート
import api.instagram as InstagramAPI  # Instagram APIをインポート
import api.facebook as FacebookAPI  # Facebook APIをインポート

# プロジェクトのルートディレクトリを取得
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SETTINGS_JSON = PROJECT_ROOT / "settings" / "settings.json"

# ロガーのセットアップ
logger = setup_logger(__name__, "window.log")

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.settings = self.load_settings()
        self.daily_json = PROJECT_ROOT / "data" / "daily_followers.json"
        self.compare_days_ago = self.settings.get("compare_days_ago", 1)
        self.sound_volume = self.settings.get("sound_volume", 50)

        self.fullscreen = True  # フルスクリーン状態の管理フラグ
        self.sns_data = self.init_sns_data()
        self.initUI()
        self.fetch_sns_data()
        self.setup_timer()  # ← タイマー追加
    
    def load_settings(self):
        try:
            with open(str(SETTINGS_JSON), "r") as f:
                return json.load(f)
        except Exception:
            # デフォルト値
            return {
                "compare_days_ago": 1,
                "daily_json": str(PROJECT_ROOT / "data" / "daily_followers.json"),
                "sound_volume": 50
            }
    
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
        icon_path = PROJECT_ROOT / "asset" / f"{sns.lower()}.png"
        icon_label = QLabel()
        pixmap = QPixmap(str(icon_path)).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
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

        diff_label = QLabel(f"{self.compare_days_ago}日前比: -")
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
            logger.error(f"API呼び出しエラー: {e}", exc_info=True)
            return default_value
        except Exception as e:
            logger.error(f"予期しないエラー: {e}", exc_info=True)
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

                # 旧値を現在の表示から取得
                current_text = count_label.text()
                old_value_str = current_text.split(": ")[1] if ": " in current_text else "N/A"

                # 音声再生判定
                if self.should_play_sound(old_value_str, new_value):
                    play_increase_sound(volume=self.sound_volume)

                # 表示更新
                count_label.setText(f"{label_type}: {new_value}")
                self.save_today_follower(sns_name, new_value)
            
                # 比較対象日のフォロワー数差分を計算し、UIに反映
                diff_str = self.show_follower_diff(sns_name, new_value)
                diff_label.setText(f"{self.compare_days_ago}日前比: {diff_str}")            

    def save_today_follower(self, sns_name, newvalue):
        """本日の日付でフォロワー数をJSONに記録・上書きする"""
        today = datetime.now().strftime("%Y-%m-%d")
        try:
            self.daily_json.parent.mkdir(parents=True, exist_ok=True)
            # 既存データの読み込み
            try:
                with open(str(self.daily_json), "r") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {}

            # 今日の日付のデータがなければ作成
            if today not in data:
                data[today] = {}

            # SNSごとの値を上書き
            data[today][sns_name] = newvalue

            # 保存
            with open(str(self.daily_json), "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"フォロワー数保存エラー: {e}", exc_info=True)
        
    def show_follower_diff(self, sns_name, today_count):
        """本日と“任意の日数前”を比較し、差分を返す（文字列で）"""
        # 日付の計算
        today = datetime.now().date()
        compare_date = today - timedelta(days=self.compare_days_ago)
        compare_date_str = compare_date.strftime("%Y-%m-%d")

        # 指定日の値を取得
        try:
            with open(self.daily_json, "r") as f:
                data = json.load(f)
            compare_count = data.get(compare_date_str, {}).get(sns_name, None)
        except (FileNotFoundError, json.JSONDecodeError):
            compare_count = None

        if compare_count is None:
            return f"{compare_date_str}データなし"
        try:
            diff = int(today_count) - int(compare_count)
            sign = "+" if diff > 0 else ""
            return f"{sign}{diff}"
        except ValueError:
            return "無効なデータ: 数値に変換できません"
        except Exception:
            return "計算エラー"

    def should_play_sound(self, old_value_str, new_value):
        """音声再生の条件判定を分離"""
        try:
            if old_value_str == "N/A":
                return False
            old_value = int(old_value_str)
            new_int = int(new_value)
            return new_int > old_value
        except (ValueError, TypeError):
            return False

