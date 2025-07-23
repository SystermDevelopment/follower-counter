import requests
from utils.config import IG_USER_ID, IG_TOKEN

def validate_env():
    if not IG_USER_ID or not IG_TOKEN:
        raise EnvironmentError("[Instagram_API] エラー: 環境変数 IG_USER_ID または IG_TOKEN が未設定です")


def get_instagram_follower_count():
    validate_env()
    url = f"https://graph.facebook.com/{IG_USER_ID}"
    params = {
        "fields": "followers_count",
        "access_token": IG_TOKEN
    }

    try:
        res = requests.get(url, params=params)
        if res.status_code == 200:
            data = res.json()
            return int(data.get("followers_count", -1))
        else:
            print(f"[Instagram_API] エラー: ステータスコード {res.status_code}")
            return -1
    except Exception as e:
        print(f"[Instagram_API] 例外: {str(e)}")
        return -1
