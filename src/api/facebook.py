import requests
from utils.config import FB_PAGE_ID, FB_TOKEN
from utils.logger import setup_logger

# ロガーの設定
logger = setup_logger('FacebookAPI', 'facebook.log')

def validate_env():
    if not FB_PAGE_ID or not FB_TOKEN:
        logger.critical("必須環境変数が未設定: FB_PAGE_ID または FB_TOKEN")
        raise EnvironmentError("[Facebook_API] エラー: 環境変数 FB_PAGE_ID または FB_TOKEN が未設定です")

def get_facebook_follower_count():
    logger.info("Facebookフォロワー数取得開始")
    validate_env()
    url = f"https://graph.facebook.com/{FB_PAGE_ID}"
    params = {
        "fields": "followers_count",
        "access_token": FB_TOKEN
    }
    logger.debug(f"API URL: {url}")
    try:
        res = requests.get(url, params=params)
        if res.status_code == 200:
            data = res.json()
            follower_count = int(data.get("followers_count", -1))
            logger.info(f"Facebookフォロワー数取得成功: {follower_count}")
            return follower_count
        else:
            logger.error(f"APIエラー: ステータスコード {res.status_code}")
            logger.error(f"レスポンス内容: {res.text}")
            return -1
    except Exception as e:
        logger.error(f"予期しないエラーが発生しました", exc_info=True)
        return -1
