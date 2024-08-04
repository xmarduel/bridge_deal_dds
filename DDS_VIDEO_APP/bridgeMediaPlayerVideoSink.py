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

        self.annotation_items = []

        self.videoFrameChanged.connect(self.grabbedFrame)

        self.yolo = YoloImageRecognition(
            {
                "nb_classes": 52,
                "confidence": 0.9,
                "threshold": 0.9,
                "yolotrainingsize": 512,
            }
        )

    def grabbedFrame(self, video_frame: QVideoFrame):
        print("DDSVideoSink::grabbedFrame", video_frame)

        self.remove_annotations()

        self.video_frame = video_frame

        ### https://stackoverflow.com/questions/69432427/how-to-use-qvideosink-in-qml-in-qt6
        image = video_frame.toImage()

        # video_frame.map(QVideoFrame.WriteOnly)

        # YOLO PROCESSING / find the labels and augment the image during the processing
        labels: List[str] = []
        if False:
            labels = self.yolo.process(image)

        # painter = QPainter(image)
        # painter = QPainter(self.video_widget)

        # video_frame.paint(
        #    painter,
        #    QtCore.QRectF(0.0, 0.0, 700.0, 700.0),  # what is that
        #    QVideoFrame.PaintOptions(),  # what is that
        # )

        # video_frame.setSubtitleText("Xavier")
        # video_frame.unmap()

        self.video_item.videoSink().setVideoFrame(video_frame)
        # self.setVideoFrame(video_frame)

        self.annotate_scene()

        # and fill the list of cards in the main window as a (partially) hand
        if labels:
            print("LABELS:", labels)
            # self.graphics_view.main_window.set_yolo_cards_from_labels(labels)

    def annotate_scene(self):
        """
        add extra to scene! but needs to be removed!
        """
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor("red"))
        pen.setWidth(3)

        line = QtCore.QLineF(0, 0, 100 * random.random(), 100 * random.random())
        item = QGraphicsLineItem(line)

        self.graphics_view.the_scene.addLine(line, pen)

        self.annotation_items.append(item)

    def remove_annotations(self):
        """ """
        items = self.graphics_view.the_scene.items()
        for item in items:
            # print("type : <", item.type(), ">", item.__class__.__name__)
            if item.type() != 14:  # "QGraphicsVideoItem":
                # print("    delete item", item.type(), item.__class__.__name__)
                self.graphics_view.the_scene.removeItem(item)

        self.annotation_items = []
