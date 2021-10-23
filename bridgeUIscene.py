#coding: utf8

import sys

from deal import Deal
from deal import Color
from deal import Card

if sys.platform == 'win32':
    from PySide6 import QtCore
    from PySide6 import QtGui
    from PySide6 import QtWidgets
else:
    from PySide2 import QtCore
    from PySide2 import QtGui
    from PySide2 import QtWidgets  

class BridgeUIscene (QtWidgets.QGraphicsScene) :
    '''
    '''
    def __init__(self, deal):
        '''
        '''
        QtWidgets.QGraphicsScene.__init__(self)
        
        self.deal = deal
        
        self.grabbedItem = None
        
        self.make_default_scene()
        self.display_deal()
        
        self.spinboxN.valueChanged.connect(self.cb_set_target_points_N)
        self.spinboxS.valueChanged.connect(self.cb_set_target_points_S)
        self.spinboxE.valueChanged.connect(self.cb_set_target_points_E)
        self.spinboxW.valueChanged.connect(self.cb_set_target_points_W)
        
        self.target_area = {
            "N" : {"x1":200, "x2":300, "y1":0,   "y2":200 }, 
            "S" : {"x1":200, "x2":300, "y1":200, "y2":999 }, 
            "W" : {"x1":000, "x2":200, "y1":200, "y2":999 }, 
            "E" : {"x1":300, "x2":999, "y1":200, "y2":999 }, 
            "-" : {"x1":400, "x2":999, "y1":0,   "y2":999 }, 
        }

    def cb_set_target_points_N(self, value):
        '''
        '''
        self.deal.hand["N"].target_points = value

    def cb_set_target_points_S(self, value):
        '''
        '''
        self.deal.hand["S"].target_points = value

    def cb_set_target_points_E(self, value):
        '''
        '''
        self.deal.hand["E"].target_points = value

    def cb_set_target_points_W(self, value):
        '''
        '''
        self.deal.hand["W"].target_points = value

    def make_default_scene(self):
        '''
        '''
        # deal layout - table
        self.addRect(200,200,100,100)
        # with annotations
        self.addText("N").setPos(240, 200)
        self.addText("S").setPos(240, 280)
        self.addText("E").setPos(285, 240)
        self.addText("W").setPos(200, 240)
        
        # user input : target pts for each hand
        self.spinboxN = QtWidgets.QSpinBox()
        self.spinboxS = QtWidgets.QSpinBox()
        self.spinboxE = QtWidgets.QSpinBox()
        self.spinboxW = QtWidgets.QSpinBox()
        
        self.spinboxN.setSuffix(" pts")
        self.spinboxS.setSuffix(" pts")
        self.spinboxE.setSuffix(" pts")
        self.spinboxW.setSuffix(" pts")
        
        self.spinboxN.setToolTip("targeted points")
        self.spinboxS.setToolTip("targeted points")
        self.spinboxE.setToolTip("targeted points")
        self.spinboxW.setToolTip("targeted points")
        
        self.spinboxN.setMinimum(-1)
        self.spinboxS.setMinimum(-1)
        self.spinboxE.setMinimum(-1)
        self.spinboxW.setMinimum(-1)
        
        self.itemSpinboxN = itemSpinboxN = self.addWidget(self.spinboxN)
        self.itemSpinboxS = itemSpinboxS = self.addWidget(self.spinboxS)
        self.itemSpinboxE = itemSpinboxE = self.addWidget(self.spinboxE)
        self.itemSpinboxW = itemSpinboxW = self.addWidget(self.spinboxW)
        
        itemSpinboxN.setPos(200, 170)
        itemSpinboxN.setMinimumSize(100, 20)
        
        itemSpinboxS.setPos(200, 310)
        itemSpinboxS.setMinimumSize(100, 20)
        
        itemSpinboxE.setPos(310, 200)
        itemSpinboxE.setMinimumSize(100, 20)
        
        itemSpinboxW.setPos(90, 200)
        itemSpinboxW.setMinimumSize(100, 20)
        
        # placeholder for the user hands with predefined card : the 4 colors
        x = {
            '♠' : 200,
            '♥' : 225,
            '♦' : 250,
            '♣' : 275,
        }
        y = 145
                
        itemNP = self.addText('♠')
        itemNP.setPos(x['♠'], y)
        itemNC = self.addText('♥')
        itemNC.setPos(x['♥'], y)
        itemNK = self.addText('♦')
        itemNK.setPos(x['♦'], y)
        itemNT = self.addText('♣')
        itemNT.setPos(x['♣'], y)
        itemNC.setDefaultTextColor(QtGui.QColor("red"))
        itemNK.setDefaultTextColor(QtGui.QColor("red"))
        
        x = {
            '♠' : 200,
            '♥' : 225,
            '♦' : 250,
            '♣' : 275,
        }
        y = 330
        itemSP = self.addText('♠')
        itemSP.setPos(x['♠'], y)
        itemSC = self.addText('♥')
        itemSC.setPos(x['♥'], y)
        itemSK = self.addText('♦')
        itemSK.setPos(x['♦'], y)
        itemST = self.addText('♣')
        itemST.setPos(x['♣'], y)
        itemSC.setDefaultTextColor(QtGui.QColor("red"))
        itemSK.setDefaultTextColor(QtGui.QColor("red"))
        
        x = {
            '♠' : 310,
            '♥' : 335,
            '♦' : 360,
            '♣' : 385,
        }
        y = 220
        
        itemEP = self.addText('♠')
        itemEP.setPos(x['♠'], y)
        itemEC = self.addText('♥')
        itemEC.setPos(x['♥'], y)
        itemEK = self.addText('♦')
        itemEK.setPos(x['♦'], y)
        itemET = self.addText('♣')
        itemET.setPos(x['♣'], y)
        itemEC.setDefaultTextColor(QtGui.QColor("red"))
        itemEK.setDefaultTextColor(QtGui.QColor("red"))
        
        x = {
            '♠' : 90,
            '♥' : 115,
            '♦' : 140,
            '♣' : 165,
        }
        y = 220
        
        itemWP = self.addText('♠')
        itemWP.setPos(x['♠'], y)
        itemWC = self.addText('♥')
        itemWC.setPos(x['♥'], y)
        itemWK = self.addText('♦')
        itemWK.setPos(x['♦'], y)
        itemWT = self.addText('♣')
        itemWT.setPos(x['♣'], y)
        itemWC.setDefaultTextColor(QtGui.QColor("red"))
        itemWK.setDefaultTextColor(QtGui.QColor("red"))
        
        # the game cards to select into the user cards
        self.populate_card_item()

    def populate_card_item(self):
        '''
        '''
        cardset = "naylor"
        suffix = "gif"

        cardset = "quadrat"
        suffix = "png"

        SIZE = 25

        self.pixmaps = {
            "UNKNOWN" : QtGui.QPixmap("cardset-%s/unknown.gif" % cardset).scaled(SIZE,SIZE),
            
            Card.S_A : QtGui.QPixmap("cardset-%s/As.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.S_K : QtGui.QPixmap("cardset-%s/Ks.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.S_Q : QtGui.QPixmap("cardset-%s/Qs.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.S_J : QtGui.QPixmap("cardset-%s/Js.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.S_T : QtGui.QPixmap("cardset-%s/10s.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.S_9 : QtGui.QPixmap("cardset-%s/9s.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.S_8 : QtGui.QPixmap("cardset-%s/8s.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.S_7 : QtGui.QPixmap("cardset-%s/7s.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.S_6 : QtGui.QPixmap("cardset-%s/6s.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.S_5 : QtGui.QPixmap("cardset-%s/5s.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.S_4 : QtGui.QPixmap("cardset-%s/4s.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.S_3 : QtGui.QPixmap("cardset-%s/3s.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.S_2 : QtGui.QPixmap("cardset-%s/2s.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
        
            Card.H_A : QtGui.QPixmap("cardset-%s/Ah.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.H_K : QtGui.QPixmap("cardset-%s/Kh.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.H_Q : QtGui.QPixmap("cardset-%s/Qh.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.H_J : QtGui.QPixmap("cardset-%s/Jh.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.H_T : QtGui.QPixmap("cardset-%s/10h.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.H_9 : QtGui.QPixmap("cardset-%s/9h.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.H_8 : QtGui.QPixmap("cardset-%s/8h.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.H_7 : QtGui.QPixmap("cardset-%s/7h.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.H_6 : QtGui.QPixmap("cardset-%s/6h.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.H_5 : QtGui.QPixmap("cardset-%s/5h.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.H_4 : QtGui.QPixmap("cardset-%s/4h.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.H_3 : QtGui.QPixmap("cardset-%s/3h.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.H_2 : QtGui.QPixmap("cardset-%s/2h.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            
            Card.D_A : QtGui.QPixmap("cardset-%s/Ad.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.D_K : QtGui.QPixmap("cardset-%s/Kd.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.D_Q : QtGui.QPixmap("cardset-%s/Qd.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.D_J : QtGui.QPixmap("cardset-%s/Jd.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.D_T : QtGui.QPixmap("cardset-%s/10d.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.D_9 : QtGui.QPixmap("cardset-%s/9d.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.D_8 : QtGui.QPixmap("cardset-%s/8d.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.D_7 : QtGui.QPixmap("cardset-%s/7d.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.D_6 : QtGui.QPixmap("cardset-%s/6d.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.D_5 : QtGui.QPixmap("cardset-%s/5d.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.D_4 : QtGui.QPixmap("cardset-%s/4d.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.D_3 : QtGui.QPixmap("cardset-%s/3d.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.D_2 : QtGui.QPixmap("cardset-%s/2d.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            
            Card.C_A : QtGui.QPixmap("cardset-%s/Ac.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.C_K : QtGui.QPixmap("cardset-%s/Kc.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.C_Q : QtGui.QPixmap("cardset-%s/Qc.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.C_J : QtGui.QPixmap("cardset-%s/Jc.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.C_T : QtGui.QPixmap("cardset-%s/10c.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.C_9 : QtGui.QPixmap("cardset-%s/9c.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.C_8 : QtGui.QPixmap("cardset-%s/8c.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.C_7 : QtGui.QPixmap("cardset-%s/7c.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.C_6 : QtGui.QPixmap("cardset-%s/6c.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.C_5 : QtGui.QPixmap("cardset-%s/5c.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.C_4 : QtGui.QPixmap("cardset-%s/4c.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.C_3 : QtGui.QPixmap("cardset-%s/3c.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
            Card.C_2 : QtGui.QPixmap("cardset-%s/2c.%s" % (cardset, suffix)).scaled(SIZE,SIZE),
        }

        self.card_item = {

            Card.S_A : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_A]),
            Card.S_K : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_K]),
            Card.S_Q : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_Q]),
            Card.S_J : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_J]),
            Card.S_T : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_T]),
            Card.S_9 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_9]),
            Card.S_8 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_8]),
            Card.S_7 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_7]),
            Card.S_6 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_6]),
            Card.S_5 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_5]),
            Card.S_4 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_4]),
            Card.S_3 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_3]),
            Card.S_2 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_2]),
            
            Card.H_A : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_A]),
            Card.H_K : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_K]),
            Card.H_Q : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_Q]),
            Card.H_J : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_J]),
            Card.H_T : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_T]),
            Card.H_9 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_9]),
            Card.H_8 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_8]),
            Card.H_7 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_7]),
            Card.H_6 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_6]),
            Card.H_5 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_5]),
            Card.H_4 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_4]),
            Card.H_3 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_3]),
            Card.H_2 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_2]),
            
            Card.D_A : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_A]),
            Card.D_K : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_K]),
            Card.D_Q : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_Q]),
            Card.D_J : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_J]),
            Card.D_T : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_T]),
            Card.D_9 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_9]),
            Card.D_8 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_8]),
            Card.D_7 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_7]),
            Card.D_6 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_6]),
            Card.D_5 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_5]),
            Card.D_4 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_4]),
            Card.D_3 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_3]),
            Card.D_2 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_2]),
            
            Card.C_A : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_A]),
            Card.C_K : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_K]),
            Card.C_Q : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_Q]),
            Card.C_J : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_J]),
            Card.C_T : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_T]),
            Card.C_9 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_9]),
            Card.C_8 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_8]),
            Card.C_7 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_7]),
            Card.C_6 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_6]),
            Card.C_5 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_5]),
            Card.C_4 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_4]),
            Card.C_3 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_3]),
            Card.C_2 : QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_2]),
        }

        # map item -> card
        self.item_card = {}
        
        for card in self.card_item:
            item = self.card_item[card]
            self.item_card[item] = card



        self.unknown_cards = []

        self.make_cards_play()
        self.display_play_cards()

    def delete_unknown_items(self):
        '''
        '''
        for item in self.unknown_cards:
            self.removeItem(item)

        self.unknown_cards = []

    def make_cards_play(self):
        '''
        '''
        for card in self.card_item:  
            item = self.card_item[card]
            self.addItem(item)

    def display_play_cards(self):
        '''
        '''
        initial_x_position = {
            Color.SPADES   : 450,
            Color.HEARTS   : 480,
            Color.DIAMONDS : 510,
            Color.CLUBS    : 540,
        }
        
        initial_y_position = 10
        
        for color in Color:
            y = initial_y_position
            for card in self.card_item:
                if  card.color() != color:
                    continue

                item = self.card_item[card]
                item.setPos(initial_x_position[color],y)
                y += 30

    def display_deal(self):
        '''
        '''
        # target points
        self.spinboxN.setValue(self.deal.hand["N"].target_points)
        self.spinboxS.setValue(self.deal.hand["S"].target_points)
        self.spinboxE.setValue(self.deal.hand["E"].target_points)
        self.spinboxW.setValue(self.deal.hand["W"].target_points)

        self.display_hand("N")
        self.display_hand("S")
        self.display_hand("E")
        self.display_hand("W")

    def display_hand(self, pos):
        '''
        '''
        initial_x_position = {

            "N": {
                Color.SPADES   : 200,
                Color.HEARTS   : 225,
                Color.DIAMONDS : 250,
                Color.CLUBS    : 275,
            },  
        
            "S" : {
                Color.SPADES   : 200,
                Color.HEARTS   : 225,
                Color.DIAMONDS : 250,
                Color.CLUBS    : 275,
            },
            
            "W" : {
                Color.SPADES   :  90,
                Color.HEARTS   : 115,
                Color.DIAMONDS : 140,
                Color.CLUBS    : 165,
            },
            
            "E" : {
                Color.SPADES   : 310,
                Color.HEARTS   : 335,
                Color.DIAMONDS : 360,
                Color.CLUBS    : 385,
            }
        }
        
        initial_y_position = {

            "N" : 145,
            "S" : 350,
            "W" : 240,
            "E" : 240,
        }

        # for N, we have to get the max nb of cards in each colors in order
        # to position (y) the cards optimally

        max_nb_cards = 0

        target_cards = {}
        
        for color in Color:
            target_cards[color] = self.deal.hand["N"].target_cards[color]
                
        # eval the max number of card for a color
        
        max_nb_cards = 0
        
        if pos == "N":
            max_nb_cards = max(max_nb_cards, len(target_cards[Color.SPADES]))
            max_nb_cards = max(max_nb_cards, len(target_cards[Color.HEARTS]))
            max_nb_cards = max(max_nb_cards, len(target_cards[Color.DIAMONDS]))
            max_nb_cards = max(max_nb_cards, len(target_cards[Color.CLUBS]))
            
            max_nb_cards = max(max_nb_cards, self.deal.hand["N"].target_distribution[Color.SPADES])
            max_nb_cards = max(max_nb_cards, self.deal.hand["N"].target_distribution[Color.HEARTS])
            max_nb_cards = max(max_nb_cards, self.deal.hand["N"].target_distribution[Color.DIAMONDS])
            max_nb_cards = max(max_nb_cards, self.deal.hand["N"].target_distribution[Color.CLUBS])
            
        # --------------------------------------------------------------------------------
                
        for color in Color:
            target_cards[color] = self.deal.hand[pos].target_cards[color]
                
            x = initial_x_position[pos][color]
            y = initial_y_position[pos]
            
            if pos == "N":
                h = max_nb_cards * (25+5)
                y = y - h
        
            for card in target_cards[color]:
                item = self.card_item[card]
                item.setPos(x,y)
                y += 30
                
            missing = self.deal.hand[pos].target_distribution[color] - len(target_cards[color])
            if missing > 0 :
                for c in range(missing):
                    item = QtWidgets.QGraphicsPixmapItem(self.pixmaps["UNKNOWN"])
                    self.unknown_cards.append(item)
                    self.addItem(item)
                    item.setPos(x,y)
                    y += 30

    def mousePressEvent(self, mouseEvent):
        '''
        '''
        grabbedItem = self.itemAt( mouseEvent.buttonDownScenePos(QtCore.Qt.LeftButton),
                                   QtGui.QTransform() )
        
        if not grabbedItem:
            QtWidgets.QGraphicsScene.mousePressEvent(self, mouseEvent)
            return
            
        if grabbedItem in (self.itemSpinboxN, self.itemSpinboxW, self.itemSpinboxS, self.itemSpinboxE):
            QtWidgets.QGraphicsScene.mousePressEvent(self, mouseEvent)
            return
        
        self.grabbedItem = grabbedItem
            
        mousePos = mouseEvent.scenePos().toPoint()
        
        #print("item  pos", self.grabbedItem.pos())
        #print("mouse pos", mousePos)
        
        itemPos = QtCore.QPoint(self.grabbedItem.pos().x(), self.grabbedItem.pos().y())
        
        self.delta_grab = mousePos - itemPos
        
        QtWidgets.QGraphicsScene.mousePressEvent(self, mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        '''
        '''
        if self.grabbedItem:
            mousePos = mouseEvent.scenePos().toPoint()
            
            itemPos = mousePos - self.delta_grab
            item = mouseEvent.pos()
            
            self.grabbedItem.setPos(itemPos)
            
        QtWidgets.QGraphicsScene.mouseMoveEvent(self, mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        '''
        '''
        if self.grabbedItem:
            mousePos = mouseEvent.scenePos().toPoint()
            
            itemPos = mousePos - self.delta_grab
            
            self.grabbedItem.setPos(itemPos)
        
        if self.grabbedItem not in self.item_card:
            QtWidgets.QGraphicsScene.mouseReleaseEvent(self, mouseEvent)
            return

        card = self.item_card[self.grabbedItem]
        
        source_hand = None
        
        for hand in ("N", "S", "W", "E"):
            for color in Color:
                if card in self.deal.hand[hand].target_cards[color]:
                    source_hand = self.deal.hand[hand]
       
        target_hand = self.get_target_hand(mousePos)
        
        if source_hand:
            print("Source Hand " + source_hand.pos + "...")
            source_hand.target_cards[card.color()].remove(card)
        else:
            print("No Source Hand")
            
        if target_hand:
            print("Target Hand " + target_hand.pos + "...")
            target_hand.target_cards[card.color()].append(card)
        else:
            print("No Target Hand")
            
        self.delete_unknown_items()
        self.display_play_cards()
        self.display_deal()
            
        QtWidgets.QGraphicsScene.mouseReleaseEvent(self, mouseEvent)
        
        self.grabbedItem = None

    def get_target_hand(self, pos):
        '''
        '''
        x = pos.x()
        y = pos.y()
        
        for hand in ("N", "S", "W", "E"):
            area = self.target_area[hand]
        
            if area["x1"] <= x and x <= area["x2"] and area["y1"] <= y and y <= area["y2"]:
                return self.deal.hand[hand]
        
        return None
