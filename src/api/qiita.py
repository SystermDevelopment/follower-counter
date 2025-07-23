from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config import QIITA_TOKEN, ORGANIZATION_NAME
from utils.logger import setup_logger
import requests
import time
import re
import shutil

# ロガーの設定
logger = setup_logger('QiitaAPI', 'qiita.log')



def get_organization_members():
    logger.info(f"組織メンバー取得開始: {ORGANIZATION_NAME}")
    
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
        logger.debug(f"アクセスURL: {members_url}")
        driver.get(members_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span[class^='style-']"))
        )

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
                logger.debug(f"メンバー追加: {username}")

        logger.info(f"取得メンバー数: {len(authors)}")
        return authors
        
    except Exception as e:
        logger.error(f"メンバー取得中に例外発生", exc_info=True)
        return set()
    finally:
        driver.quit()

# いいね数取得関数
def get_likes(username):
    logger.debug(f"ユーザー{username}のいいね数取得開始")
    headers = {"Authorization": f"Bearer {QIITA_TOKEN}"}
    page = 1
    per_page = 100
    total_likes = 0

    while True:
        url = f"https://qiita.com/api/v2/users/{username}/items?page={page}&per_page={per_page}"
        logger.debug(f"API URL: {url}")
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            logger.warning(f"ユーザー{username}の情報取得失敗 (ステータスコード: {response.status_code})")
            break

        items = response.json()

        if not isinstance(items, list) or not items:
            break

        for item in items:
            total_likes += item.get('likes_count', 0)

        page += 1

    logger.debug(f"ユーザー{username}の合計いいね数: {total_likes}")
    return total_likes

def validate_env():
    if not QIITA_TOKEN or not ORGANIZATION_NAME:
        logger.critical("必須環境変数が未設定: QIITA_TOKEN または ORGANIZATION_NAME")
        raise EnvironmentError("環境変数 QIITA_TOKEN または ORGANIZATION_NAME が未設定です")

def get_qiita_likes_total():
    try:
        logger.info("Qiita合計いいね数取得開始")
        validate_env()
        members = get_organization_members()
        add_like_count = 0

        # メンバーごとにいいね数取得（APIの負荷軽減のため1秒待機）
        for member in members:
            likes = get_likes(member)
            add_like_count += likes
            logger.debug(f"現在の合計いいね数: {add_like_count}")
            time.sleep(1)  # APIリクエスト間隔を空ける
        
        # 合計いいね数を返す
        logger.info(f"Qiita合計いいね数取得完了: {add_like_count}")
        return add_like_count
    except Exception as e:
        logger.error(f"合計いいね数取得中に例外発生", exc_info=True)
        return -1

