import requests
from utils.config import X_TOKEN, X_ACCOUNT

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
        raise EnvironmentError("[xAPI] X_TOKEN または X_ACCOUNT が未設定です")

# === フォロワー数を取得する関数 ===
def get_x_follower_count():
    validate_env()
    token = CONFIG["BEARER_TOKEN"]
    headers = CONFIG["HEADERS"](token)

    # ユーザー名からユーザーIDを取得
    user_url = f'{CONFIG["BASE_URL"]}/users/by/username/{USERNAME}'
    resp_user = requests.get(user_url, headers=headers)
    
    if resp_user.status_code != 200:
        print("ユーザー取得エラー:", resp_user.status_code, resp_user.text)
        return f"情報エラー（{resp_user.status_code}エラー）"

    user_id = resp_user.json()["data"]["id"]

    # フォロワー数などのメトリクス取得
    detail_url = f'{CONFIG["BASE_URL"]}/users/{user_id}?user.fields=public_metrics'
    resp_detail = requests.get(detail_url, headers=headers)
    
    if resp_detail.status_code != 200:
        print("詳細情報取得エラー:", resp_detail.status_code, resp_detail.text)
        return f"詳細情報エラー（{resp_detail.status_code}エラー）"

    data = resp_detail.json()["data"]
    followers = data["public_metrics"]["followers_count"]
    print(f"@{USERNAME} のXフォロワー数は {followers} 人です。")
    
    return followers
