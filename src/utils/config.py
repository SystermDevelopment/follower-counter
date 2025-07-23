from dotenv import load_dotenv
import os

load_dotenv()  # .env を読み込む（1回でOK）

# 環境変数から設定を取得
QIITA_TOKEN: str = os.getenv("QIITA_TOKEN")
ORGANIZATION_NAME: str = os.getenv("ORGANIZATION_NAME")
X_TOKEN: str = os.getenv("X_TOKEN")
X_ACCOUNT: str = os.getenv("X_ACCOUNT")
IG_USER_ID: str = os.getenv("IG_USER_ID")
IG_TOKEN: str = os.getenv("IG_TOKEN")
FB_PAGE_ID: str = os.getenv("FB_PAGE_ID")
FB_TOKEN: str = os.getenv("FB_TOKEN")
