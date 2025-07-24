import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
import json

def load_logging_config():
    """設定ファイルからロギング設定を読み込む"""
    try:
        settings_path = Path(__file__).resolve().parent.parent.parent / "settings" / "settings.json"
        with open(settings_path, "r") as f:
            settings = json.load(f)
            return settings.get("logging", {
                "console_level": "INFO",
                "file_level": "DEBUG",
                "enabled": True
            })
    except Exception:
        # デフォルト設定
        return {
            "console_level": "INFO",
            "file_level": "DEBUG",
            "enabled": True
        }

def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    """各モジュール用のロガーを設定
    
    Args:
        name: ロガーの名前（通常はモジュール名）
        log_file: ログファイル名（Noneの場合はコンソールのみ）
        
    Returns:
        設定済みのロガーインスタンス
    """
    # 設定を読み込む
    config = load_logging_config()
    
    # ロギングが無効の場合はNullHandlerを返す
    if not config.get("enabled", True):
        logger = logging.getLogger(name)
        logger.addHandler(logging.NullHandler())
        return logger
    
    logger = logging.getLogger(name)
    
    # 既にハンドラーが設定されている場合はスキップ
    if logger.handlers:
        return logger
        
    logger.setLevel(logging.DEBUG)
    
    # ログフォーマット
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # コンソール出力（設定ファイルからレベルを取得）
    console_level = getattr(logging, config.get("console_level", "INFO").upper())
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # ファイル出力（DEBUGレベル以上）
    if log_file:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # 日付ごとにローテーション
        file_level = getattr(logging, config.get("file_level", "DEBUG").upper())
        file_handler = logging.handlers.TimedRotatingFileHandler(
            log_dir / log_file,
            when='midnight',
            interval=1,
            backupCount=7,  # 7日分保持
            encoding='utf-8'
        )
        file_handler.setLevel(file_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # 親ロガーへの伝播を防ぐ
    logger.propagate = False
    
    return logger