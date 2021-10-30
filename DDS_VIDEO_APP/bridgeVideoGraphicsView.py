
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

from PySide6 import QtMultimedia
from PySide6 import QtMultimediaWidgets

from PySide6.QtMultimedia import (QAudio, QAudioOutput, QMediaFormat, QMediaPlayer, QVideoFrame)
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem

from bridgeVideoGraphicsViewItemVideoSink import BridgeVideoGraphicsVideoItem
from bridgeVideoGraphicsViewItemVideoSink import BridgeVideoGraphicsVideoItemVideoSink
   
class BridgeVideoGraphicsView(QtWidgets.QGraphicsView):
    '''
    '''
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.url = None

        self.thescene = QtWidgets.QGraphicsScene()
        self.setScene(self.thescene)

        self.video_item = BridgeVideoGraphicsVideoItem()
        self.video_item.setPos(0,0)
        self.video_item.setSize(QtCore.QSize(100,200))
        self.video_item.setVisible(True)

        
        self.thescene.addItem(self.video_item)

        # -----------------------------------------------------
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.video_item)

        # -----------------------------------------------------
        self.videoSink = BridgeVideoGraphicsVideoItemVideoSink(self.player, self.video_item, self)
        self.player.setVideoSink(self.videoSink)

        self.video_item.videoSink().setSubtitleText("xxxx")
        
        self.show()

    def open_and_play_video(self, url):
        '''
        '''
        self.url = url
        self.player.setSource(url)
        self.player.play()

'''


player = new QMediaPlayer(this);

QGraphicsVideoItem *item = new QGraphicsVideoItem;
player->setVideoOutput(item);
graphicsView->scene()->addItem(item);
graphicsView->show();

player->setSource(QUrl("http://example.com/myclip4.ogv"));
player->play();




QGraphicsVideoItem *item = new QGraphicsVideoItem;
graphicsView->scene()->addItem(item);
graphicsView->show();
QImage img = QImage("images/qt-logo.png").convertToFormat(QImage::Format_ARGB32);
item->videoSink()->setVideoFrame(QVideoFrame(img));



'''