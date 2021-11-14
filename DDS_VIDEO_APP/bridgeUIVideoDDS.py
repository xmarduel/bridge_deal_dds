#coding: utf8

VERSION = "0_0_1"

import os
import sys
import copy

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

from PySide6.QtUiTools import QUiLoader

from PySide6.QtMultimedia import QMediaCaptureSession
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimedia import QCameraDevice, QMediaDevices, QCamera, QVideoSink

from deal import Card
from deal import Hand
from deal import Deal

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

        # the captured cards, to become a valid hand - hopefully -
        self.yolo_cards = []
        # the deal (the 4 hands) for DDS
        self.deal = Deal()

        self.window.pushButtonCalcDDS.clicked.connect(self.cb_dds)
        self.window.pushButtonNord.clicked.connect(self.cb_set_hand_nord)
        self.window.pushButtonSud.clicked.connect(self.cb_set_hand_sud)
        self.window.pushButtonWest.clicked.connect(self.cb_set_hand_west)
        self.window.pushButtonEast.clicked.connect(self.cb_set_hand_east)

        # captured cards view
        self.yolo_cards_view = self.window.hand_view

        # dds view 
        self.dds_view = self.window.dds_view
        self.dds_view.hide()

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
        
    def dds_enable(self):
        '''
        '''
        enabled = True
        
        if len(self.deal.hand['N'].cards) != 13:
            enabled = False
        if len(self.deal.hand['S'].cards) != 13:
            enabled = False
        if len(self.deal.hand['W'].cards) != 13:
            enabled = False
        if len(self.deal.hand['E'].cards) != 13:
            enabled = False

        self.window.pushButtonCalcDDS.setEnabled(enabled)
        
    def cb_dds(self):
        '''
        '''
        pbn = self.deal.to_pbn()

        self.dds_view.show()
        self.dds_view.display_dds(pbn)

    def reset_deal(self):
        '''
        '''    
        self.deal.reset()

    def cb_set_hand_nord(self):
        '''
        '''
        if len(self.yolo_cards) == 13:
            self.deal.hand["N"].cards = copy.deepcopy(self.yolo_cards)

    def cb_set_hand_sud(self):
        '''
        '''
        if len(self.yolo_cards) == 13:
            self.deal.hand["S"].cards = copy.deepcopy(self.yolo_cards)

    def cb_set_hand_west(self):
        '''
        '''
        if len(self.yolo_cards) == 13:
            self.deal.hand["W"].cards = copy.deepcopy(self.yolo_cards)

    def cb_set_hand_east(self):
        '''
        '''
        if len(self.yolo_cards) == 13:
            self.deal.hand["E"].cards = copy.deepcopy(self.yolo_cards)
        
    def set_yolo_cards_from_labels(self, labels):
        '''
        '''
        self.yolo_cards = self.yolo_cards_view.hand_from_labels(labels)

        # display it
        self.yolo_cards_view.display_cards(self.yolo_cards)

        # can it be assigned to the deal ?
        enabled = (len(self.yolo_cards) == 13)
            
        # enable/disable hand selection
        self.window.pushButtonNord.setEnabled(enabled)
        self.window.pushButtonSud.setEnabled(enabled)
        self.window.pushButtonWest.setEnabled(enabled)
        self.window.pushButtonEast.setEnabled(enabled)

        self.dds_enable()

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
