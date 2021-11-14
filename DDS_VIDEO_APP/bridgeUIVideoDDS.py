#coding: utf8

VERSION = "0_0_1"

import os
import sys

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

from PySide6.QtUiTools import QUiLoader

from PySide6.QtMultimedia import QMediaCaptureSession
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimedia import QCameraDevice, QMediaDevices, QCamera, QVideoSink

from deal import Card

import bridgeHandView
import bridgeDDSView

from bridgeVideoGraphicsView import BridgeVideoGraphicsView

class VideoDDSMainWindow(QtWidgets.QMainWindow):
    """
    """
    def __init__(self):
        """
        """
        QtWidgets.QMainWindow.__init__(self)
        
        self.window = self.load_ui('bridgeUiVideoDDS.ui')
        
        self.setCentralWidget(self.window)

        self.window.pushButtonCalcDDS.clicked.connect(self.cb_dds)

        # the deal or similarly said the 4 hands for DDS
        self.dealOK = False
        self.deal = None

        # hand view (captured cards)
        self.hand_view = self.window.hand_view
        self.hand = [Card.S_5, Card.H_J] ## test hand view
        # test captured cards view
        self.display_hand()

        # dds view 
        self.dds_view = self.window.dds_view
        self.cb_dds() ## test dds view

        # video output ---------------------------------------------------
        self.video_graphics_view = BridgeVideoGraphicsView(self)
        self.window.VideoViewContainer.layout().addWidget(self.video_graphics_view)

        self.video_graphics_view.open_and_play_video("./test/IMG_0770_0720x1280.MOV")

        return

        # MEDIA PLAYER
        case = 1
        
        # CAMERA
        case = 2

        if case == 2:

            def checkCameraAvailability():
                if QMediaDevices.videoInputs().count() > 0:
                    return True
                else:
                    return False

            def getCamera():
                # seems good
                #self.camera = QMediaDevices.defaultVideoInput() 

                cameras = QMediaDevices.videoInputs()
        
                for cameraDevice in cameras:
                    if cameraDevice.description == "mycamera":
                        self.camera = QCamera(cameraDevice)
                        #self.camera = QCamera(QCameraDevice.FrontFace)
                        #self.camera = QCamera(QCameraDevice.BackFace)

                        #self.camera.setFocusPointMode(QCamera.FocusModeManual)
                        #self.camera.setCustomFocusPoint(QtCore.QPointF(0.25, 0.75))
                        #self.camera.setZoomFactor(3.0)
                        #self.camera.setWhiteBalanceMode(QCamera.WhiteBalanceFluorescent)
                
                captureSession = QMediaCaptureSession()
                captureSession.setCamera(self.camera)
                
                self.camera.setVideoOutput(self.preview)
                self.preview.show()

                # for image processing 
                self.video_sink = QVideoSink()
                self.camera.setVideoOutput(self.video_sink)
                # self.video_sink.setVideoFrame(..) will be called with video frames

                self.camera.start()

        # video output ---------------------------------------------------
        
    def cb_dds(self):
        '''
        '''
        pbn = "N:KQ964.AK763.J6.Q AJ8.J5.Q92.KJ964 7.T42.AT84.AT875 T532.Q98.K753.32"

        self.dds_view.display_dds(pbn)
        
    def set_hand_labels(self, labels):
        '''
        '''
        self.hand = self.hand_view.hand_from_labels(labels)

    def display_hand(self):
        '''
        fill hand_view
        '''
        self.hand_view.display_cards(self.hand)

    def load_ui(self, uifile):
        '''
        '''
        loader = QUiLoader(self)
        loader.registerCustomWidget(bridgeDDSView.BridgeDDSView)
        loader.registerCustomWidget(bridgeHandView.BridgeHandView)
        
        window = loader.load(uifile)

        return window


def main():
    '''
    '''
    app = QtWidgets.QApplication()
    app.setApplicationName("VideoDDS")

    mainWin = VideoDDSMainWindow()
    mainWin.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    '''
    '''
    main()
