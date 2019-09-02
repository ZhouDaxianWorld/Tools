# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox, QPushButton, QPlainTextEdit
from PyQt5.QtGui import QIcon
import re
from urllib.parse import urlparse

class CurlConvertHttp(object):

    def run(self, curlText, messageBox):
        request_header = {}
        request_url = ""
        if re.match("curl", curlText, re.I):

            # region 判断提交方法
            x_option = re.search(r"-X (.*?) ", curlText, re.I)
            d_option = re.search(r"--data", curlText, re.I)
            if x_option != None:
                request_method = x_option.group(1)
            elif d_option != None:
                request_method = 'POST'
            else:
                request_method = 'GET'
            # endregion

            # region 匹配请求url
            try:
                request_url = re.search(r"curl ['\"]((http|https).*?)['\"]", curlText, re.I).group(1)
            except AttributeError as e:
                print("请求URL不合法")
                messageBox.setText("请求URL不合法")
                messageBox.open()
                return False
            # endregion

            # region 匹配请求头
            try:
                for header in re.finditer(r"-H ['\"](.*?: (?!\s).*?)['\"]", curlText, re.I):
                    x = re.split(r":", header.group(1), maxsplit=1, flags=re.I)
                    request_header[x[0]] = x[1].strip()
            except Exception as e:
                print("报文头不合法")
                messageBox.setText("报文头不合法")
                messageBox.open()
                return False
            # endregion

            # region匹配数据
            data = re.search(r"--data ['\"](.*?)['\"]", curlText, re.I).group(1)

            urlParse = urlparse(request_url)
            httpStr = ""
            httpStr += request_method + " " + urlParse.path + "?" + urlParse.query + " HTTP/1.1" + "\r\n"
            httpStr += "Host: " + urlParse.netloc

            for key, value in request_header.items():
                httpStr += key + ": " + value + "\r\n"
            httpStr += "\r\n\r\n"
            httpStr += data
            return httpStr


class Fuzz(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.curlText = QPlainTextEdit("curl内容", self)
        self.curlText.resize(798, 300)
        self.curlText.move(0, 0)

        self.httpText = QPlainTextEdit("HTTP内容", self)
        self.httpText.resize(798, 300)
        self.httpText.move(0, 368)

        self.convertButton = QPushButton("转换", self)
        self.convertButton.resize(self.convertButton.sizeHint())
        self.convertButton.move(200, 310)
        self.convertButton.clicked.connect(self.convert)

        self.statusBar().showMessage("ready")
        self.resize(800, 800)
        self.center()
        self.setWindowTitle('Fuzz')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def convert(self):
        messageBox = QMessageBox(self)
        curlText = self.curlText.toPlainText()
        httpText = CurlConvertHttp().run(curlText, messageBox)
        self.httpText.setPlainText(httpText)

if __name__ == "__main__":
    # 每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
    app = QApplication(sys.argv)
    fuzz = Fuzz()
    sys.exit(app.exec_())