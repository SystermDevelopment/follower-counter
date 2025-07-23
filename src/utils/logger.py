import logging
import logging.handlers
from pathlib import Path
from datetime import datetime

def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    """各モジュール用のロガーを設定
    
    Args:
        name: ロガーの名前（通常はモジュール名）
        log_file: ログファイル名（Noneの場合はコンソールのみ）
        
    Returns:
        設定済みのロガーインスタンス
    """
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
    
    # コンソール出力（INFOレベル以上）
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # ファイル出力（DEBUGレベル以上）
    if log_file:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # 日付ごとにローテーション
        file_handler = logging.handlers.TimedRotatingFileHandler(
            log_dir / log_file,
            when='midnight',
            interval=1,
            backupCount=7,  # 7日分保持
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # 親ロガーへの伝播を防ぐ
    logger.propagate = False
    
    return logger