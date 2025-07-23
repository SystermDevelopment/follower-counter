import sys
from PyQt5.QtWidgets import QApplication
from ui.window import Window  # ui.window から Window をインポート

app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec_())
