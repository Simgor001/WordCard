import sys
import core
# import img_rc
import threading
import update
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


if __name__ == "__main__":
    threading.Thread(target=update.update, args=('1.2.0',)).start()
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(':/logo/icon.png'))
    # if sys.platform.startswith('win'):
    #    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
    #        "Sail Word Card")
    app.setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton)
    SailWordCard = core.core()
    SailWordCard.show()
    
    sys.exit(app.exec())
