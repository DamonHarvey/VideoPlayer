import sys

from PyQt6.QtCore import QSize, QUrl, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QGridLayout
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget


class VideoPlayer(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.init_window()
        self.init_player()
        self.init_buttons()
        self.init_main_widget()

    def init_window(self):
        self.setWindowTitle("Video Player")
        self.resize(QSize(1280, 720))

    def init_player(self):
        self.media_player = QMediaPlayer()
        self.media_player.setSource(QUrl.fromLocalFile("video.mp4"))

        self.video_widget = QVideoWidget()
        self.media_player.setVideoOutput(self.video_widget)

        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

    def init_buttons(self):
        play_button = QPushButton()
        play_button.setText("Play")
        play_button.clicked.connect(lambda: self.media_player.play())
        play_button.setFixedSize(QSize(100, 30))
        self.play_button = play_button

        pause_button = QPushButton()
        pause_button.setText("Pause")
        pause_button.clicked.connect(lambda: self.media_player.pause())
        pause_button.setFixedSize(QSize(100, 30))
        self.pause_button = pause_button

    def init_main_widget(self):

        layout = QGridLayout()
        layout.addWidget(self.video_widget, 0, 0, 1, 2)
        layout.addWidget(self.play_button, 1, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.pause_button, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        #### testing
        button = QPushButton()
        button.setText("debug")

        button.clicked.connect(lambda: self.get_info())

        layout.addWidget(button, 2, 0)
        ####

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def get_info(self):

        # time frame in milliseconds
        print(f"{self.media_player.position()}/{self.media_player.duration()}")


def main():

    app = QApplication(sys.argv)
    window = VideoPlayer()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
