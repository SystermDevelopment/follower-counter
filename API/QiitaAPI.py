from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from config import QIITA_TOKEN, ORGANIZATION_NAME
import requests
import time
import re
import shutil



def get_organization_members():
    # システムにインストールされたchromedriverのパスを取得
    chromedriver_path = shutil.which("chromedriver")
    service = Service(chromedriver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)

    qiita_organization_url = "https://qiita.com/organizations/" + ORGANIZATION_NAME  # Qiita組織のURLを入力

    driver.get(qiita_organization_url)
    time.sleep(5)

    article_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/items/']")
    authors = set()

    for link in article_links:
        href = link.get_attribute('href')
        match = re.match(r"https://qiita.com/([^/]+)/items/", href)
        if match:
            authors.add(match.group(1))

    driver.quit()
    return authors

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

def validate_env():
    if not QIITA_TOKEN or not ORGANIZATION_NAME:
        raise EnvironmentError("[QiitaAPI] QIITA_TOKEN または ORGANIZATION_NAME が未設定です")

def get_qiita_likes_total():
    validate_env()
    members = get_organization_members()
    add_like_count = 0

    # メンバーごとにいいね数取得（APIの負荷軽減のため1秒待機）
    for member in members:
        likes = get_likes(member)
        add_like_count += likes
        time.sleep(1)  # APIリクエスト間隔を空ける
    
    # 合計いいね数を返す
    return add_like_count

