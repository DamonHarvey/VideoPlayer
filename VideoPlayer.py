import sys

from PyQt6.QtCore import QSize, QUrl, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QGridLayout,
    QSlider,
    QFileDialog,
)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtGui import QAction


class VideoPlayer(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.init_window()
        self.init_menu_bar()
        self.init_player()
        self.init_buttons()
        self.init_slider()

        self.debug()

        self.init_main_widget()

    def init_window(self):
        self.setWindowTitle("Video Player")
        self.resize(QSize(1280, 720))

    def init_menu_bar(self):
        menu_bar = self.menuBar()
        if menu_bar is None:
            return
        file_menu = menu_bar.addMenu("&Files")
        if file_menu is None:
            return
        open_file = QAction("&Open", self)
        open_file.triggered.connect(self.open_file)

        close_file = QAction("&Close", self)
        close_file.triggered.connect(self.close_file)

        exit_app = QAction("&Exit", self)
        exit_app.triggered.connect(lambda: self.close())

        file_menu.addAction(open_file)
        file_menu.addAction(close_file)
        file_menu.addSeparator()
        file_menu.addAction(exit_app)

    def open_file(self):
        file_path = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            "",
            "Video Files (*.mp4);; Audio Files (*.mp3, *.flac, *.wav)",
        )
        self.media_player.setSource(QUrl.fromLocalFile(file_path[0]))

    def close_file(self):
        self.media_player.setSource(QUrl())

    def init_player(self):
        self.media_player = QMediaPlayer()

        self.video_widget = QVideoWidget()
        self.media_player.setVideoOutput(self.video_widget)

        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

    def init_buttons(self):
        play_button = QPushButton()
        play_button.setText("Play")
        play_button.clicked.connect(self.set_playback)
        play_button.setFixedSize(QSize(100, 30))
        self.play_button = play_button

    def set_playback(self):
        if not self.media_player.isPlaying():
            self.media_player.play()
            self.play_button.setText("Pause")
        else:
            self.media_player.pause()
            self.play_button.setText("Play")

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
        layout.addWidget(self.video_widget, 0, 0, 1, 1)
        layout.addWidget(self.play_button, 2, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.position_slider, 1, 0, 1, 1)

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
