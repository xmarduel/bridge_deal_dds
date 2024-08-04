"""PySide6 Multimedia player example"""

import sys
from PySide6 import QtWidgets
from PySide6.QtCore import QStandardPaths, Qt, Slot
from PySide6.QtGui import QAction, QIcon, QKeySequence, QScreen
from PySide6.QtWidgets import (QTabWidget, QWidget, QDialog, QFileDialog, QMainWindow, QSlider, QStyle, QToolBar)
from PySide6.QtMultimedia import (QAudio, QAudioOutput, QMediaFormat, QMediaPlayer)
from PySide6.QtMultimediaWidgets import QVideoWidget


def get_supported_mime_types():
    result = []
    for f in QMediaFormat().supportedFileFormats(QMediaFormat.Decode):
        mime_type = QMediaFormat(f).mimeType()
        result.append(mime_type.name())
    return result


class BridgeVideoWidget(QWidget):

    def __init__(self, main_win):
        super().__init__(main_win)

        self.main_win = main_win
        self.url = None

        self._audio_output = QAudioOutput()
        self._player = QMediaPlayer()
        self._player.setAudioOutput(self._audio_output)

        self._player.errorOccurred.connect(self._player_error)

        tool_bar = QToolBar()
        self.main_win.addToolBar(tool_bar)

        style = self.style()
        icon = QIcon.fromTheme("media-playback-start.png",
                               style.standardIcon(QStyle.SP_MediaPlay))
        self._play_action = tool_bar.addAction(icon, "Play")
        self._play_action.triggered.connect(self._player.play)

        icon = QIcon.fromTheme("media-playback-pause.png",
                               style.standardIcon(QStyle.SP_MediaPause))
        self._pause_action = tool_bar.addAction(icon, "Pause")
        self._pause_action.triggered.connect(self._player.pause)

        self._video_widget = QVideoWidget()
        self._player.playbackStateChanged.connect(self.update_buttons)
        self._player.setVideoOutput(self._video_widget)

        self.update_buttons(self._player.playbackState())

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().addWidget(self._video_widget)


    def closeEvent(self, event):
        self._ensure_stopped()
        event.accept()

    def open_and_play_video(self, url):
        '''
        '''
        self.url = url
        self._player.setSource(url)
        self._player.play()

    @Slot()
    def _ensure_stopped(self):
        if self._player.playbackState() != QMediaPlayer.StoppedState:
            self._player.stop()

    def update_buttons(self, state):
        #self._play_action.setEnabled(True)
        #self._pause_action.setEnabled(state == QMediaPlayer.PlayingState)
        pass

    @Slot(QMediaPlayer.Error, str)
    def _player_error(self, error, error_string):
        print(error_string, file=sys.stderr)


