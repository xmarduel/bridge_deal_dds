#coding: utf8

VERSION = "0_0_1"

import os
import sys

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

from PySide6 import QtMultimedia
from PySide6 import QtMultimediaWidgets

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtUiTools import QUiLoader

from PySide6.QtMultimedia import QMediaCaptureSession
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimedia import QCameraDevice, QMediaDevices, QCamera, QVideoSink
from PySide6.QtMultimediaWidgets import QVideoWidget

from deal import Card
from bridgeHandView import BridgeHandView
from bridgeDDSView import BridgeDDSView


class VideoDDSMainWindow(QtWidgets.QMainWindow):
    """
    """
    def __init__(self):
        """
        """
        QtWidgets.QMainWindow.__init__(self)
        
        self.window = loadUi('bridgeWUiVideoDDS.ui', self)
        
        self.setCentralWidget(self.window)

        self.window.pushButtonCalcDDS.clicked.connect(self.cb_dds)

        
        # captured cards view
        self.hand_view = BridgeHandView()
        self.window.capturedHandView.layout().addWidget(self.hand_view)
        # test captured cards view
        self.display_captured_cards()

        # the deal or similarly said the 4 hands for DDS
        self.dealOK = False
        self.deal = None

        # dds view
        self.window.textBrowserShowDDS.setLayout(QtWidgets.QHBoxLayout())
        self.display_dds_widget = BridgeDDSView()
        self.window.textBrowserShowDDS.layout().addWidget(self.display_dds_widget)
        # test dds view
        self.cb_dds()


        # video output ---------------------------------------------------
        video = self.window.videoView
        self.preview = QVideoWidget()

        video.setLayout(QtWidgets.QHBoxLayout())
        video.layout().addWidget(self.preview, 1)

        self.player = None
        self.camera = None
            
        # MEDIA PLAYER
        case = 1
            
        # CAMERA
        case = 2
            
            
        if case == 1:
                
            self.player = QMediaPlayer()
            self.player.setSource(QtCore.QUrl("http://example.com/myclip1.mp4"))

            self.player.setVideoOutput(self.preview)

            self.preview.show()
            self.player.play()

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

        self.display_dds_widget.display_dds(pbn)
        
    def display_captured_cards(self):
        '''
        fill handView
        '''
        # IR results
        self.captured_cards = [Card.S_2, Card.H_6, Card.C_K, Card.C_6, Card.C_9, Card.H_J, Card.H_Q, Card.D_9, Card.D_J, Card.D_Q, Card.D_5, Card.D_6, Card.C_7]
        #self.captured_cards = [Card.S_2, Card.H_6]

        self.hand_view.display_cards(self.captured_cards)


def loadUi(uifile, baseinstance=None):
    '''
    '''
    loader = QUiLoader(baseinstance)

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
