import sys

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QGridLayout


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("video player")

        self.init_buttons()

    def init_buttons(self):

        button = QPushButton()
        button.setText("click")
        button.clicked.connect(lambda: print("clicked"))
        button.setFixedSize(QSize(100, 30))

        button_two = QPushButton()
        button_two.setText("who")
        button_two.clicked.connect(lambda: print("clicked"))
        button_two.setFixedSize(QSize(100, 30))

        layout = QGridLayout()
        layout.addWidget(button, 0, 0)
        layout.addWidget(button_two, 0, 1)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


def main():

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
