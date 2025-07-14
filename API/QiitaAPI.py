from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from config import QIITA_TOKEN, ORGANIZATION_NAME
import requests
import time
import re
import shutil

qiita_organization_url = "https://qiita.com/organizations/" + ORGANIZATION_NAME  # Qiita組織のURLを入力

def get_organization_members():
    # システムにインストールされたchromedriverのパスを取得
    chromedriver_path = shutil.which("chromedriver")
    service = Service(chromedriver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # メンバーページに直接アクセス
        members_url = f"https://qiita.com/organizations/{ORGANIZATION_NAME}/members"
        driver.get(members_url)
        time.sleep(10)  # 読み込み時間を増やす
        
        # デバッグ用：ページタイトルを確認
        
        # 複数のセレクタを試す
        member_links = []
        # ...existing code...
        selectors = [
            "a[href^='/']"
        ]

        for selector in selectors:
            links = driver.find_elements(By.CSS_SELECTOR, selector)
            if links:
                member_links = links
                break

        # ...existing code...
        authors = set()

        # spanタグからユーザー名抽出
        spans = driver.find_elements(By.CSS_SELECTOR, "span[class^='style-']")
        for span in spans:
            text = span.text.strip()
            # 「@」の次にユーザー名が続くパターンを抽出
            match = re.match(r"^@\s*([A-Za-z0-9_-]+)$", text)
            if match:
                username = match.group(1)
                authors.add(username)

        # ...existing code...
        return authors
        
    except Exception as e:
        print(f"エラー: {e}")
        return set()
    finally:
        driver.quit()

# いいね数取得関数
def get_likes(username):
    headers = {"Authorization": f"Bearer {QIITA_TOKEN}"}
    page = 1
    per_page = 100
    total_likes = 0

    while True:
        url = f"https://qiita.com/api/v2/users/{username}/items?page={page}&per_page={per_page}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"{username}さんのAPIエラー: {response.status_code}")
            print("詳細:", response.text)
            break

        items = response.json()

        if not isinstance(items, list) or not items:
            break

        for item in items:
            total_likes += item.get('likes_count', 0)

        page += 1

    return total_likes

def get_qiita_likes_total():
    members = get_organization_members()
    add_like_count = 0

    # メンバーごとにいいね数取得（APIの負荷軽減のため1秒待機）
    for member in members:
        likes = get_likes(member)
        add_like_count += likes
        time.sleep(1)  # APIリクエスト間隔を空ける
    
    # 合計いいね数を返す
    return add_like_count

