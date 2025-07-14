import os
import requests
from dotenv import load_dotenv

load_dotenv()

FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_TOKEN = os.getenv("FB_TOKEN")

def get_facebook_follower_count():
    url = f"https://graph.facebook.com/v19.0/{FB_PAGE_ID}?fields=followers_count&access_token={FB_TOKEN}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            return int(data.get("followers_count", -1))
        else:
            print(f"[FacebookAPI] Error: Status {res.status_code}")
            return -1
    except Exception as e:
        print(f"[FacebookAPI] Exception: {str(e)}")
        return -1
