"""
QRコード生成ユーティリティ
各SNSのプロフィールURLをQRコードに変換して保存
"""
import qrcode
import os
from pathlib import Path
from utils.logger import setup_logger

logger = setup_logger(__name__, "qr_generator.log")

# プロジェクトルート
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
QR_DIR = PROJECT_ROOT / "data" / "qr"


def generate_all_qr_codes():
    """
    全SNSのQRコードを生成してdata/qr/に保存
    起動時に毎回実行される想定
    """
    logger.info("QRコード生成開始")

    # 保存先ディレクトリを作成
    QR_DIR.mkdir(parents=True, exist_ok=True)

    # 各SNSのURL定義
    sns_urls = {
        "instagram": f"https://www.instagram.com/{os.getenv('IG_USERNAME', '')}",
        "x": f"https://x.com/{os.getenv('X_ACCOUNT', '')}",
        "facebook": f"https://www.facebook.com/{os.getenv('FB_PAGE_NAME', '')}",
        "qiita": f"https://qiita.com/organizations/{os.getenv('ORGANIZATION_NAME', '')}"
    }

    # 各SNSごとにQRコード生成
    for sns_name, url in sns_urls.items():
        try:
            # 環境変数が空の場合はスキップ（URLが"https://.../"で終わる）
            if not url.endswith('/'):
                qr = qrcode.QRCode(
                    version=1,  # QRコードのサイズ（1-40）
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,  # 各ボックスのピクセル数
                    border=2,     # 余白のサイズ
                )
                qr.add_data(url)
                qr.make(fit=True)

                # 画像生成
                img = qr.make_image(fill_color="black", back_color="white")

                # 保存
                qr_path = QR_DIR / f"{sns_name}_qr.png"
                img.save(str(qr_path))
                logger.info(f"{sns_name} QRコード生成完了: {url} -> {qr_path}")
            else:
                logger.warning(f"{sns_name} の環境変数が設定されていません（URL: {url}）")

        except Exception as e:
            logger.error(f"{sns_name} QRコード生成失敗: {e}", exc_info=True)

    logger.info("QRコード生成完了")


def get_qr_path(sns_name: str) -> Path:
    """
    指定されたSNSのQRコード画像パスを取得

    Args:
        sns_name: SNS名（Instagram, X, Facebook, Qiita）

    Returns:
        QRコード画像のPathオブジェクト
    """
    return QR_DIR / f"{sns_name.lower()}_qr.png"
