import sys
import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, \
    QGridLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculator")

        centralW = QWidget()
        self.setCentralWidget(centralW)

        mainLayout = QVBoxLayout(centralW)

        # Preview and Output Window
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setFocusPolicy(Qt.NoFocus)
        self.display.setAlignment(Qt.AlignRight)
        mainLayout.addWidget(self.display)

        # Grid
        grid = QGridLayout()
        mainLayout.addLayout(grid)

        # Buttons
        self.b0 = QPushButton("0")
        self.b1 = QPushButton("1")
        self.b2 = QPushButton("2")
        self.b3 = QPushButton("3")
        self.b4 = QPushButton("4")
        self.b5 = QPushButton("5")
        self.b6 = QPushButton("6")
        self.b7 = QPushButton("7")
        self.b8 = QPushButton("8")
        self.b9 = QPushButton("9")

        self.btimes = QPushButton("*")
        self.bdivided = QPushButton("/")
        self.bplus = QPushButton("+")
        self.bminus = QPushButton("-")

        self.bequal = QPushButton("=")
        self.bdot = QPushButton(".")
        self.bc = QPushButton("C")
        self.bb = QPushButton("<-")

        self.bd1 = QPushButton(" ")
        self.bd2 = QPushButton(" ")

        # adding the buttons to the grid
        grid.addWidget(self.bb, 0 , 0)
        grid.addWidget(self.bd1, 0, 1)
        grid.addWidget(self.bd2, 0, 2)
        grid.addWidget(self.bc, 0, 3)

        grid.addWidget(self.b0, 1, 0)
        grid.addWidget(self.b1, 1, 1)
        grid.addWidget(self.b2, 1, 2)
        grid.addWidget(self.bdivided, 1, 3)

        grid.addWidget(self.b3, 2, 0)
        grid.addWidget(self.b4, 2, 1)
        grid.addWidget(self.b5, 2, 2)
        grid.addWidget(self.btimes, 2, 3)

        grid.addWidget(self.b6, 3, 0)
        grid.addWidget(self.b7, 3, 1)
        grid.addWidget(self.b8, 3, 2)
        grid.addWidget(self.bminus, 3, 3)

        grid.addWidget(self.b9, 4, 0)
        grid.addWidget(self.bdot, 4, 1)
        grid.addWidget(self.bequal, 4, 2)
        grid.addWidget(self.bplus, 4, 3)

        # ------------------------ Logic ------------------------ #

        # Initialize calculator variables
        self.output = ""
        self.operator = ""
        self.num1 = ""
        self.num2 = ""
        self.calculated = ""

        # function assignment
        self.b0.clicked.connect(lambda: self.num_pressed("0"))
        self.b1.clicked.connect(lambda: self.num_pressed("1"))
        self.b2.clicked.connect(lambda: self.num_pressed("2"))
        self.b3.clicked.connect(lambda: self.num_pressed("3"))
        self.b4.clicked.connect(lambda: self.num_pressed("4"))
        self.b5.clicked.connect(lambda: self.num_pressed("5"))
        self.b6.clicked.connect(lambda: self.num_pressed("6"))
        self.b7.clicked.connect(lambda: self.num_pressed("7"))
        self.b8.clicked.connect(lambda: self.num_pressed("8"))
        self.b9.clicked.connect(lambda: self.num_pressed("9"))

        self.bplus.clicked.connect(lambda: self.operator_pressed("+"))
        self.bminus.clicked.connect(lambda: self.operator_pressed("-"))
        self.btimes.clicked.connect(lambda: self.operator_pressed("*"))
        self.bdivided.clicked.connect(lambda: self.operator_pressed("/"))

        self.bequal.clicked.connect(self.calculate)
        self.bdot.clicked.connect(lambda: self.dot_pressed())
        self.bc.clicked.connect(self.clear)
        self.bb.clicked.connect(self.backspace)

    # functions
    def num_pressed(self, n):
        if not self.operator:
            self.num1 += n
            self.output += n
            self.display.setText(self.output)
        else:
            self.num2 += n
            self.output += n
            self.display.setText(self.output)

    def operator_pressed(self, p):
        if not self.operator:
            if p == "-" and self.num1 == "":
                self.num1 = "-"
                self.output += "-"
                self.display.setText(self.output)
            else:
                self.operator = p
                self.output += self.operator
                self.display.setText(self.output)
        else:
            if p == "-" and self.num2 == "":
                self.num2 = "-"
                self.output += "-"
                self.display.setText(self.output)
            else:
                self.clear()
                self.display.setText("Error: Invalid operation")
                return

    def dot_pressed(self):
        if not self.operator:
            if "." not in self.num1:
                self.num1 += "."
                self.output += "."
        else:
            if "." not in self.num2:
                self.num2 += "."
                self.output += "."
        self.display.setText(self.output)

    def calculate(self):
        if self.operator == "/" :
            if float(self.num2) != 0:
                self.calculated = float(self.num1) / float(self.num2)
            else:
                self.clear()
                self.display.setText("Error: Division by zero")
                return
        elif self.operator == "*" :
            self.calculated = float(self.num1) * float(self.num2)
        elif self.operator == "+" :
            self.calculated = float(self.num1) + float(self.num2)
        elif self.operator == "-" :
            self.calculated = float(self.num1) - float(self.num2)

        self.output = f"{self.num1}{self.operator}{self.num2}={self.calculated}"
        self.display.setText(self.output)

    def clear(self):
        self.num1 = ""
        self.num2 = ""
        self.operator = ""
        self.output = ""
        self.calculated = ""
        self.display.setText("")

    def backspace(self):
        if self.output:
            self.output = self.output[:-1]
            if self.num2:
                if self.num2 == "-":
                    self.num2 = ""
                else:
                    self.num2 = self.num2[:-1]
            elif self.operator:
                self.operator = ""
            elif self.num1:
                if self.num1 == "-":
                    self.num1 = ""
                else:
                    self.num1 = self.num1[:-1]

            self.display.setText(self.output)

app = QApplication(sys.argv)

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)
qss_path = os.path.join(base_path, "style.qss")

with open(qss_path, "r") as f:
    app.setStyleSheet(f.read())
window = MainWindow()
window.show()

app.exec()