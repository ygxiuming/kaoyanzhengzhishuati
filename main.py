import json
import sys

from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog
from qtpy import uic


class MyWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.ui = uic.loadUi("./UI/tiku.ui")
        self.ui.selectbutton.clicked.connect(self.get_tiku_title)
        self.ui.comboBox1.currentTextChanged.connect(self.combobox1_changed)
        self.ui.comboBox2.currentTextChanged.connect(self.combobox2_changed)
        self.ui.comboBox3.currentTextChanged.connect(self.show_question)
        # self.ui.submition.clicked.connect(self.submit)
        # self.ui.showresult.clicked.connect(self.submit)

    #     选项触发事件
        self.ui.checkBoxA.stateChanged.connect(lambda state, extraParam=1: self.checkboxchange(state, extraParam))
        self.ui.checkBoxB.stateChanged.connect(lambda state, extraParam=2: self.checkboxchange(state, extraParam))
        self.ui.checkBoxC.stateChanged.connect(lambda state, extraParam=3: self.checkboxchange(state, extraParam))
        self.ui.checkBoxD.stateChanged.connect(lambda state, extraParam=4: self.checkboxchange(state, extraParam))

        self.ui.pasttimu.clicked.connect(self.pasttimu)
        self.ui.nexttimu.clicked.connect(self.nexttimu)

        self.ui.submition.clicked.connect(self.submit)
        self.ui.showresult.clicked.connect(self.show_result)





    def get_tiku_title(self):
        path = QFileDialog.getOpenFileName(window, '打开文件', '', 'All Files (*.*)')[0]
        print(path)

        with open(path,'rb') as f:
            self.data = json.load(f)
        self.ui.title.setText(self.data['title'])

        com1 = list(self.data.keys())
        com1.pop(0)
        print(com1)
        for i in com1:
            self.ui.comboBox1.addItem(i)
            width = self.ui.comboBox1.view().sizeHintForColumn(0) + self.ui.comboBox1.view().verticalScrollBar().sizeHint().width()
            self.ui.comboBox1.view().setMinimumWidth(width)






    def combobox1_changed(self,text):
        print(text)
        # print(self.ui.comboBox3.currentText())

        self.ui.comboBox2.clear()
        for i in self.data[self.ui.comboBox1.currentText()]:
            self.ui.comboBox2.addItem(i)
            width = self.ui.comboBox2.view().sizeHintForColumn(0) + self.ui.comboBox2.view().verticalScrollBar().sizeHint().width()
            self.ui.comboBox2.view().setMinimumWidth(width)


    def combobox2_changed(self,text):
        self.ui.comboBox3.clear()
        if text == '':
            print(1)
        else:
            for i in self.data[self.ui.comboBox1.currentText()][self.ui.comboBox2.currentText()]:
                self.ui.comboBox3.addItem(i)





    def show_question(self,text):
        id = self.ui.comboBox3.currentText()
        length = len(self.ui.comboBox3)
        if text == '':
            print(1)
        else:
            self.ui.question.setText(
                f'{id}/{length}:\n   ' +
                self.data[self.ui.comboBox1.currentText()][self.ui.comboBox2.currentText()][self.ui.comboBox3.currentText()]['title']
                + '\n\n' + '————修明制作，开源软件，请勿付费\nhttps://github.com/ygxiuming/kaoyanzhengzhishuati'
            )
            self.question = self.data[self.ui.comboBox1.currentText()][self.ui.comboBox2.currentText()][self.ui.comboBox3.currentText()]
            self.ui.xuanxiang.clear()
            self.ui.xuanxiang.append(self.question['type'])
            for i in self.question['xuanxiang']:
                self.ui.xuanxiang.append(i)

        self.ui.checkBoxA.setChecked(False)
        self.ui.checkBoxB.setChecked(False)
        self.ui.checkBoxC.setChecked(False)
        self.ui.checkBoxD.setChecked(False)



    def checkboxchange(self,state,x):
        if state == 2:
            question_type = self.question['type']
            if question_type == '单选':
                type = 1
            else:
                type = 4

            if type == 1:
                self.ui.checkBoxA.setChecked(False)
                self.ui.checkBoxB.setChecked(False)
                self.ui.checkBoxC.setChecked(False)
                self.ui.checkBoxD.setChecked(False)
                if x == 1:self.ui.checkBoxA.setChecked(True)
                elif x == 2:self.ui.checkBoxB.setChecked(True)
                elif x == 3:self.ui.checkBoxC.setChecked(True)
                elif x == 4:self.ui.checkBoxD.setChecked(True)


    def yourchoose(self):
        choose = []
        if self.ui.checkBoxA.isChecked():choose.append('A')
        if self.ui.checkBoxB.isChecked():choose.append('B')
        if self.ui.checkBoxC.isChecked():choose.append('C')
        if self.ui.checkBoxD.isChecked():choose.append('D')

        return choose

    def submit(self):
        yourchoose = self.yourchoose()
        truechoose = self.data[self.ui.comboBox1.currentText()][self.ui.comboBox2.currentText()][self.ui.comboBox3.currentText()]['right_value']
        trues = ''
        your = ''
        for i in truechoose: trues += i
        for i in yourchoose: your += i
        if set(yourchoose) == set(truechoose):
            print("恭喜你做对了！！！")

            self.ui.xuanxiang.append(f'\n\n你的选项是：{your}\n正确选项：{trues}\n\n恭喜你做对了！！！')
            self.show_result()
            self.nexttimu()

        else:
            self.ui.xuanxiang.append(f'\n\n你的选项是：{your}\n正确选项：{trues}\n\n加油哦，你做错了')
            self.show_result()
    def pasttimu(self):
        self.ui.jiexi.clear()
        id = self. ui.comboBox3.currentText()
        if int(id) >= 1:id = str(int(id) - 1)
        else:id = str(1)
        self.ui.comboBox3.setCurrentText(id)

    def nexttimu(self):
        self.ui.jiexi.clear()
        id = self.ui.comboBox3.currentText()
        length = len(self.ui.comboBox3)
        if int(id) <= int(length) - 1:
            id = str(int(id) + 1)
        self.ui.comboBox3.setCurrentText(id)


    def show_result(self):
        truechoose = self.data[self.ui.comboBox1.currentText()][self.ui.comboBox2.currentText()][self.ui.comboBox3.currentText()]['right_value']
        trues = ''
        for i in truechoose: trues += i
        self.ui.jiexi.clear()
        self.ui.jiexi.insertHtml('<p>正确答案：{}</p> <br>'.format(trues))
        self.ui.jiexi.insertHtml('<p>解析：\n    </p><br>' )
        self.ui.jiexi.insertHtml(self.data[self.ui.comboBox1.currentText()][self.ui.comboBox2.currentText()][self.ui.comboBox3.currentText()]['jiexi'])





if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyWindow()
    window.ui.show()

    # app.exec()
    sys.exit(app.exec_())