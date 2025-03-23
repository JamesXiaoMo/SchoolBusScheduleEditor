import sys
from bin.init import ifFolderExists
from bin.busCrawler import busCrawler
from bin.downloadImg import download_image
from ui import CreateNewScheduleUI
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHeaderView,
    QCheckBox,
    QFrame
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import (
    Qt,
    QCoreApplication,
    QRect
)
from ui.MainWindowUI import Ui_MainWindow


class CreatNewScheduleWindow(CreateNewScheduleUI.QMainWindow):
    def __init__(self, x, y, parent=None):
        super().__init__(parent)
        self.ui = CreateNewScheduleUI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.x = x
        self.y = y
        self.move(self.x + 640, self.y)
        for k in range(2):
            for i in range(14):
                exec(f'self.ui.line_{i} = QFrame(self.ui.tab_{1 + k})')
                exec(f'self.ui.line_{i}.setObjectName("line_{i}")')
                exec(f'self.ui.line_{i}.setGeometry(QRect(0, {40 + i *40}, 730, 3))')
                exec(f'self.ui.line_{i}.setFrameShape(QFrame.Shape.HLine)')
                exec(f'self.ui.line_{i}.setFrameShadow(QFrame.Shadow.Sunken)')
            for j in range(15):
                for i in range(12):
                    exec(f"self.ui.checkBox_{1 + k}_{7 + j}{i * 5} = QCheckBox(self.ui.tab_{1 + k})")
                    exec(f'self.ui.checkBox_{1 + k}_{7 + j}{i * 5}.setObjectName(u"checkBox_1_{7 + j}{i * 5}")')
                    exec(
                        f"self.ui.checkBox_{1 + k}_{7 + j}{i * 5}.setGeometry(QRect({5 + i * 60}, {10 + j * 40}, 60, 20))"
                    )
                    exec(
                        f'self.ui.checkBox_{1 + k}_{7 + j}{i * 5}.setText(QCoreApplication.translate("MainWindow", u"{7 + j}:'
                        f'{i * 5 if i > 1 else f'0{i * 5}'}", None))'
                    )

    def moveEvent(self, event):
        if self.parent():
            self.parent().move(self.pos().x() - 640, self.pos().y())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.CreatNewScheduleWindow = CreatNewScheduleWindow(x=self.pos().x(), y=self.pos().y(), parent=self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.busTitles = []
        self.busLinks = []
        self.ui.pushButton.clicked.connect(self.updateBusInfo)
        self.ui.comboBox.currentTextChanged.connect(self.showImage)
        self.ui.pushButton_2.clicked.connect(self.openCreatNewScheduleWindow)
        header = self.ui.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)
        self.ui.tableWidget.setColumnWidth(0, 309)
        self.ui.tableWidget.setColumnWidth(1, 309)

    def moveEvent(self, event):
        self.CreatNewScheduleWindow.move(self.pos().x() + 640, self.pos().y())

    def updateBusInfo(self):
        self.ui.comboBox.clear()
        self.busTitles, self.busLinks = busCrawler()
        for i in self.busTitles:
            self.ui.comboBox.addItem(i)
        for i in range(len(self.busTitles)):
            download_image(url=self.busLinks[i], save_dir="pics", filename=f'{self.busTitles[i]}.jpg')

    def showImage(self):
        self.ui.label.clear()
        pixmap = QPixmap(f"pics/{self.ui.comboBox.currentText()}.jpg")
        self.ui.label.setPixmap(pixmap.scaled(self.ui.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def openCreatNewScheduleWindow(self):
        self.CreatNewScheduleWindow.show()
        for k in range(2):
            for j in range(15):
                for i in range(12):
                    exec(f"self.CreatNewScheduleWindow.ui.checkBox_{1 + k}_{7 + j}{i * 5}.setChecked(0)")


if __name__ == "__main__":
    ifFolderExists("pics")
    ifFolderExists("schedules")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
