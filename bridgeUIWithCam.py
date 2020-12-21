#coding: utf8

VERSION = "0_0_1"

import os
import sys
import io
import logging
import copy

import colorama
import json

from deal import Deal
from deal import Color
from deal import Card

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from PySide2 import QtMultimedia
from PySide2 import QtMultimediaWidgets

from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtUiTools import QUiLoader

#from PySide2.QtCore import Signal, Slot
import bridgeUIscene
import bridgeVideo


class GuiLogger(logging.Handler):
    def __init__(self, textedit):
        logging.Handler.__init__(self)
        self.textedit = textedit

    def emit(self, record):
        self.textedit.append(self.format(record))  # implementation of append_line omitted



@QtCore.Slot(QtMultimedia.QVideoFrame)                                                                  
def titi(frame):                                                   
    print("xxx")  

class BRIDGEMainWindow(QtWidgets.QMainWindow):
    """
    """
    def __init__(self):
        """
        """
        QtWidgets.QMainWindow.__init__(self)
        
        self.window = loadUi('bridgeWUiWithCam.ui', self)
        
        self.setCentralWidget(self.window)
        
        
        curr_template = self.read_settings()
        
        self.templates = self.read_templates()
        self.deals = self.read_deals()
        
        self.template = self.templates[curr_template]
        
        # fill the graphic view
        self.scene = bridgeUIscene.BridgeUIscene(self.template)
         
        self.window.graphicsViewEdit.setScene(self.scene)
        self.window.graphicsViewEdit.show()

        gui_logger = GuiLogger(self.window.loggerView)
        logging.getLogger().addHandler(gui_logger)

        self.window.tabWidget.currentChanged.connect(self.cb_toggle_view)

        self.window.pushButtonGenerate.clicked.connect(self.cb_generate)
        self.window.pushButtonDDS.clicked.connect(self.cb_dds)

        self.window.pushButtonSaveTemplate.clicked.connect(self.cb_save_template)
        self.window.pushButtonNewTemplate.clicked.connect(self.cb_new_template)
        self.window.comboBoxTemplates.currentIndexChanged.connect(self.cb_show_template)
        
        self.window.pushButtonSaveDeal.clicked.connect(self.cb_save_deal)   
        self.window.pushButtonSaveDealAsImage.clicked.connect(self.cb_save_deal_as_image)
             
        #self.window.pushButtonN.clicked.connect(self.XXXX)
        #self.window.pushButtonS.clicked.connect(self.XXXX)
        #self.window.pushButtonW.clicked.connect(self.XXXX)
        #self.window.pushButtonE.clicked.connect(self.XXXX)
        
        self.window.loggerView.hide()
        # invisible on Template View
        self.window.pushButtonDDS.hide()
        self.window.textBrowserDDS.hide()
        
        self.window.pushButtonGenerate.show()
    
        tpl_list = [tpl_name for tpl_name in self.templates]
        self.window.comboBoxTemplates.addItems(tpl_list)
        
        deal_list = [" "] + [deal.name for deal in self.deals]
        self.window.comboBoxDeals.addItems(deal_list)        
        
        idx = tpl_list.index(curr_template)
        self.window.comboBoxTemplates.setCurrentIndex(idx)
        
        self.window.comboBoxDeals.currentIndexChanged.connect(self.cb_show_deal)

        # camera ---------------------------------------------------
        camTab = self.window.tabWidget.widget(1)
        
        camerasInfo = QtMultimedia.QCameraInfo.availableCameras()
        
        self.camera = None
        if len(camerasInfo) > 0:
            self.camera = QtMultimedia.QCamera(camerasInfo[0])
            #self.camera = QtMultimedia.QCamera(QtMultimedia.QCamera.FrontFace)
            #self.camera = QtMultimedia.QCamera(QtMultimedia.QCamera.BackFace)
            
            # CAMERA
            case = 1
            case = 2
            
            # MEDIA PLAYER
            #case = 11
            #case = 12
            case = 13
            
            if case == 1:
                
                viewfinder = QtMultimediaWidgets.QCameraViewfinder()
            
                camTab.layout().addWidget(viewfinder, 1)
            
                self.camera.setViewfinder(viewfinder)
                viewfinder.show()
                
                self.camera.start()  # to start the viewfinder
                
            if case == 2:
                
                scene = bridgeVideo.DDSVideoScene(self.window.cameraView)
                self.window.cameraView.show()
                
                self.video_surface = bridgeVideo.DDSVideoSurface(self.window.cameraView, scene)
                surface_format = QtMultimedia.QVideoSurfaceFormat(QtCore.QSize(400,400),
                                                                 QtMultimedia.QVideoFrame.Format_RGB32)
                self.video_surface.start(surface_format)
                
                self.camera.setViewfinder(self.video_surface)

                #self.videoProbe = QtMultimedia.QVideoProbe(self)
                #ok = self.videoProbe.setSource(self.camera)
                #print("ok = ", ok)
                #self.videoProbe.videoFrameProbed.connect(self.toto)
                #self.videoProbe.videoFrameProbed.connect(titi)
                                                                  
                self.camera.start()  # to start the viewfinder
                

            if case == 11:  # MOVIE inside videoItem # FIXME: size of MOVIE / size of videoItem
                
                scene = bridgeVideo.DDSVideoScene(self.window.cameraView)
                self.window.cameraView.show()
                
                videoItem = QtMultimediaWidgets.QGraphicsVideoItem()
                size = videoItem.size()  # (320,240) 
                #videoItem.setSize(QtCore.QSize(320,555))
                size = videoItem.size()
                
                surface = videoItem.videoSurface()
                nativesize = videoItem.nativeSize()
                
                scene.addItem(videoItem)
                 
                player = QtMultimedia.QMediaPlayer(self)
                player.setVideoOutput(videoItem)
                player.setMedia(QtCore.QUrl.fromLocalFile("/Users/xavier/PYTHON_TOOLS/GITHUB/bridge_dds/IMG_0770_0720x1280.MOV"))
                player.play()
                
            if case == 12:  # MOVIE inside QVideoWidget - GOOD
                
                self.window.cameraView.hide()
                
                videoWidget =  QtMultimediaWidgets.QVideoWidget()
                camTab.layout().addWidget(videoWidget, 1)
                videoWidget.show()
                
                # player must NOT be destroyed... -> must be "self.player"
                self.player = QtMultimedia.QMediaPlayer()
                self.player.setVideoOutput(videoWidget)
                self.player.setMedia(QtCore.QUrl.fromLocalFile("/Users/xavier/PYTHON_TOOLS/GITHUB/bridge_dds/IMG_0770_0720x1280.MOV"))                                   
                self.player.play()
                
            if case == 13:  # MOVIE inside QAbstractVideoSurface # FIXME: nothing shown...
                
                scene = bridgeVideo.DDSVideoScene(self.window.cameraView)
                self.window.cameraView.show()
                
                self.video_surface = bridgeVideo.DDSVideoSurface(self.window.cameraView, scene)
                surface_format = QtMultimedia.QVideoSurfaceFormat(QtCore.QSize(720/2, 1280/2),
                                                                  QtMultimedia.QVideoFrame.Format_RGB32)
                ok = self.video_surface.start(surface_format)
                
                self.player = QtMultimedia.QMediaPlayer()
                
                self.player.setVideoOutput(self.video_surface)
                self.player.setMedia(QtCore.QUrl.fromLocalFile("/Users/xavier/PYTHON_TOOLS/GITHUB/bridge_dds/IMG_0770_0720x1280.MOV"))
                self.player.play()
                
        # camera ---------------------------------------------------
        
        self.counter = 1
    
    @QtCore.Slot(QtMultimedia.QVideoFrame) 
    def toto(self, frame):
        print("toto")
    
    def closeEvent(self, event):
        self.write_settings()
        self.write_db()

    def read_deals(self):
        ''' '''
        fp = open("templates.json")
        db = json.load(fp)
        fp.close()
        
        deals = []
        
        for deal_description in db['DEALS']:
            
            deal = Deal()
            deal.name = deal_description["NAME"]
            deal.description = deal_description["DESCRIPTION"] 
            deal.difficulty = deal_description["DIFFICULTY"] 
            deal.from_pbn(deal_description["PBN"])
            deal.generate()
        
            deals.append(deal)
            
        return deals

    def read_templates(self):
        ''' '''
        fp = open("templates.json")
        db = json.load(fp)
        fp.close()
        
        ##------------------------------------------------------
        def get_cards(symbols, color):
            cards = []
            for symbol in symbols:
                card = Card.fromSymbolAndColor(symbol, color)
                if card:
                    cards.append(card)
            return cards
        ##------------------------------------------------------
        
        templates = {}
        
        for tpl in db['TEMPLATES']:
            
            deal = Deal()
            deal.name = tpl["NAME"]
            
            h = {
               "NORTH": "N",
               "SOUTH": "S",
               "EAST" : "E",
               "WEST" : "W",
            }
            
            for hand in ("NORTH", "SOUTH", "EAST", "WEST"):
                pos = h[hand]
                
                deal.hand[pos].target_points = tpl[hand]["POINTS"]
                
                deal.hand[pos].distribution_type = tpl[hand]["DISTRIBUTION"]["TYPE"]
                
                deal.hand[pos].target_distribution[Color.SPADES] = tpl[hand]["DISTRIBUTION"]["SPADES"]
                deal.hand[pos].target_distribution[Color.HEARTS] = tpl[hand]["DISTRIBUTION"]["HEARTS"]
                deal.hand[pos].target_distribution[Color.DIAMONDS] = tpl[hand]["DISTRIBUTION"]["DIAMONDS"]
                deal.hand[pos].target_distribution[Color.CLUBS] = tpl[hand]["DISTRIBUTION"]["CLUBS"]
                    
                deal.hand[pos].target_cards[Color.SPADES] = get_cards(tpl[hand]["CARDS"]["SPADES"], Color.SPADES)
                deal.hand[pos].target_cards[Color.HEARTS] = get_cards(tpl[hand]["CARDS"]["HEARTS"], Color.HEARTS)
                deal.hand[pos].target_cards[Color.DIAMONDS] = get_cards(tpl[hand]["CARDS"]["DIAMONDS"], Color.DIAMONDS)
                deal.hand[pos].target_cards[Color.CLUBS] = get_cards(tpl[hand]["CARDS"]["CLUBS"], Color.CLUBS)        
            
            templates[deal.name] = deal
            
        return templates

    def write_db(self):
        ''' '''
        ##---------------------------------------------------------
        def get_formatted_target_cards(deal: Deal, color: Color):
            cards = deal.target_cards[color]
            cards_str = [ card.symbol() for card in cards ]
        
            return ''.join(k for k in cards_str)
        ##---------------------------------------------------------
        
        data = {
            "TEMPLATES": [],
            "DEALS"    : []
        }
            
        # TEMPLATE section
        for tplname in self.templates:
            
            tpl = self.templates[tplname]
            
            tpl_description = {}
            tpl_description["NAME"] = tplname
            
            h = {
               "NORTH": "N",
               "SOUTH": "S",
               "EAST" : "E",
               "WEST" : "W",
            }
            
            for hand in ("NORTH", "SOUTH", "EAST", "WEST"): 
                pos = h[hand]
                
                tpl_description[hand] = {}
                tpl_description[hand]["POINTS"] = tpl.hand[pos].target_points
                
                tpl_description[hand]["DISTRIBUTION"] = {}
                tpl_description[hand]["CARDS"] = {}
            
                tpl_description[hand]["DISTRIBUTION"]["TYPE"] = tpl.hand[pos].distribution_type
            
                tpl_description[hand]["DISTRIBUTION"]["SPADES"] = tpl.hand[pos].target_distribution[Color.SPADES]
                tpl_description[hand]["DISTRIBUTION"]["HEARTS"] = tpl.hand[pos].target_distribution[Color.HEARTS]
                tpl_description[hand]["DISTRIBUTION"]["DIAMONDS"] = tpl.hand[pos].target_distribution[Color.DIAMONDS]
                tpl_description[hand]["DISTRIBUTION"]["CLUBS"] = tpl.hand[pos].target_distribution[Color.CLUBS]
            
                tpl_description[hand]["CARDS"]["SPADES"] = get_formatted_target_cards(tpl.hand[pos], Color.SPADES)
                tpl_description[hand]["CARDS"]["HEARTS"] = get_formatted_target_cards(tpl.hand[pos], Color.HEARTS)
                tpl_description[hand]["CARDS"]["DIAMONDS"] = get_formatted_target_cards(tpl.hand[pos], Color.DIAMONDS)
                tpl_description[hand]["CARDS"]["CLUBS"] = get_formatted_target_cards(tpl.hand[pos], Color.CLUBS)
            
            data["TEMPLATES"].append(tpl_description)

        # DEALS section 
        for deal in self.deals:
            
            deal_description = {}
            deal_description["NAME"] = deal.name
            deal_description["DESCRIPTION"] = deal.description
            deal_description["DIFFICULTY"]  = deal.difficulty
            deal_description["PBN"] = deal.to_pbn()
                
            data["DEALS"].append(deal_description)
               
        fp = open("templates.json", "w")
        json.dump(data, fp, indent=4, separators=(',', ': '))
        fp.close()

    def read_settings(self):
        '''
        '''
        #settings = QtCore.QSettings("BridgeMaster", "App Example")

        self.settings_file = "app.ini"
        settings = QtCore.QSettings(self.settings_file, QtCore.QSettings.IniFormat)

        return settings.value("current-template", "default")

    def write_settings(self):
        '''
        '''
        #settings = QtCore.QSettings("BridgeMaster", "App Example")
        
        self.settings_file = "app.ini"
        settings = QtCore.QSettings(self.settings_file, QtCore.QSettings.IniFormat)
            
        settings.setValue("current-template", "default")

    def cb_show_template(self, index):
        '''
        '''
        name = self.window.comboBoxTemplates.itemText(index)
        template = copy.deepcopy(self.templates[name])

        self.template = template

        self.template.reset()

        self.scene.deal = self.template
        self.scene.delete_unknown_items()
        self.scene.display_play_cards()
        self.scene.display_deal()

    def cb_save_template(self):
        '''
        save the currently edited deal template
        '''
        name = self.scene.deal.name
        self.templates[name] = copy.deepcopy(self.scene.deal)

    def cb_new_template(self):
        '''
        '''
        name, ok = QtWidgets.QInputDialog.getText(self, 
                    "QInputDialog::getText()",
                    "Template Name:", 
                    QtWidgets.QLineEdit.Normal,
                    QtCore.QDir.home().dirName())
        
        names = [tplname for tplname in self.templates]
        
        if name in names:
            # TODO - no duplicated names - disable OK button
            pass
        
        if ok:
            template = copy.deepcopy(self.template)
            template.name = name
        
            self.templates[name] = template
            names = [tplname for tplname in self.templates]
            
            combo = self.window.comboBoxTemplates
            
            combo.currentIndexChanged.disconnect()
            
            combo.clear()
            combo.addItems(names)
            
            combo.currentIndexChanged.connect(self.cb_show_template)
            
            combo.setCurrentIndex(combo.findText(name))

    def cb_show_deal(self, index):
        ''' '''
        if index > 0 :
            deal = self.deals[index-1]

            html = deal.get_deal_html()
            self.window.textBrowserDealTable.setHtml(html)
        
            html = deal.get_dds_results_html()
            self.window.textBrowserDDS.setHtml(html)

    def cb_save_deal(self):
        '''
        '''
        self.counter += 1
        
        deal = copy.deepcopy(self.template)
        deal.name = "%s-%03d" % (self.template.name, self.counter)
        self.deals.append(deal)
        
        deal_list = [" "] + [deal.name for deal in self.deals]
        
        self.window.comboBoxDeals.clear()
        self.window.comboBoxDeals.addItems(deal_list)           
    
    def cb_save_deal_as_image(self):
        '''
        '''
        self.counter += 1
        
        pixmap = QtGui.QPixmap.grabWidget(self, rect = self.geometry())
        
        filename = "deal-%s-%03d.png" % (self.template.name, self.counter)
        
        file = QtCore.QFile(filename)
        file.open(QtCore.QIODevice.WriteOnly)
        pixmap.save(file, "PNG")

    def cb_generate(self):
        '''
        '''
        self.template.reset()
        self.template.generate()
        
        html = self.template.get_deal_html()
        self.window.textBrowserDealTable.setHtml(html)
        
        # jump in "deal" view
        self.window.tabWidget.setCurrentIndex(1)
        
        #print(html)
        
        # reset this, need to call "DDS"
        self.window.textBrowserDDS.setText("")
        self.cb_dds()
        
    def cb_dds(self):
        '''
        '''
        html = self.template.get_dds_results_html()
        
        self.window.textBrowserDDS.setHtml(html)
        
    def cb_toggle_view(self, index):
        '''
        '''
        if index == 0:
            self.window.pushButtonGenerate.show()
            self.window.pushButtonDDS.hide()
            self.window.textBrowserDDS.hide()
        if index == 1:
            self.window.pushButtonGenerate.hide()
            self.window.pushButtonDDS.show()
            self.window.textBrowserDDS.show() 
        if index == 2:
            self.window.pushButtonGenerate.show()
            self.window.pushButtonDDS.show()
            self.window.textBrowserDDS.show() 
            
        # remake layout... TODO
        self.layout()



def loadUi(uifile, baseinstance=None):
    '''
    '''
    loader = QUiLoader(baseinstance)

    window = loader.load(uifile)

    return window


def main():
    '''
    '''
    colorama.init()

    app = QtWidgets.QApplication()
    app.setApplicationName("DealUI")

    mainWin = BRIDGEMainWindow()
    mainWin.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    '''
    '''
    main()
