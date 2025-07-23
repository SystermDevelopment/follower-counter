import requests
from utils.config import X_TOKEN, X_ACCOUNT
from utils.logger import setup_logger

# ロガーの設定
logger = setup_logger('X_API', 'x.log')

# === 設定項目 ===
USERNAME = X_ACCOUNT  # 任意のXユーザー名
CONFIG = {
    "BEARER_TOKEN": X_TOKEN,             # XのBearerトークンを入力
    "BASE_URL": "https://api.twitter.com/2",
    "HEADERS": lambda token: {
        "Authorization": f"Bearer {token}"
    }
}

def validate_env():
    if not CONFIG["BEARER_TOKEN"] or not USERNAME:
        logger.critical("必須環境変数が未設定: X_TOKEN または X_ACCOUNT")
        raise EnvironmentError("環境変数 X_TOKEN または X_ACCOUNT が未設定です")

# === フォロワー数を取得する関数 ===
def get_x_follower_count():
    try:
        logger.info(f"Xフォロワー数取得開始: @{USERNAME}")
        validate_env()
        token = CONFIG["BEARER_TOKEN"]
        headers = CONFIG["HEADERS"](token)

        # ユーザー名からユーザーIDを取得
        user_url = f'{CONFIG["BASE_URL"]}/users/by/username/{USERNAME}'
        logger.debug(f"ユーザー情報取得URL: {user_url}")
        resp_user = requests.get(user_url, headers=headers)
        
        if resp_user.status_code != 200:
            logger.warning(f"ユーザー取得失敗 (ステータスコード: {resp_user.status_code})")
            return -1

        user_id = resp_user.json()["data"]["id"]
        logger.debug(f"ユーザーID取得成功: {user_id}")

        # フォロワー数などのメトリクス取得
        detail_url = f'{CONFIG["BASE_URL"]}/users/{user_id}?user.fields=public_metrics'
        logger.debug(f"メトリクス取得URL: {detail_url}")
        resp_detail = requests.get(detail_url, headers=headers)
        
        if resp_detail.status_code != 200:
            logger.warning(f"詳細情報取得失敗 (ステータスコード: {resp_detail.status_code})")
            return -1

        data = resp_detail.json()["data"]
        followers = data["public_metrics"]["followers_count"]
        
        logger.info(f"Xフォロワー数取得完了: {followers}")
        return followers
    except Exception as e:
        logger.error(f"フォロワー数取得中に例外発生", exc_info=True)
        return -1
