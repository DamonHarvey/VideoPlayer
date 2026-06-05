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
    QLabel,
)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtGui import QAction


def convert_ms(milliseconds: int) -> str:

    seconds, ms = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


class VideoPlayer(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.init_window()
        self.init_player()

        self.init_menu_bar()

        self.init_playback_button()
        self.init_playback_widget()
        self.init_audio_widget()
        self.init_playback_speed_widget()

        self.init_main_widget()

    def init_window(self):
        self.setWindowTitle("Video Player")
        self.resize(QSize(1280, 720))

    def init_menu_bar(self):
        menu_bar = self.menuBar()
        if menu_bar is None:
            return

        self.menu_bar = menu_bar

        self.init_menu_bar_file()
        self.init_menu_bar_debug()

    def init_menu_bar_file(self):
        file_menu = self.menu_bar.addMenu("File")
        if file_menu is None:
            raise TypeError("file_menu is none")

        open_file = QAction("Open", self)
        open_file.triggered.connect(self.open_file)

        close_file = QAction("Close", self)
        close_file.triggered.connect(self.close_file)

        exit_app = QAction("Exit", self)
        exit_app.triggered.connect(lambda: self.close())

        file_menu.addAction(open_file)
        file_menu.addAction(close_file)
        file_menu.addSeparator()
        file_menu.addAction(exit_app)

    def init_menu_bar_debug(self):
        debug_menu = self.menu_bar.addMenu("Debug")
        if debug_menu is None:
            raise TypeError("debug_menu is none")

        get_file_position = QAction("Get file position", self)
        get_file_position.triggered.connect(
            lambda: print(f"Position: {self.media_player.position()}")
        )

        get_file_duration = QAction("Get file duration", self)
        get_file_duration.triggered.connect(
            lambda: print(f"Duration: {self.media_player.duration()}")
        )

        debug_menu.addAction(get_file_position)
        debug_menu.addAction(get_file_duration)

    def open_file(self):
        file_path = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            "",
            "Video Files (*.mp4);; Audio Files (*.mp3, *.flac, *.wav)",
        )
        self.media_player.setSource(QUrl.fromLocalFile(file_path[0]))

        # Makes video player show first frame.
        self.media_player.play()
        self.media_player.pause()

        self.playback_button.setText("Play")
        self.playback_speed_slider.setValue(100)

    def close_file(self):
        self.media_player.setSource(QUrl())

    def init_player(self):
        self.media_player = QMediaPlayer()

        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumSize(1280, 720)

        self.media_player.setVideoOutput(self.video_widget)

    def init_playback_button(self):
        playback_button = QPushButton()
        playback_button.setText("Play")
        playback_button.clicked.connect(self.set_playback)
        playback_button.setFixedSize(QSize(100, 30))
        self.playback_button = playback_button

    def set_playback(self):
        if not self.media_player.isPlaying():
            self.media_player.play()
            self.playback_button.setText("Pause")
        else:
            self.media_player.pause()
            self.playback_button.setText("Play")

    def init_playback_widget(self):

        layout = QGridLayout()
        container = QWidget()
        container.setLayout(layout)
        self.play_back_widget = container

        slider = QSlider(Qt.Orientation.Horizontal)

        self.media_player.durationChanged.connect(
            lambda: slider.setRange(0, self.media_player.duration())
        )

        slider.valueChanged.connect(
            lambda: self.media_player.setPosition(slider.value())
        )

        self.media_player.positionChanged.connect(self.on_position_change)

        self.position_slider = slider

        playback_position = QLabel(text="00:00:00")
        playback_duration = QLabel(text="00:00:00")
        playback_position.setFixedWidth(42)
        playback_duration.setFixedWidth(42)

        self.media_player.positionChanged.connect(
            lambda: playback_position.setText(convert_ms(self.media_player.position()))
        )

        self.media_player.durationChanged.connect(
            lambda: playback_duration.setText(convert_ms(self.media_player.duration()))
        )

        self.media_player.positionChanged.connect(self.check_end_of_video)

        layout.addWidget(playback_position, 0, 0)
        layout.addWidget(slider, 0, 1)
        layout.addWidget(playback_duration, 0, 2)

        container.setMaximumHeight(35)

    def check_end_of_video(self):
        if self.media_player.position() == self.media_player.duration():
            self.playback_button.setText("Play")

    def on_position_change(self):
        self.position_slider.blockSignals(True)
        self.position_slider.setValue(self.media_player.position())
        self.position_slider.blockSignals(False)

    def init_audio_widget(self):

        layout = QGridLayout()
        container = QWidget()
        container.setLayout(layout)
        self.volume_widget = container

        volume_slider = QSlider(Qt.Orientation.Horizontal)
        volume_slider.setRange(0, 100)
        volume_slider.setValue(100)
        volume_slider.setFixedWidth(75)

        volume_slider.valueChanged.connect(
            lambda: self.audio_output.setVolume(volume_slider.value() / 100)
        )

        volume_display = QLabel()
        volume_display.setText("100%")
        volume_display.setFixedWidth(28)
        volume_slider.valueChanged.connect(
            lambda: volume_display.setText(f"{volume_slider.value()}%")
        )

        title = QLabel(text="Volume:")

        layout.addWidget(title, 0, 0)
        layout.addWidget(volume_display, 0, 1, Qt.AlignmentFlag.AlignRight)
        layout.addWidget(volume_slider, 0, 2, Qt.AlignmentFlag.AlignLeft)

    def init_playback_speed_widget(self):

        layout = QGridLayout()
        container = QWidget()
        container.setLayout(layout)
        self.playback_speed_widget = container

        speed_slider = QSlider(Qt.Orientation.Horizontal)
        speed_slider.setRange(25, 200)
        speed_slider.setValue(100)
        speed_slider.setFixedWidth(75)

        speed_slider.valueChanged.connect(
            lambda: self.media_player.setPlaybackRate(speed_slider.value() / 100)
        )

        speed_display = QLabel()
        speed_display.setText(f"{1:.2f}")
        speed_display.setFixedWidth(28)
        speed_slider.valueChanged.connect(
            lambda: speed_display.setText(f"{speed_slider.value()/100:.2f}")
        )

        title = QLabel(text="Speed:")

        layout.addWidget(title, 0, 0)
        layout.addWidget(speed_display, 0, 1, Qt.AlignmentFlag.AlignRight)
        layout.addWidget(speed_slider, 0, 2, Qt.AlignmentFlag.AlignLeft)

        self.playback_speed_slider = speed_slider

    def init_main_widget(self):

        layout = QGridLayout()
        layout.addWidget(self.video_widget, 0, 0, 1, 3)
        layout.addWidget(self.play_back_widget, 1, 0, 1, 3)

        layout.addWidget(self.playback_button, 2, 1)
        layout.addWidget(self.volume_widget, 2, 2, Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.playback_speed_widget, 2, 0, Qt.AlignmentFlag.AlignLeft)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


def main():

    app = QApplication(sys.argv)
    window = VideoPlayer()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
