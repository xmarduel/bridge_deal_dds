
from PySide6 import QtCore, QtGui, QtWidgets, QtMultimedia
from PySide6.QtGui import QPaintDevice, QPainter, QPixmap
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem
from PySide6.QtWidgets import QGraphicsItem, QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsView, QStyleOptionGraphicsItem, QWidget
   
from PySide6.QtMultimedia import QMediaPlayer, QVideoFrame, QVideoFrameFormat
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem


class BridgeVideoGraphicsVideoItem(QGraphicsVideoItem):
    '''
    '''
    def __init__(self):
        super().__init__()

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        '''
        '''
        super().paint(painter, option, widget)


class BridgeVideoGraphicsVideoItemVideoSink(QtMultimedia.QVideoSink):
    '''
    '''
    def __init__(self, player: QMediaPlayer, video_item: QGraphicsVideoItem, view: QGraphicsView):
        super().__init__(player)

        self.player = player
        self.video_item = video_item
        self.view = view

        self.video_frame = None

        self.pixmap_item = None
        self.rect_item = None

        self.videoFrameChanged.connect(self.grabbedFrame)

    #def videoFrame(self):
    #    print("DDSVideoSink::videoFrame")
    #    return super().videoFrame()

    #def setVideoFrame(self, frame):
    #    '''
    #    '''
    #    print("DDSVideoSink::setVideoFrame")
    #    return super().setVideoFrame(frame)

    def paint(self):
        print("DDSVideoSink::paint")

        if self.video_frame != None:
            painter = QPainter()
            painter.drawImage(0, 0, self.video_frame.toImage())
            painter.drawText(10, 10, "YYY")
            painter.fillRect(20, 20, 20, 20, QtCore.Qt.red)

            super().paint()

    def grabbedFrame(self, video_frame: QVideoFrame):
        #print("DDSVideoSink::grabbedFrame", video_frame)

        self.video_frame = video_frame


        #data = video_frame.map(QVideoFrame.ReadWrite)
        #print("DDSVideoSink::grabbedFrame data", data)


        painter = QPainter()  # which QPainterDevice device  ?
        painter.drawImage(0, 0, video_frame.toImage())
        painter.drawText(10, 10, "YYY")
        painter.fillRect(20, 20, 20, 20, QtCore.Qt.red)

        option = QStyleOptionGraphicsItem(QStyleOptionGraphicsItem.SO_GraphicsItem)
        self.video_item.paint(painter, option, None)
        
        

        video_frame_size = video_frame.size()
        w = video_frame_size.width()
        h = video_frame_size.height()
    
        view_w = self.view.width()
        view_h = self.view.height()

        factor = max(w/view_w, h/view_h)

        ww = int(w/factor) - 2
        hh = int(h/factor) - 2

        

        #return 

        img = video_frame.toImage()
        # still not optimal, I would like to draw inside the VideoItem...
        if self.pixmap_item == None:
            self.pixmap_item = QGraphicsPixmapItem(QPixmap(img).scaled(ww,hh))
            self.view.scene().addItem(self.pixmap_item)
        else:
            self.pixmap_item.setPixmap(QPixmap(img).scaled(ww,hh))

        if self.rect_item == None:
            self.rect_item = QGraphicsRectItem(100,100,50,50)
            self.view.scene().addItem(self.rect_item)



       