#-*- coding:utf-8 -*-
#!/usr/bin/env python
from PyQt5.QtWidgets import QMainWindow,QApplication,QTextEdit,QTextBrowser,QPushButton,QMessageBox,QLabel,QComboBox
from PyQt5.QtGui import QIcon
import sys,pymysql,configparser
class read_excel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        # 加解密按钮
        self.ButtonClicked1()
        self.ButtonClicked2()
        
    def initUI(self):
        self.setWindowTitle('pymysql connector v1.0')
        self.setWindowIcon(QIcon('images/favicon.ico'))
        #self.resize(600, 650)
        # 固定窗口大小
        self.setFixedSize(600, 650)
        # windows窗口的位置
        self.move(700, 200)
        # 文本框位置
        self.text_area1 = QTextEdit(self)
        # 窗口位置
        self.text_area1.move(20, 80)
        self.text_area1.resize(440,80)
        self.text_area1.setStyleSheet("font-weight: bold; font-size: 18px; font-family: Consolas")
        #文本框位置
        self.text_area2 = QTextBrowser(self)
        #窗口位置
        self.text_area2.move(20, 180)
        #窗口区域大小
        self.text_area2.resize(440, 440)
        self.text_area2.setStyleSheet("font-weight: thin; font-size: 14px; font-family: Consolas")

        btn1 = QPushButton('执行SQL', self)
        btn1.move(480, 80)
        btn1.resize(100,80)
        btn1.setStyleSheet("font-weight: bold; font-size: 20px; font-family: Microsoft YaHei UI")

        btn2 = QPushButton('全部清除', self)
        btn2.move(480, 180)
        btn2.resize(100,80)
        btn2.setStyleSheet("font-weight: bold; font-size: 20px; font-family: Microsoft YaHei UI")
        
        # 创建enceypt_type文本标签
        self.enceypt_type_label = QLabel(self)
        self.enceypt_type_label.move(10,20)
        self.enceypt_type_label.resize(65,30)
        self.enceypt_type_label.setText('数据库地址:')
        self.enceypt_type_label.setStyleSheet("font-weight: thin; font-size: 12px; font-family: Microsoft YaHei UI")
        
        # 创建enceypt_type下拉框
        self.denceypt_type_option = QComboBox(self)
        self.denceypt_type_option.move(80,20)
        self.denceypt_type_option.resize(230,30)

        # 设置下拉框可选项
        #self.denceypt_type_option.addItems(['Base64','MD5','不加密'])
        self.denceypt_type_option.addItems(['本地数据库','远程数据库'])
        # 设置下拉框的默认值
        self.denceypt_type_option.setCurrentIndex(0)
        self.denceypt_type_option.setStyleSheet("font-weight: thin; font-size: 12px; font-family: Microsoft YaHei UI")
        
        self.show()
        self.statusBar().showMessage('兴趣永远是最好的老师！')
        btn1.clicked.connect(self.ButtonClicked1)
        btn2.clicked.connect(self.ButtonClicked2)

    # 获取索引号
    def get_encrypt_index(self):
        encrypt_index = self.denceypt_type_option.currentIndex()
        return encrypt_index

    # 获取索引内容
    def get_encrypt_Text(self):
        encrypt_text = self.denceypt_type_option.currentText()
        return encrypt_text

    # 加密按钮
    def ButtonClicked1(self):
        textcontenct = self.text_area1.toPlainText()
        # 过滤掉空值
        if textcontenct == '':
            pass
        else:
            self.text_area2.clear()
            # 获取输入的sql
            encrypt_text = self.get_encrypt_Text()
            print('所选择的数据库为:',encrypt_text)
            # 加密主窗口
            #result = hashlib.md5(textcontenct.encode(encoding='UTF-8')).hexdigest().upper()
            result=self.exec_pymysql(textcontenct)
            # 获取md5加密值大写
            self.text_area2.append(str(result))

            self.statusBar().showMessage("心灵鸡汤接口预留内容")

    # 清除按钮
    def ButtonClicked2(self):
        self.text_area1.clear()
        self.text_area2.clear()
        # 解密主窗口
        # self.statusBar().showMessage("清除成功！")

    # pymysql engine to run sql command.
    def exec_pymysql(self,str_sql):
        try:
            config = configparser.ConfigParser() 
            config.read("dbconf.cfg")
            key_host=config.get("dockerhost", "host") 
            key_port=config.getint("dockerhost", "port") 
            key_user=config.get("dockerhost", "dbuser")
            key_passwd=config.get("dockerhost", "dbpasswd")
            key_db=config.get("dockerhost", "db")
            conn = pymysql.connect(host=key_host,port=key_port,user=key_user, passwd=key_passwd, db=key_db,charset='utf8mb4')
            cur = conn.cursor()
            cur.execute(str_sql)
            conn.commit()
            conn.close()
            return cur.fetchall()
        except Exception as ERRORS:
            return ERRORS

    #自定义退出事件
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '提示', "你确定要退出么?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = read_excel()
    sys.exit(app.exec_())
