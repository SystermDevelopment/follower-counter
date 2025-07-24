import requests
from utils.config import IG_USER_ID, IG_TOKEN
from utils.logger import setup_logger

# ロガーの設定
logger = setup_logger('InstagramAPI', 'instagram.log')

def validate_env():
    if not IG_USER_ID or not IG_TOKEN:
        logger.critical("必須環境変数が未設定: IG_USER_ID または IG_TOKEN")
        raise EnvironmentError("[Instagram_API] エラー: 環境変数 IG_USER_ID または IG_TOKEN が未設定です")


def get_instagram_follower_count():
    logger.info("Instagramフォロワー数取得開始")
    validate_env()
    url = f"https://graph.facebook.com/{IG_USER_ID}"
    params = {
        "fields": "followers_count",
        "access_token": IG_TOKEN
    }
    logger.debug(f"API URL: {url}")

    try:
        res = requests.get(url, params=params)
        if res.status_code == 200:
            data = res.json()
            follower_count = int(data.get("followers_count", -1))
            logger.info(f"Instagramフォロワー数取得成功: {follower_count}")
            return follower_count
        else:
            logger.error(f"APIエラー: ステータスコード {res.status_code}")
            logger.error(f"レスポンス内容: [詳細はデバッグログを確認]")
            logger.debug(f"レスポンス詳細: {res.text[:200]}..." if len(res.text) > 200 else f"レスポンス詳細: {res.text}")
            return -1
    except Exception as e:
        logger.error(f"予期しないエラーが発生しました", exc_info=True)
        return -1
