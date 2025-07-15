import os
import requests
from dotenv import load_dotenv

load_dotenv()

FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_TOKEN = os.getenv("FB_TOKEN")

def validate_env():
    if not FB_PAGE_ID or not FB_TOKEN:
        raise EnvironmentError("[FacebookAPI] 環境変数 FB_PAGE_ID または FB_TOKEN が未設定です")

def get_facebook_follower_count():
    validate_env()
    url = f"https://graph.facebook.com/{FB_PAGE_ID}"
    params = {
        "fields": "followers_count",
        "access_token": FB_TOKEN
    }
    try:
        res = requests.get(url, params=params)
        if res.status_code == 200:
            data = res.json()
            return int(data.get("followers_count", -1))
        else:
            print(f"[FacebookAPI] Error: Status {res.status_code}")
            return -1
    except Exception as e:
        print(f"[FacebookAPI] Exception: {str(e)}")
        return -1
