import os
import requests
from dotenv import load_dotenv

load_dotenv()

IG_USER_ID = os.getenv("IG_USER_ID")
IG_TOKEN = os.getenv("IG_TOKEN")

def get_instagram_follower_count():
    url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}?fields=followers_count&access_token={IG_TOKEN}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            return int(data.get("followers_count", -1))
        else:
            print(f"[InstagramAPI] Error: Status {res.status_code}")
            return -1
    except Exception as e:
        print(f"[InstagramAPI] Exception: {str(e)}")
        return -1
