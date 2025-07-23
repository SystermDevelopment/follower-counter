import sys
from PyQt5.QtWidgets import QApplication
from ui.window import Window  # ui.window から Window をインポート
from utils.logger import setup_logger

# アプリケーションのメインロガー設定
logger = setup_logger('MainApp', 'app.log')

if __name__ == "__main__":
    logger.info("アプリケーション起動開始")
    
    try:
        app = QApplication(sys.argv)
        win = Window()
        win.show()
        logger.info("メインウィンドウ表示完了")
        
        exit_code = app.exec_()
        logger.info(f"アプリケーション終了 (終了コード: {exit_code})")
        sys.exit(exit_code)
        
    except Exception as e:
        logger.critical("アプリケーション起動失敗", exc_info=True)
        sys.exit(1)
