import sys
from PyQt5.QtWidgets import QApplication
from ui import Window  # ui.py から Window をインポート

app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec_())
