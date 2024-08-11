from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem, QVideoWidget

from bridgeMediaPlayerVideoSink import BridgeMediaPlayerVideoSink


class BridgeVideoGraphicsView(QtWidgets.QGraphicsView):
    """ """

    def __init__(self, parent=None):
        QtWidgets.QGraphicsView.__init__(self, parent)

        self.main_window = None
        self.url = None

        self.the_scene = QtWidgets.QGraphicsScene()
        self.setScene(self.the_scene)

        self.video_item = QGraphicsVideoItem()
        self.video_item.setPos(0, 0)
        self.video_item.setSize(self.eval_video_item_size())
        self.video_item.setVisible(True)

        self.the_scene.addItem(self.video_item)

        # -----------------------------------------------------
        self.player = QMediaPlayer()

        # self.player.setVideoOutput(self.video_item)

        self.player_video_sink = BridgeMediaPlayerVideoSink(self)
        self.player.setVideoSink(self.player_video_sink)
        # -----------------------------------------------------

        self.show()

    def set_main_window(self, main_window):
        """ """
        self.main_window = main_window
        self.video_item.setSize(self.eval_video_item_size())

    def eval_video_item_size(self):
        """ """
        video_frame_size = (1280, 720)
        w = video_frame_size[0]
        h = video_frame_size[1]

        view_w = self.width()
        view_h = self.height()

        factor = max(w / view_w, h / view_h)

        ww = int(w / factor)
        hh = int(h / factor)

        return QtCore.QSize(ww, hh)

    def open_and_play_video(self, url):
        """ """
        self.url = url
        self.player.setSource(url)
        self.player.play()
