import sys
import os
import mainWin
import json
import aboutWin
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtPrintSupport


class core(QtWidgets.QMainWindow, mainWin.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        '字典列表："item,A,B,tab_len"'
        self.word_list = list()
        self.setupUi(self)

        self.setConnect()
        self.add_Word: QtWidgets.QListWidgetItem = self.listWidget.addItem(
            '...')

        self.listWidget.setCurrentRow(0)
        self.listWidget.setSelectionMode(self.listWidget.SingleSelection)

        self.now_tab_len = 0
        self.sheet = 0
        self.file_name = ''
        self.file_change = False
        self.file_change_SW = False

        self.update_data()

    def setupUi(self, parent):
        super().setupUi(parent)
        self.lineEdit_col.setValidator(QtGui.QIntValidator())
        self.lineEdit_row.setValidator(QtGui.QIntValidator())
        self.lineEdit_size.setValidator(QtGui.QIntValidator())

    def setConnect(self):
        self.lineEdit_A.returnPressed.connect(self.save_item)
        self.lineEdit_B.returnPressed.connect(self.save_item)
        self.lineEdit_row.editingFinished.connect(self.update_data)
        self.lineEdit_col.editingFinished.connect(self.update_data)

        self.A_new.triggered.connect(self.new_file)
        self.A_open.triggered.connect(self.open_file)
        self.A_save.triggered.connect(self.save)
        self.A_saveAs.triggered.connect(self.save_as)
        self.A_quit.triggered.connect(self.close)
        self.A_del.triggered.connect(self.del_item)
        self.A_preview.triggered.connect(self.start_preview)
        self.A_print.triggered.connect(self.start_print)

        self.pushButton.clicked.connect(self.save_item)
        self.pushButton_del.clicked.connect(self.del_item)
        self.pushButton_preview.clicked.connect(self.start_preview)
        self.pushButton_print.clicked.connect(self.start_print)
        self.listWidget.itemSelectionChanged.connect(self.selectionChanged)
        self.listWidget.itemActivated.connect(self.item_activated)
        self.A_aboutQT.triggered.connect(QtWidgets.QApplication.aboutQt)
        self.A_about.triggered.connect(self.about)

    def about(self):
        class AboutDialog(QtWidgets.QDialog, aboutWin.Ui_aboutWin):
            def __init__(self, parent):
                super().__init__(parent)
                self.setupUi(self)

        AboutDialog(self).show()

    def update_data(self):
        if self.file_change_SW:
            self.file_change = True
        else:
            self.file_change_SW = False
        self.label_num.setText(str(len(self.word_list)))
        error_num = 0
        for i in self.word_list:
            if i['A'] == '(空)' or i['B'] == '(空)':
                error_num += 1
        self.label_error_num.setText(str(error_num))
        # 计算页数
        row = int(self.lineEdit_row.text())
        col = int(self.lineEdit_col.text())
        self.sheet = int(len(self.word_list) / (row * col))
        if len(self.word_list) % (row * col) != 0:
            self.sheet += 1
        self.label_paper.setText(str(self.sheet))

    def item_activated(self, item):
        index = self.listWidget.currentRow()
        now_item = self.listWidget.currentItem()
        if now_item.text() == '...':
            self.lineEdit_A.setText('')
            self.lineEdit_B.setText('')
            self.lineEdit_A.setFocus(True)
        else:
            word_a = self.word_list[index]['A']
            word_b = self.word_list[index]['B']
            if word_a == '(空)':
                self.lineEdit_A.setFocus(True)
                self.lineEdit_B.setText(word_b)
            elif word_b == '(空)':
                self.lineEdit_B.setFocus(True)
                self.lineEdit_A.setText(word_a)
            else:
                self.lineEdit_A.setFocus(True)
                self.lineEdit_B.setText(word_b)
                self.lineEdit_A.setText(word_a)
        if now_item.text() == '...':
            self.pushButton_del.setEnabled(False)
            self.A_del.setEnabled(False)
        else:
            self.pushButton_del.setEnabled(True)
            self.A_del.setEnabled(True)

    def selectionChanged(self):
        index = self.listWidget.currentRow()
        now_item = self.listWidget.currentItem()
        self.lineEdit_A.setText('')
        self.lineEdit_B.setText('')
        if now_item.text() == '...':
            # 设置焦点
            self.lineEdit_A.setFocus(True)
        else:
            word_a = self.word_list[index]['A']
            word_b = self.word_list[index]['B']
            if word_a == '(空)':
                self.lineEdit_B.setText(word_b)

            elif word_b == '(空)':
                self.lineEdit_A.setText(word_a)

            else:

                self.lineEdit_A.setText(word_a)
                self.lineEdit_B.setText(word_b)
        if now_item.text() == '...':
            self.pushButton_del.setEnabled(False)
            self.A_del.setEnabled(False)
        else:
            self.pushButton_del.setEnabled(True)
            self.A_del.setEnabled(True)

    def save_item(self):
        self.file_change = True
        word_a = self.lineEdit_A.text()
        word_b = self.lineEdit_B.text()

        now_item: QtWidgets.QListWidgetItem = self.listWidget.currentItem()
        if now_item.text() == '...':
            # 添加模式
            if word_a.strip() == '' + word_b.strip() == '':
                return
            self.add_item()
            self.lineEdit_A.setText('')
            self.lineEdit_B.setText('')
            self.listWidget.setCurrentRow(self.listWidget.count() - 1)
            self.lineEdit_A.setFocus(True)
        else:
            # 修改模式
            if word_a.strip() == '' + word_b.strip() == '':
                self.del_item()
                return
            if word_a.strip() == '':
                word_a = '(空)'
            if word_b.strip() == '':
                word_b = '(空)'
            index = self.listWidget.currentRow()

            word_tab_len = self.get_tab_len(word_a)
            self.word_list[index]['A'] = word_a
            self.word_list[index]['B'] = word_b
            self.word_list[index]['tab_len'] = word_tab_len
            now_item.setText(word_a + self.get_tab(word_tab_len) + word_b)

            self.lineEdit_A.setText('')
            self.lineEdit_B.setText('')
            self.listWidget.setCurrentRow(index + 1)
        self.update_data()

    def add_item(self):
        word_a = self.lineEdit_A.text()
        word_b = self.lineEdit_B.text()

        if word_a.strip() == '':
            word_a = '(空)'
        if word_b.strip() == '':
            word_b = '(空)'
        ins_row = self.listWidget.count() - 1
        word_tab_len = self.get_tab_len(word_a)
        word_item = self.listWidget.insertItem(
            ins_row, word_a + self.get_tab(word_tab_len) + word_b)
        word_dict = {
            'item': word_item,
            'A': word_a,
            'B': word_b,
            'tab_len': word_tab_len
        }
        self.word_list.append(word_dict)

    def del_item(self):
        self.file_change = True
        index = self.listWidget.currentRow()
        self.listWidget.takeItem(index)
        if self.word_list.pop(index)['tab_len'] >= self.now_tab_len:
            max_len = 0
            for i in self.word_list:
                if i['tab_len'] > max_len:
                    max_len = i['tab_len']
            self.now_tab_len = max_len
            self.set_item()
        self.update_data()

    def get_tab_len(self, word_a: str):
        tab_len = int(len(bytes(word_a, 'GBK')) / 7)
        if len(bytes(word_a, 'GBK')) in (27, 20):
            tab_len += 1
        if tab_len >= self.now_tab_len:
            # 如果A词条太长，就需要整体增长tab
            self.now_tab_len = tab_len
            self.set_item()
        return tab_len

    def get_tab(self, word_tab_len: int):
        return (self.now_tab_len - word_tab_len + 2) * '\t'

    def set_item(self):
        index = 0
        for i in self.word_list:
            item: QtWidgets.QListWidgetItem = self.listWidget.item(index)
            word_a = self.word_list[index]['A']
            word_b = self.word_list[index]['B']
            word_tab_len = self.word_list[index]['tab_len']
            item.setText(word_a + self.get_tab(word_tab_len) + word_b)
            index += 1

    def new_file(self):
        opinion = self.check_save()
        if opinion != 0:
            self.file_change = False
            self.setWindowTitle('Sail Word Card')
            self.word_list.clear()
            self.listWidget.clear()
            self.add_Word: QtWidgets.QListWidgetItem = self.listWidget.addItem(
                '...')

            self.listWidget.setCurrentRow(0)
            self.listWidget.setSelectionMode(self.listWidget.SingleSelection)
            self.file_name = ''

    def open_file(self, file_name=''):

        if file_name != '' and type(file_name) == str:
            if not file_name.lower().endswith('.wordcard'):
                QtWidgets.QMessageBox.critical(
                    self, '错误', '打开文件"%s"失败！该文件不是Sail Word Card文件！' % file_name)
                sys.exit('10 打开的文件不是Sail Word Card文件')
            if not os.path.isfile(file_name):
                return
            self.file_name = file_name
            self.setWindowTitle(self.file_name + ' - Sail Word Card')
            self.file_change = False

            with open(self.file_name, 'r', encoding='UTF-8') as f:
                self.load_file(json.load(f))
            return
        opinion = self.check_save()
        if opinion != 0:
            self.file_name = str(QtWidgets.QFileDialog.getOpenFileName(
                self, '打开..', '', 'Sail Word Card文件(*.WordCard)')[0]).strip()
            if self.file_name != '':
                with open(self.file_name, 'r', encoding='UTF-8') as f:
                    self.load_file(json.load(f))
                self.setWindowTitle(self.file_name + ' - Sail Word Card')
                self.file_change = False

    def save(self):
        self.check_save(True)

    def save_as(self):
        self.check_save(True, True)

    def load_file(self, word_card: dict):

        self.word_list.clear()
        self.listWidget.clear()
        self.add_Word: QtWidgets.QListWidgetItem = self.listWidget.addItem(
            '...')

        self.listWidget.setCurrentRow(0)
        self.listWidget.setSelectionMode(self.listWidget.SingleSelection)

        self.lineEdit_row.setText(str(word_card['row']))
        self.lineEdit_col.setText(str(word_card['col']))
        self.fontComboBox.setCurrentFont(QtGui.QFont(word_card['font']))
        self.lineEdit_size.setText(str(word_card['size']))
        self.now_tab_len = word_card['tab_len']
        self.word_list = word_card['data']
        index = 0
        for i in self.word_list:
            ins_row = self.listWidget.count() - 1
            i['item'] = self.listWidget.insertItem(
                ins_row, i['A'] + self.get_tab(i['tab_len']) + i['B'])
            self.word_list[index] = i
            index += 1
        self.listWidget.setCurrentRow(self.listWidget.count() - 1)
        self.update_data()

    def save_file(self):
        row = int(self.lineEdit_row.text())
        col = int(self.lineEdit_col.text())
        font = self.fontComboBox.currentFont().family()
        size = int(self.lineEdit_size.text())
        word_card = {
            'type': 'WordCard',
            'row': row,
            'col': col,
            'font': font,
            'size': size,
            'tab_len': self.now_tab_len,
            'data': self.word_list
        }
        return word_card

    def check_save(self, is_save=False, save_as=False):
        '''寻问文件是否需要保存，如果需要则弹出提示框\n
        返回值：0表示取消操作，1表示已经保存，2表示不保存'''
        opinion = 0
        if self.file_change:
            if not is_save:
                # 寻问是否需要保存
                opinion = saveMessageBox(self).exec()

        if opinion == 0 and self.file_change or is_save == True:
            # 选择保存
            if self.file_name == '' or save_as:
                # 当文件没有保存过，需要寻问保存位置
                self.file_name = str(QtWidgets.QFileDialog.getSaveFileName(
                    self, '另存为..' if save_as else '保存', '', 'Sail Word Card文件(*.WordCard)')[0]).strip()

            if self.file_name != '':
                with open(self.file_name, 'w', encoding='UTF-8') as f:
                    json.dump(self.save_file(), f,
                              ensure_ascii=False, indent=4)
                self.setWindowTitle(self.file_name + ' - Sail Word Card')
                self.file_change = False
                return 1
            else:
                return 0
        elif opinion == 1:
            return 2
        elif opinion == 2:
            return 0
        else:
            return 1
        ...

    def closeEvent(self, event):
        """改写窗口即将关闭信号"""
        if self.check_save() == 0:
            event.ignore()
        else:
            event.accept()

    def start_preview(self):
        pre = QtPrintSupport.QPrintPreviewDialog(self)
        pre.setWindowFlags(
            pre.windowFlags() | QtCore.Qt.WindowMaximizeButtonHint)
        pre.paintRequested.connect(self.preview)
        pre.exec()

    def preview(self, printer):
        self.init_print(printer)
        row = int(self.lineEdit_row.text())
        col = int(self.lineEdit_col.text())
        size = int(self.lineEdit_size.text())
        count = int(self.lineEdit.text())
        printer.setCopyCount(count)
        font = self.fontComboBox.currentFont().family()
        word_list = list()
        for i in self.word_list:
            word_list.append((i['A'], i['B']))
        self.print(word_list, row, col, font, size, True)

    def start_print(self):
        prt = QtPrintSupport.QPrinter()
        self.init_print(prt)
        row = int(self.lineEdit_row.text())
        col = int(self.lineEdit_col.text())
        size = int(self.lineEdit_size.text())
        font = self.fontComboBox.currentFont().family()
        count = int(self.lineEdit.text())
        prt.setCopyCount(count)
        word_list = list()
        for i in self.word_list:
            word_list.append((i['A'], i['B']))
        prt_dio = QtPrintSupport.QPrintDialog(prt, self)
        if prt_dio.exec():
            self.print(word_list, row, col, font, size)

    def init_print(self, printer):
        self.prt: QtPrintSupport.QPrinter = printer
        self.pat = QtGui.QPainter()
        self.prt.setPageSize(self.prt.A4)
        # 横向
        self.prt.setPageOrientation(1)
        self.prt.setPageMargins(6, 6, 6, 6, self.prt.Millimeter)

    def config(self, words: list, row, col, font='宋体', d_size=18):
        self.row = row + 1
        self.col = col + 1
        self.font = font
        # 计算页数
        self.sheet = int(len(words) / (row * col))
        if len(words) % (row * col) != 0:
            self.sheet += 1

        self.y_list = list()
        self.x_list = list()

        for i in range(self.col):
            self.x_list.append(int(self.mmToPix_x(284 / col * i)))
        for i in range(self.row):
            self.y_list.append(int(self.mmToPix_y(195 / row * i)))

        'wordA,wordB,xA,yA,xB,yB,sizeA,sizeB'
        self.words = list()
        width = self.x_list[1] - self.x_list[0]
        height = self.y_list[1] - self.y_list[0]
        p = QtGui.QPainter()
        for word, word2 in words:
            word_dict = dict()
            self.pat.setFont(QtGui.QFont(font, d_size))
            w_size = self.pat.fontMetrics().width(word)
            i = 0
            while w_size > width:
                i -= 1
                self.pat.setFont(QtGui.QFont(font, d_size + i))
                w_size = self.pat.fontMetrics().width(word)
                if i < -8:
                    break

            word_dict['xA'] = int((width - w_size) / 2)
            word_dict['yA'] = int((height - self.pat.fontMetrics().height()) / 2)

            # 注意：w_size被复用
            w_size = d_size + i
            word_dict['sizeA'] = w_size

            self.pat.setFont(QtGui.QFont(font, d_size))
            w_size = self.pat.fontMetrics().width(word2)
            i = 0
            while w_size > width:
                i -= 1
                self.pat.setFont(QtGui.QFont(font, d_size + i))
                w_size = self.pat.fontMetrics().width(word2)
                if i < -8:
                    break

            word_dict['xB'] = int((width - w_size) / 2)
            word_dict['yB'] = int((height - self.pat.fontMetrics().height()) / 2)

            # 注意：w_size被复用
            w_size = d_size + i
            word_dict['sizeB'] = w_size

            word_dict['wordA'] = word
            word_dict['wordB'] = word2

            self.words.append(word_dict)

    def mmToPix_x(self, x):
        rect: QtCore.QRect = self.prt.paperRect()
        width = rect.width()
        return int(width / 297 * x)

    def mmToPix_y(self, y):
        rect: QtCore.QRect = self.prt.paperRect()
        height = rect.height()
        return int(height / 210 * y)

    def print(self, words: list, row, col, font='宋体', d_size=18, preview=False):

        def print_word_a():
            pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)

            self.pat.setPen(pen)
            index = 0
            for n in range(self.sheet):
                for i in range(self.col):
                    self.pat.drawLine(self.x_list[i], 0,
                                      self.x_list[i], self.mmToPix_y(195))
                for i in range(self.row):
                    if i < self.row - 1 and index < len(self.words):
                        for col_index in range(self.col - 1):
                            if index >= len(self.words):
                                break
                            word_dict = self.words[index]
                            self.pat.setFont(QtGui.QFont(
                                self.font, word_dict['sizeA']))
                            self.pat.drawText(
                                word_dict['xA'] + self.x_list[col_index],
                                word_dict['yA'] + self.y_list[i] + self.mmToPix_y(5), word_dict['wordA'])

                            index += 1
                    self.pat.drawLine(0, self.y_list[i],
                                      self.mmToPix_x(284), self.y_list[i])

                if n < self.sheet - 1:
                    self.prt.newPage()

        def print_word_b():
            pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
            self.pat.setPen(pen)
            # 打印镜像
            index = 0
            for n in range(self.sheet):
                for i in range(self.row):
                    if i < self.row - 1 and index < len(self.words):
                        for col_index in range(self.col - 1):
                            if index >= len(self.words):
                                break
                            word_dict = self.words[index]
                            self.pat.setFont(QtGui.QFont(
                                self.font, word_dict['sizeB']))
                            self.pat.drawText(
                                word_dict['xB'] + self.x_list[self.col - col_index - 2],
                                word_dict['yB'] + self.y_list[i] + self.mmToPix_y(5), word_dict['wordB'])

                            index += 1

                if n < self.sheet - 1:
                    self.prt.newPage()

        if self.checkBox.checkState() == 0 or preview:
            if not self.pat.begin(self.prt):
                return
            self.config(words, row, col, font, d_size)
            print_word_a()
            self.prt.newPage()
            print_word_b()
            self.pat.end()
            return

        if not self.pat.begin(self.prt):
            return
        self.config(words, row, col, font, d_size)
        print_word_a()
        self.pat.end()
        if wordBMessageBox(self).exec() == 1:
            return
        if not self.pat.begin(self.prt):
            return
        self.config(words, row, col, font, d_size)
        print_word_b()
        self.pat.end()


class saveMessageBox(QtWidgets.QMessageBox):
    """生成一个保存提问窗口"""

    def __init__(self, w):
        super().__init__(w)
        self.setIcon(QtWidgets.QMessageBox.Question)
        self.setWindowTitle('保存')
        self.setText('<font size = "5">是否保存已更改的内容？</font>')
        self.y = self.addButton('保存(&S)', QtWidgets.QMessageBox.YesRole)
        self.y = self.addButton('不保存(&N)', QtWidgets.QMessageBox.NoRole)
        self.r = self.addButton('取消', QtWidgets.QMessageBox.RejectRole)


class wordBMessageBox(QtWidgets.QMessageBox):
    """生成一个翻面提示窗口"""

    def __init__(self, w):
        super().__init__(w)
        self.setIcon(QtWidgets.QMessageBox.Information)
        self.setWindowTitle('手动翻面')
        self.setText('<font size = "5">请以短边为轴心把纸翻到背面，并装进进纸器后，点击继续！</font>')
        self.y = self.addButton('继续(&p)', QtWidgets.QMessageBox.YesRole)
        self.r = self.addButton('取消', QtWidgets.QMessageBox.RejectRole)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    SailWordCard = core()
    SailWordCard.show()
    sys.exit(app.exec())
