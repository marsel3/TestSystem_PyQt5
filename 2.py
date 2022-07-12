import sys
import sqlite3
import datetime
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QWidget


# Первый класс. Окно регистрации
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.FirstWidget()

    def FirstWidget(self):
        self.setGeometry(0, 0, 300, 150)
        self.setWindowTitle('Регистрация')

        self.lbl = QLabel(self)
        self.lbl.setText('Введите фамилию')
        self.lbl.move(20, 20)

        self.first_input = QLineEdit(self)
        self.first_input.move(120, 18)
        self.first_input.resize(120, 20)

        self.btn = QPushButton('Начать', self)
        self.btn.move(170, 100)

        self.btn.clicked.connect(self.registr)

    # Переход к новому классу(новому окну). Закрытие регистрационного окна
    def registr(self):
        if self.first_input.text() != '':
            self.second_form = MyWidgetMain(self.first_input.text())
            self.second_form.show()
            self.close()


# Второй класс. Класс с вопросами и результатом
class MyWidgetMain(QMainWindow):
    def __init__(self, name):
        super().__init__()
        uic.loadUi('2.ui', self)
        self.first = datetime.datetime.now()
        self.tabWidget.setTabEnabled(1, False)
        self.progress_sum = 0
        self.m1 = []
        self.k = 0
        self.max_score = 0
        self.name = name
        self.datebase()
        self.textBrowser.append(self.res[self.k][0])
        self.pushButton.clicked.connect(self.questions)
        self.pushButton_2.clicked.connect(self.close_programm)

    # Считывание вопроса, ответа, балла из БД
    def datebase(self):
        con = sqlite3.connect('server.sqlite')
        cur = con.cursor()
        self.res = cur.execute("""SELECT question, answer, score FROM questions""").fetchall()
        for i in self.res:
            self.max_score += i[2]
        self.progress = round(100 / len(self.res))
        con.close()

    # Вывод вопроса на экран
    def questions(self):
        if self.lineEdit.text() != '':
            self.progress_sum += self.progress
            self.progressBar.setValue(self.progress_sum)
            if self.lineEdit.text().strip().lower() == self.res[self.k][1]:
                self.m1.append(int(self.res[self.k][2]))
            else:
                self.m1.append(0)
            self.k = self.k + 1
            if self.k == len(self.res):
                self.test_end()
            else:
                self.lineEdit.setText('')
                self.textBrowser.clear()
                self.textBrowser.append(self.res[self.k][0])

    # Подведение результата.
    def test_end(self):
        self.second = datetime.datetime.now()
        self.time = self.second - self.first
        self.score = round(sum(self.m1) / self.max_score * 100)
        self.grade = self.grades(self.score)
        self.tab_result()
        self.tabWidget.setTabEnabled(1, True)
        self.tabWidget.setTabEnabled(0, False)
        self.save()

    # Оформление результата.
    def tab_result(self):
        self.time = str(self.time).split(':')
        self.second = int(self.time[-1][:(self.time[-1]).index(".")])
        self.minute = int(self.time[-2])
        self.label_2.setText(f'Всего заданий в тесте: {len(self.m1)}')
        self.label_3.setText(f'Из них правильно: {len(self.m1) - self.m1.count(0)}')
        self.label_4.setText(f'Тест пройден за {self.minute} минут {self.second} секунд')
        self.label_5.setText(f'Набрано балов {sum(self.m1) - self.m1.count(0)} из {self.max_score}'
                             f' возможных. \nВаш результат {self.score}%')
        self.label_6.setText(f'Ваша оценка: {self.grade}')

    # Выставление оценки по процентам
    def grades(self, score):
        if score > 84:
            return 5
        elif score > 70:
            return 4
        elif score >= 50:
            return 3
        else:
            return 2

    # Сохранение результата в текстовый файл.
    def save(self):
        dt = datetime.datetime.now()
        self.writeFile = open('results.txt', 'a+', encoding='utf-8')
        self.writeFile.write('Сохранение от {}г-{}м-{}д {}ч:{}м:{}с\n"'.format(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second))
        self.writeFile.write(f'Ученик {self.name} набрал {self.score} баллов и получил оценку {self.grade}'
                             f'\nТест пройден за {self.minute} минут {self.second} секунд')
        self.writeFile.write('"\n\n')
        self.writeFile.close()

    # Завершение программы
    def close_programm(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())