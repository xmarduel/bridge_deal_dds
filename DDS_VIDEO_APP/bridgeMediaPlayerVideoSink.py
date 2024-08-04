from PySide6 import QtCore
from PySide6 import QtGui

from PySide6.QtGui import QPainter
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem
from PySide6.QtWidgets import QGraphicsView

from PySide6.QtWidgets import QGraphicsLineItem

from PySide6.QtMultimedia import (
    QVideoFrame,
    QVideoFrameFormat,
    QVideoSink,
)
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem, QVideoWidget

from bridgeYoloImageRecognition import YoloImageRecognition

# from bridgeVideoGraphicsView import BridgeVideoGraphicsView

import numpy as np
import random

from typing import List

"""
https://stackoverflow.com/questions/52359924/pyqt5-access-frames-with-qmediaplayer
"""


class BridgeMediaPlayerVideoSink(QVideoSink):
    """ """

    def __init__(
        self,
        graphics_view: "BridgeVideoGraphicsView",
    ):
        super().__init__()

        self.graphics_view = graphics_view
        self.video_item = graphics_view.video_item

        self.videoFrameChanged.connect(self.grabbedFrame)

        self.yolo = YoloImageRecognition(
            {
                "nb_classes": 52,
                "confidence": 0.9,
                "threshold": 0.9,
                "yolotrainingsize": 512,
            }
        )

    def grabbedFrame(self, input_video_frame: QVideoFrame):
        """
        Has to create an empty video frame and fill it with the true image!

        Because the input_video_frame has an Invalid video_image_format (strange)

        With this empty video_frame and its **mapped** image, the paint
        can put the real image inside it + labels boxes
        """
        print("DDSVideoSink::grabbedFrame", input_video_frame)

        size = input_video_frame.size()
        size.transpose()  # strange!

        video_frame = QVideoFrame(
            QVideoFrameFormat(size, QVideoFrameFormat.PixelFormat.Format_BGRA8888)
        )

        src_image = input_video_frame.toImage()

        cv_image = self.QImageToCvMat(image=src_image)

        if (not video_frame.isValid()) or (not video_frame.map(QVideoFrame.WriteOnly)):
            QtCore.qWarning("QVideoFrame is not valid or not writable")
            return

        video_image_format = QVideoFrameFormat.imageFormatFromPixelFormat(
            video_frame.pixelFormat()
        )

        if video_image_format == QtGui.QImage.Format_Invalid:
            QtCore.qWarning(
                "It is not possible to obtain image format from the pixel format of the videoframe"
                + str(video_frame.pixelFormat()),
            )
            return

        ### https://stackoverflow.com/questions/69432427/how-to-use-qvideosink-in-qml-in-qt6

        mapped_image = QtGui.QImage(
            video_frame.bits(0), size.width(), size.height(), video_image_format
        )

        # YOLO PROCESSING / find the labels and augment the image during the processing
        labels: List[str] = []
        if True:
            labels = self.yolo.process(cv_image)

        painter = QPainter(mapped_image)
        self.paint_content(painter, src_image)
        # self.paint_labels(painter)
        painter.end()

        video_frame.unmap()

        self.video_item.videoSink().setVideoFrame(video_frame)

        # and fill the list of cards in the main window as a (partially) hand
        if labels:
            print("LABELS:", labels)
            # self.graphics_view.main_window.set_yolo_cards_from_labels(labels)

    def QImageToCvMat(self, image):
        """Converts a QImage into an opencv MAT format"""
        # take care the conversion format !
        # Format_RGB888 seems to swap R and B !!!
        image = image.convertToFormat(QtGui.QImage.Format.Format_BGR888)

        width = image.width()
        height = image.height()

        ptr = image.constBits()
        arr = np.array(ptr).reshape(height, width, 3)  #  Copies the data

        return arr

    def paint_labels(self, painter: QPainter):
        """ """
        # ensure at least one detection exists
        if len(self.yolo.idxs) > 0:
            # loop over the indexes we are keeping
            for i in self.yolo.idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (self.yolo.boxes[i][0], self.yolo.boxes[i][1])
                (w, h) = (self.yolo.boxes[i][2], self.yolo.boxes[i][3])

                # draw a bounding box rectangle and label on the image
                color = [int(c) for c in self.yolo.COLORS[self.yolo.classIDs[i]]]
                pen = QtGui.QPen()
                pen.setColor(QtGui.QColor(*color))
                pen.setWidth(5)
                painter.setPen(pen)
                painter.setFont(QtGui.QFont("Arial", 15))
                painter.drawRect(x, y, w, h)
                text = "{}: {:.3f}".format(
                    self.yolo.LABELS[self.yolo.classIDs[i]], self.yolo.confidences[i]
                )
                painter.drawText(x, y - 5, text)

    def paint_content(self, painter: QPainter, src_image: QtGui.QImage):
        """ """
        painter.drawImage(
            QtCore.QRect(0, 0, src_image.width(), src_image.height()),
            src_image,
            QtCore.QRect(0, 0, src_image.width(), src_image.height()),
        )

        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor("black"))
        pen.setWidth(25)

        painter.fillRect(300, 100, 200, 200, QtGui.QColor("green"))
