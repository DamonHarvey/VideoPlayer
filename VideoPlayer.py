import sys

from PyQt6.QtCore import QSize, QUrl, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QGridLayout,
    QSlider,
)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget


class VideoPlayer(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.init_window()
        self.init_player()
        self.init_buttons()
        self.init_slider()

        self.debug()

        self.init_main_widget()

    def init_window(self):
        self.setWindowTitle("Video Player")
        self.resize(QSize(1280, 720))

    def init_player(self):
        self.media_player = QMediaPlayer()
        self.media_player.setSource(QUrl.fromLocalFile(r"VideoPlayer\video.mp4"))

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

    def init_slider(self):
        slider = QSlider(Qt.Orientation.Horizontal)

        self.media_player.durationChanged.connect(
            lambda: slider.setRange(0, self.media_player.duration())
        )

        slider.valueChanged.connect(
            lambda: self.media_player.setPosition(slider.value())
        )

        self.media_player.positionChanged.connect(self.on_position_change)

        self.position_slider = slider

    def on_position_change(self):
        self.position_slider.blockSignals(True)
        self.position_slider.setValue(self.media_player.position())
        self.position_slider.blockSignals(False)

    def init_main_widget(self):

        layout = QGridLayout()
        layout.addWidget(self.video_widget, 0, 0, 1, 2)
        layout.addWidget(self.play_button, 2, 0, Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.pause_button, 2, 1, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.position_slider, 1, 0, 1, 2)

        #### debug
        # layout.addWidget(self.debug_button, 3, 0)
        ####

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def debug(self):
        button = QPushButton()
        button.setText("debug")

        button.clicked.connect(
            lambda: print(
                f"{self.media_player.position()}/{self.media_player.duration()}"
            )
        )

        self.debug_button = button


def main():

    app = QApplication(sys.argv)
    window = VideoPlayer()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
