import sys
import random
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QMainWindow, QWidget, QPushButton

words = [
    ('apple','사과'), ('bear','곰'), ('cat','고양이'), ('dog','개'), ('fire','불'), ('grape','포도')
]

day1 = [('hotel','호텔')]
day2 = [('ice','얼음')]
day3 = [('juice','쥬스')]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initGUI()

    def initGUI(self):
        self.childWindow = None

        lblTxtTitle = QLabel("TOEIC 단어 테스트 프로그램입니다.", self)
        lblTxtTitle.move(50, 50)
        lblTxtDay = QLabel("Day : ", self)
        lblTxtDay.move(50, 100)
        self.leDay = QLineEdit("0", self)
        self.leDay.move(100, 100)
        lblTxtTime = QLabel("Time : ", self)
        lblTxtTime.move(50, 150)
        self.leLimitTime = QLineEdit("0", self)
        self.leLimitTime.move(100, 150)

        self.btnStart = QPushButton("Start", self)
        self.btnStart.clicked.connect(self.onBtnClicked)
        self.btnStart.move(150, 200)

        self.setWindowTitle("TOEIC Word")
        self.setGeometry(200, 200, 400, 400)
        self.show()

    def onBtnClicked(self):
        self.close()
        if self.childWindow == None:
            day = self.leDay.text()
            limitTime = self.leLimitTime.text()

            self.childWindow = TestWindow(day, limitTime)
            self.childWindow.show()
        else:
            self.childWindow.close()
            self.childWindow = None

class TestWindow(QWidget):
    def __init__(self, day, limitTime):
        super().__init__()
        self.initGUI()
        self.initQuiz()
        self.nextWord()

        # todo
        self.day = day
        self.time = limitTime

    def initGUI(self):
        self.lblOrder = QLabel("1 번째 문제", self)
        self.lblOrder.move(50, 25)

        self.lblLimitTime = QLabel("--:--:--", self)
        self.lblLimitTime.move(325, 25)

        self.lblTitle = QLabel("다음 단어를 영어일 경우에는 한국어로,\n 한국어일 경우에는 영어로 입력하세요.", self)
        self.lblTitle.move(50, 75)

        lblProblem = QLabel("Problem : ", self)
        lblProblem.move(50, 150)

        self.lblQuestion = QLabel("Question", self)
        self.lblQuestion.move(50, 200)
        lblAnswer = QLabel("Answer : ", self)
        lblAnswer.move(50, 250)
        self.leAnswer = QLineEdit(self)
        self.leAnswer.move(50, 275)
        self.leAnswer.resize(300, 25)
        self.leAnswer.returnPressed.connect(self.onPressedEnterKey)

        lblTxtResult = QLabel("Result : ", self)
        lblTxtResult.move(50, 325)
        self.lblResult = QLabel("-", self)
        self.lblResult.move(100, 325)
        self.lblResult.resize(100, 25)

        self.setWindowTitle("TOEIC Word Quiz")
        self.setGeometry(200, 200, 400, 400)

    def initQuiz(self):
        self.korWords = []
        self.engWords = []
        self.wrongWords = []
        self.rnList = []

        random.shuffle(words)
        
        for (eng, kor) in words:
            self.engWords.append(eng)
            self.korWords.append(kor)

        self.currentIndex = 0
        self.cntCorrect = 0
        self.cntWrong = 0

    def nextWord(self):
        rn = random.randint(0, 1)
        if self.currentIndex < len(words):
            q = ""
            if rn == 1:
                q = self.korWords[self.currentIndex]
                
            else:
                q = self.engWords[self.currentIndex]
            
            self.lblOrder.setText("{} 번째 문제".format(self.currentIndex +1))
            self.lblQuestion.setText(q)
            self.rnList.append(rn)
        else :
            # for debugging
            print("문제 ==>", words)
            print("영어 ==>", self.engWords)
            print("한글 ==>", self.korWords)
            print("랜덤 숫자 리스트[1:한->영, 0:영->한] ==>", self.rnList)
            print("틀린 답 리스트(index, 정답, 적은것) ==>", self.wrongWords)

            reply = QtWidgets.QMessageBox.question(self, "TOEIC 단어 테스트", "모든 문제가 제출되었습니다.\n다시 하시겠습니까?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.initQuiz()
                self.nextWord()
            else:
                self.close()
                exit(0)

    def onPressedEnterKey(self):
        answer = self.leAnswer.text()
        self.leAnswer.setText("")
        
        correctAnswer = ""
        
        rn = self.rnList[self.currentIndex]

        if rn == 1:
            correctAnswer = self.engWords[self.currentIndex]

        else:
            correctAnswer = self.korWords[self.currentIndex]

        if answer == correctAnswer:
            self.lblResult.setText("정답")
            self.cntCorrect += 1
        else:
            self.lblResult.setText("오답")
            self.cntWrong += 1
            self.wrongWords.append((self.currentIndex, correctAnswer, answer))

        self.currentIndex += 1
        self.nextWord()

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    #win = QuizWindow()
    app.exec()

if __name__ == "__main__":
    main()