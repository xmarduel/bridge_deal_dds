# coding: utf8

from deal import Deal
from deal import Color
from deal import Card

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


class BridgeUIscene(QtWidgets.QGraphicsScene):
    """ """

    def __init__(self, deal):
        """ """
        QtWidgets.QGraphicsScene.__init__(self)

        self.deal = deal

        self.grabbedItem = None

        self.YY = 200  # reference height

        self.make_default_scene()
        self.display_deal()

        self.spinboxN.valueChanged.connect(self.cb_set_target_points_N)
        self.spinboxS.valueChanged.connect(self.cb_set_target_points_S)
        self.spinboxE.valueChanged.connect(self.cb_set_target_points_E)
        self.spinboxW.valueChanged.connect(self.cb_set_target_points_W)

        self.spinboxNbSpadesN.valueChanged.connect(self.cb_set_target_distribution_S_N)
        self.spinboxNbHeartsN.valueChanged.connect(self.cb_set_target_distribution_H_N)
        self.spinboxNbDiamsN.valueChanged.connect(self.cb_set_target_distribution_D_N)
        self.spinboxNbClubsN.valueChanged.connect(self.cb_set_target_distribution_C_N)

        self.spinboxNbSpadesS.valueChanged.connect(self.cb_set_target_distribution_S_S)
        self.spinboxNbHeartsS.valueChanged.connect(self.cb_set_target_distribution_H_S)
        self.spinboxNbDiamsS.valueChanged.connect(self.cb_set_target_distribution_D_S)
        self.spinboxNbClubsS.valueChanged.connect(self.cb_set_target_distribution_C_S)

        self.spinboxNbSpadesW.valueChanged.connect(self.cb_set_target_distribution_S_W)
        self.spinboxNbHeartsW.valueChanged.connect(self.cb_set_target_distribution_H_W)
        self.spinboxNbDiamsW.valueChanged.connect(self.cb_set_target_distribution_D_W)
        self.spinboxNbClubsW.valueChanged.connect(self.cb_set_target_distribution_C_W)

        self.spinboxNbSpadesE.valueChanged.connect(self.cb_set_target_distribution_S_E)
        self.spinboxNbHeartsE.valueChanged.connect(self.cb_set_target_distribution_H_E)
        self.spinboxNbDiamsE.valueChanged.connect(self.cb_set_target_distribution_D_E)
        self.spinboxNbClubsE.valueChanged.connect(self.cb_set_target_distribution_C_E)

        self.target_area = {
            "N": {"x1": 200, "x2": 300, "y1": 0, "y2": 200},
            "S": {"x1": 200, "x2": 300, "y1": 200, "y2": 999},
            "W": {"x1": 000, "x2": 200, "y1": 200, "y2": 999},
            "E": {"x1": 300, "x2": 999, "y1": 200, "y2": 999},
            "-": {"x1": 400, "x2": 999, "y1": 0, "y2": 999},
        }

    def cb_set_target_points_N(self, value):
        """ """
        self.deal.hand["N"].target_points = value

    def cb_set_target_points_S(self, value):
        """ """
        self.deal.hand["S"].target_points = value

    def cb_set_target_points_E(self, value):
        """ """
        self.deal.hand["E"].target_points = value

    def cb_set_target_points_W(self, value):
        """ """
        self.deal.hand["W"].target_points = value

    def redraw(self):
        self.delete_unknown_items()
        self.display_play_cards()
        self.display_deal()

    def cb_set_target_distribution_S_N(self, value):
        """ """
        self.deal.hand["N"].target_distribution[Color.SPADES] = value
        self.redraw()

    def cb_set_target_distribution_H_N(self, value):
        """ """
        self.deal.hand["N"].target_distribution[Color.HEARTS] = value
        self.redraw()

    def cb_set_target_distribution_D_N(self, value):
        """ """
        self.deal.hand["N"].target_distribution[Color.DIAMONDS] = value
        self.redraw()

    def cb_set_target_distribution_C_N(self, value):
        """ """
        print("NORTH CLUBS -> ", value)
        self.deal.hand["N"].target_distribution[Color.CLUBS] = value
        self.redraw()

    def cb_set_target_distribution_S_S(self, value):
        """ """
        self.deal.hand["S"].target_distribution[Color.SPADES] = value
        self.redraw()

    def cb_set_target_distribution_H_S(self, value):
        """ """
        self.deal.hand["S"].target_distribution[Color.HEARTS] = value
        self.redraw()

    def cb_set_target_distribution_D_S(self, value):
        """ """
        self.deal.hand["S"].target_distribution[Color.DIAMONDS] = value
        self.redraw()

    def cb_set_target_distribution_C_S(self, value):
        """ """
        self.deal.hand["S"].target_distribution[Color.CLUBS] = value
        self.redraw()

    def cb_set_target_distribution_S_W(self, value):
        """ """
        self.deal.hand["W"].target_distribution[Color.SPADES] = value
        self.redraw()

    def cb_set_target_distribution_H_W(self, value):
        """ """
        self.deal.hand["W"].target_distribution[Color.HEARTS] = value
        self.redraw()

    def cb_set_target_distribution_D_W(self, value):
        """ """
        self.deal.hand["W"].target_distribution[Color.DIAMONDS] = value
        self.redraw()

    def cb_set_target_distribution_C_W(self, value):
        """ """
        self.deal.hand["W"].target_distribution[Color.CLUBS] = value
        self.redraw()

    def cb_set_target_distribution_S_E(self, value):
        """ """
        self.deal.hand["E"].target_distribution[Color.SPADES] = value
        self.redraw()

    def cb_set_target_distribution_H_E(self, value):
        """ """
        self.deal.hand["E"].target_distribution[Color.HEARTS] = value
        self.redraw()

    def cb_set_target_distribution_D_E(self, value):
        """ """
        self.deal.hand["E"].target_distribution[Color.DIAMONDS] = value
        self.redraw()

    def cb_set_target_distribution_C_E(self, value):
        """ """
        self.deal.hand["E"].target_distribution[Color.CLUBS] = value
        self.redraw()

    def make_default_scene(self):
        """ """
        # deal layout - table
        self.addRect(200, self.YY, 100, 100)
        # with annotations
        self.addText("N").setPos(240, self.YY)
        self.addText("S").setPos(240, self.YY + 80)
        self.addText("E").setPos(285, self.YY + 40)
        self.addText("W").setPos(200, self.YY + 40)

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

        itemSpinboxN.setPos(200, self.YY - 30)
        itemSpinboxN.setMinimumSize(100, 20)

        itemSpinboxS.setPos(200, self.YY + 110)
        itemSpinboxS.setMinimumSize(100, 20)

        itemSpinboxE.setPos(310, self.YY)
        itemSpinboxE.setMinimumSize(100, 20)

        itemSpinboxW.setPos(90, self.YY)
        itemSpinboxW.setMinimumSize(100, 20)

        # -- NORTH -------------------------------------------------------------

        # placeholder for the user hands with predefined card : the 4 colors

        x = {
            "♠": 200,
            "♥": 225,
            "♦": 250,
            "♣": 275,
        }
        y = self.YY - 55

        self.itemNP = self.addText("♠")
        self.itemNP.setPos(x["♠"], y)
        self.itemNC = self.addText("♥")
        self.itemNC.setPos(x["♥"], y)
        self.itemNK = self.addText("♦")
        self.itemNK.setPos(x["♦"], y)
        self.itemNT = self.addText("♣")
        self.itemNT.setPos(x["♣"], y)
        self.itemNC.setDefaultTextColor(QtGui.QColor("red"))
        self.itemNK.setDefaultTextColor(QtGui.QColor("red"))

        # user input : target number of card for each color ---------

        self.spinboxNbSpadesN = QtWidgets.QSpinBox()
        self.spinboxNbHeartsN = QtWidgets.QSpinBox()
        self.spinboxNbDiamsN = QtWidgets.QSpinBox()
        self.spinboxNbClubsN = QtWidgets.QSpinBox()

        self.spinboxNbSpadesN.setMaximum(13)
        self.spinboxNbSpadesN.setMinimum(-1)

        self.spinboxNbHeartsN.setMaximum(13)
        self.spinboxNbHeartsN.setMinimum(-1)

        self.spinboxNbDiamsN.setMaximum(13)
        self.spinboxNbDiamsN.setMinimum(-1)

        self.spinboxNbClubsN.setMaximum(13)
        self.spinboxNbClubsN.setMinimum(-1)

        self.itemSpinboxNbSpadesN = self.addWidget(self.spinboxNbSpadesN)
        self.itemSpinboxNbHeartsN = self.addWidget(self.spinboxNbHeartsN)
        self.itemSpinboxNbDiamsN = self.addWidget(self.spinboxNbDiamsN)
        self.itemSpinboxNbClubsN = self.addWidget(self.spinboxNbClubsN)

        self.itemSpinboxNbSpadesN.setPos(x["♠"] - 8, self.YY - 75)
        self.itemSpinboxNbSpadesN.setMaximumSize(29, 20)

        self.itemSpinboxNbHeartsN.setPos(x["♥"] - 4, self.YY - 75)
        self.itemSpinboxNbHeartsN.setMaximumSize(29, 20)

        self.itemSpinboxNbDiamsN.setPos(x["♦"] + 0, self.YY - 75)
        self.itemSpinboxNbDiamsN.setMaximumSize(29, 20)

        self.itemSpinboxNbClubsN.setPos(x["♣"] + 4, self.YY - 75)
        self.itemSpinboxNbClubsN.setMaximumSize(29, 20)

        # -- SOUTH -------------------------------------------------------------

        x = {
            "♠": 200,
            "♥": 225,
            "♦": 250,
            "♣": 275,
        }
        y = self.YY + 130

        self.itemSP = self.addText("♠")
        self.itemSP.setPos(x["♠"], y)
        self.itemSC = self.addText("♥")
        self.itemSC.setPos(x["♥"], y)
        self.itemSK = self.addText("♦")
        self.itemSK.setPos(x["♦"], y)
        self.itemST = self.addText("♣")
        self.itemST.setPos(x["♣"], y)
        self.itemSC.setDefaultTextColor(QtGui.QColor("red"))
        self.itemSK.setDefaultTextColor(QtGui.QColor("red"))

        # user input : target number of card for each color ---------
        self.spinboxNbSpadesS = QtWidgets.QSpinBox()
        self.spinboxNbHeartsS = QtWidgets.QSpinBox()
        self.spinboxNbDiamsS = QtWidgets.QSpinBox()
        self.spinboxNbClubsS = QtWidgets.QSpinBox()

        self.spinboxNbSpadesS.setMaximum(13)
        self.spinboxNbSpadesS.setMinimum(-1)

        self.spinboxNbHeartsS.setMaximum(13)
        self.spinboxNbHeartsS.setMinimum(-1)

        self.spinboxNbDiamsS.setMaximum(13)
        self.spinboxNbDiamsS.setMinimum(-1)

        self.spinboxNbClubsS.setMaximum(13)
        self.spinboxNbClubsS.setMinimum(-1)

        self.itemSpinboxNbSpadesS = self.addWidget(self.spinboxNbSpadesS)
        self.itemSpinboxNbHeartsS = self.addWidget(self.spinboxNbHeartsS)
        self.itemSpinboxNbDiamsS = self.addWidget(self.spinboxNbDiamsS)
        self.itemSpinboxNbClubsS = self.addWidget(self.spinboxNbClubsS)

        self.itemSpinboxNbSpadesS.setPos(x["♠"] - 8, self.YY + 155)
        self.itemSpinboxNbSpadesS.setMaximumSize(29, 20)

        self.itemSpinboxNbHeartsS.setPos(x["♥"] - 4, self.YY + 155)
        self.itemSpinboxNbHeartsS.setMaximumSize(29, 20)

        self.itemSpinboxNbDiamsS.setPos(x["♦"] + 0, self.YY + 155)
        self.itemSpinboxNbDiamsS.setMaximumSize(29, 20)

        self.itemSpinboxNbClubsS.setPos(x["♣"] + 4, self.YY + 155)
        self.itemSpinboxNbClubsS.setMaximumSize(29, 20)

        # -- EAST -------------------------------------------------------------

        x = {
            "♠": 310,
            "♥": 335,
            "♦": 360,
            "♣": 385,
        }
        y = self.YY + 20

        self.itemEP = self.addText("♠")
        self.itemEP.setPos(x["♠"], y)
        self.itemEC = self.addText("♥")
        self.itemEC.setPos(x["♥"], y)
        self.itemEK = self.addText("♦")
        self.itemEK.setPos(x["♦"], y)
        self.itemET = self.addText("♣")
        self.itemET.setPos(x["♣"], y)
        self.itemEC.setDefaultTextColor(QtGui.QColor("red"))
        self.itemEK.setDefaultTextColor(QtGui.QColor("red"))

        # user input : target number of card for each color ---------
        self.spinboxNbSpadesE = QtWidgets.QSpinBox()
        self.spinboxNbHeartsE = QtWidgets.QSpinBox()
        self.spinboxNbDiamsE = QtWidgets.QSpinBox()
        self.spinboxNbClubsE = QtWidgets.QSpinBox()

        self.spinboxNbSpadesE.setMaximum(13)
        self.spinboxNbSpadesE.setMinimum(-1)

        self.spinboxNbHeartsE.setMaximum(13)
        self.spinboxNbHeartsE.setMinimum(-1)

        self.spinboxNbDiamsE.setMaximum(13)
        self.spinboxNbDiamsE.setMinimum(-1)

        self.spinboxNbClubsE.setMaximum(13)
        self.spinboxNbClubsE.setMinimum(-1)

        self.itemSpinboxNbSpadesE = self.addWidget(self.spinboxNbSpadesE)
        self.itemSpinboxNbHeartsE = self.addWidget(self.spinboxNbHeartsE)
        self.itemSpinboxNbDiamsE = self.addWidget(self.spinboxNbDiamsE)
        self.itemSpinboxNbClubsE = self.addWidget(self.spinboxNbClubsE)

        self.itemSpinboxNbSpadesE.setPos(x["♠"] - 8, self.YY + 45)
        self.itemSpinboxNbSpadesE.setMaximumSize(29, 20)

        self.itemSpinboxNbHeartsE.setPos(x["♥"] - 4, self.YY + 45)
        self.itemSpinboxNbHeartsE.setMaximumSize(29, 20)

        self.itemSpinboxNbDiamsE.setPos(x["♦"] + 0, self.YY + 45)
        self.itemSpinboxNbDiamsE.setMaximumSize(29, 20)

        self.itemSpinboxNbClubsE.setPos(x["♣"] + 4, self.YY + 45)
        self.itemSpinboxNbClubsE.setMaximumSize(29, 20)

        # -- WEST -------------------------------------------------------------

        x = {
            "♠": 90,
            "♥": 115,
            "♦": 140,
            "♣": 165,
        }
        y = self.YY + 20

        self.itemWP = self.addText("♠")
        self.itemWP.setPos(x["♠"], y)
        self.itemWC = self.addText("♥")
        self.itemWC.setPos(x["♥"], y)
        self.itemWK = self.addText("♦")
        self.itemWK.setPos(x["♦"], y)
        self.itemWT = self.addText("♣")
        self.itemWT.setPos(x["♣"], y)
        self.itemWC.setDefaultTextColor(QtGui.QColor("red"))
        self.itemWK.setDefaultTextColor(QtGui.QColor("red"))

        # user input : target number of card for each color ---------
        self.spinboxNbSpadesW = QtWidgets.QSpinBox()
        self.spinboxNbHeartsW = QtWidgets.QSpinBox()
        self.spinboxNbDiamsW = QtWidgets.QSpinBox()
        self.spinboxNbClubsW = QtWidgets.QSpinBox()

        self.spinboxNbSpadesW.setMaximum(13)
        self.spinboxNbSpadesW.setMinimum(-1)

        self.spinboxNbHeartsW.setMaximum(13)
        self.spinboxNbHeartsW.setMinimum(-1)

        self.spinboxNbDiamsW.setMaximum(13)
        self.spinboxNbDiamsW.setMinimum(-1)

        self.spinboxNbClubsW.setMaximum(13)
        self.spinboxNbClubsW.setMinimum(-1)

        self.itemSpinboxNbSpadesW = self.addWidget(self.spinboxNbSpadesW)
        self.itemSpinboxNbHeartsW = self.addWidget(self.spinboxNbHeartsW)
        self.itemSpinboxNbDiamsW = self.addWidget(self.spinboxNbDiamsW)
        self.itemSpinboxNbClubsW = self.addWidget(self.spinboxNbClubsW)

        self.itemSpinboxNbSpadesW.setPos(x["♠"] - 8, self.YY + 45)
        self.itemSpinboxNbSpadesW.setMaximumSize(29, 20)

        self.itemSpinboxNbHeartsW.setPos(x["♥"] - 4, self.YY + 45)
        self.itemSpinboxNbHeartsW.setMaximumSize(29, 20)

        self.itemSpinboxNbDiamsW.setPos(x["♦"] + 0, self.YY + 45)
        self.itemSpinboxNbDiamsW.setMaximumSize(29, 20)

        self.itemSpinboxNbClubsW.setPos(x["♣"] + 4, self.YY + 45)
        self.itemSpinboxNbClubsW.setMaximumSize(29, 20)
        # ---------------------------------------------------------------

        # the game cards to select into the user cards
        self.populate_card_item()

    def populate_card_item(self):
        """ """
        cardset = "naylor"
        suffix = "gif"

        cardset = "quadrat"
        suffix = "png"

        SIZE = 25

        self.pixmaps = {
            "UNKNOWN": QtGui.QPixmap("cardset-%s/unknown.gif" % cardset).scaled(
                SIZE, SIZE
            ),
            Card.S_A: QtGui.QPixmap("cardset-%s/As.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.S_K: QtGui.QPixmap("cardset-%s/Ks.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.S_Q: QtGui.QPixmap("cardset-%s/Qs.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.S_J: QtGui.QPixmap("cardset-%s/Js.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.S_T: QtGui.QPixmap("cardset-%s/10s.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.S_9: QtGui.QPixmap("cardset-%s/9s.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.S_8: QtGui.QPixmap("cardset-%s/8s.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.S_7: QtGui.QPixmap("cardset-%s/7s.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.S_6: QtGui.QPixmap("cardset-%s/6s.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.S_5: QtGui.QPixmap("cardset-%s/5s.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.S_4: QtGui.QPixmap("cardset-%s/4s.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.S_3: QtGui.QPixmap("cardset-%s/3s.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.S_2: QtGui.QPixmap("cardset-%s/2s.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.H_A: QtGui.QPixmap("cardset-%s/Ah.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.H_K: QtGui.QPixmap("cardset-%s/Kh.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.H_Q: QtGui.QPixmap("cardset-%s/Qh.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.H_J: QtGui.QPixmap("cardset-%s/Jh.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.H_T: QtGui.QPixmap("cardset-%s/10h.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.H_9: QtGui.QPixmap("cardset-%s/9h.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.H_8: QtGui.QPixmap("cardset-%s/8h.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.H_7: QtGui.QPixmap("cardset-%s/7h.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.H_6: QtGui.QPixmap("cardset-%s/6h.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.H_5: QtGui.QPixmap("cardset-%s/5h.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.H_4: QtGui.QPixmap("cardset-%s/4h.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.H_3: QtGui.QPixmap("cardset-%s/3h.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.H_2: QtGui.QPixmap("cardset-%s/2h.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.D_A: QtGui.QPixmap("cardset-%s/Ad.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.D_K: QtGui.QPixmap("cardset-%s/Kd.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.D_Q: QtGui.QPixmap("cardset-%s/Qd.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.D_J: QtGui.QPixmap("cardset-%s/Jd.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.D_T: QtGui.QPixmap("cardset-%s/10d.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.D_9: QtGui.QPixmap("cardset-%s/9d.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.D_8: QtGui.QPixmap("cardset-%s/8d.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.D_7: QtGui.QPixmap("cardset-%s/7d.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.D_6: QtGui.QPixmap("cardset-%s/6d.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.D_5: QtGui.QPixmap("cardset-%s/5d.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.D_4: QtGui.QPixmap("cardset-%s/4d.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.D_3: QtGui.QPixmap("cardset-%s/3d.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.D_2: QtGui.QPixmap("cardset-%s/2d.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.C_A: QtGui.QPixmap("cardset-%s/Ac.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.C_K: QtGui.QPixmap("cardset-%s/Kc.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.C_Q: QtGui.QPixmap("cardset-%s/Qc.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.C_J: QtGui.QPixmap("cardset-%s/Jc.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.C_T: QtGui.QPixmap("cardset-%s/10c.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.C_9: QtGui.QPixmap("cardset-%s/9c.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.C_8: QtGui.QPixmap("cardset-%s/8c.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.C_7: QtGui.QPixmap("cardset-%s/7c.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.C_6: QtGui.QPixmap("cardset-%s/6c.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.C_5: QtGui.QPixmap("cardset-%s/5c.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.C_4: QtGui.QPixmap("cardset-%s/4c.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.C_3: QtGui.QPixmap("cardset-%s/3c.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
            Card.C_2: QtGui.QPixmap("cardset-%s/2c.%s" % (cardset, suffix)).scaled(
                SIZE, SIZE
            ),
        }

        self.card_item = {
            Card.S_A: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_A]),
            Card.S_K: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_K]),
            Card.S_Q: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_Q]),
            Card.S_J: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_J]),
            Card.S_T: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_T]),
            Card.S_9: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_9]),
            Card.S_8: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_8]),
            Card.S_7: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_7]),
            Card.S_6: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_6]),
            Card.S_5: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_5]),
            Card.S_4: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_4]),
            Card.S_3: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_3]),
            Card.S_2: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.S_2]),
            Card.H_A: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_A]),
            Card.H_K: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_K]),
            Card.H_Q: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_Q]),
            Card.H_J: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_J]),
            Card.H_T: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_T]),
            Card.H_9: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_9]),
            Card.H_8: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_8]),
            Card.H_7: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_7]),
            Card.H_6: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_6]),
            Card.H_5: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_5]),
            Card.H_4: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_4]),
            Card.H_3: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_3]),
            Card.H_2: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.H_2]),
            Card.D_A: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_A]),
            Card.D_K: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_K]),
            Card.D_Q: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_Q]),
            Card.D_J: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_J]),
            Card.D_T: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_T]),
            Card.D_9: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_9]),
            Card.D_8: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_8]),
            Card.D_7: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_7]),
            Card.D_6: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_6]),
            Card.D_5: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_5]),
            Card.D_4: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_4]),
            Card.D_3: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_3]),
            Card.D_2: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.D_2]),
            Card.C_A: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_A]),
            Card.C_K: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_K]),
            Card.C_Q: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_Q]),
            Card.C_J: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_J]),
            Card.C_T: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_T]),
            Card.C_9: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_9]),
            Card.C_8: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_8]),
            Card.C_7: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_7]),
            Card.C_6: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_6]),
            Card.C_5: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_5]),
            Card.C_4: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_4]),
            Card.C_3: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_3]),
            Card.C_2: QtWidgets.QGraphicsPixmapItem(self.pixmaps[Card.C_2]),
        }

        # map item -> card
        self.item_card = {}

        for card in self.card_item:
            item = self.card_item[card]
            self.item_card[item] = card

        self.unknown_cards = {"N": [], "S": [], "W": [], "E": []}

        self.make_cards_play()
        self.display_play_cards()

    def delete_unknown_items(self):
        """ """
        for pos in list(self.unknown_cards.keys()):
            for item in self.unknown_cards[pos]:
                self.removeItem(item)

        self.unknown_cards = {"N": [], "S": [], "W": [], "E": []}

    def make_cards_play(self):
        """ """
        for card in self.card_item:
            item = self.card_item[card]
            self.addItem(item)

    def display_play_cards(self):
        """ """
        initial_x_position = {
            Color.SPADES: 450,
            Color.HEARTS: 480,
            Color.DIAMONDS: 510,
            Color.CLUBS: 540,
        }

        initial_y_position = 10

        for color in Color:
            y = initial_y_position
            for card in self.card_item:
                if card.color() != color:
                    continue

                item = self.card_item[card]
                item.setPos(initial_x_position[color], y)
                y += 30

    def display_deal(self):
        """ """
        # target points
        self.spinboxN.setValue(self.deal.hand["N"].target_points)
        self.spinboxS.setValue(self.deal.hand["S"].target_points)
        self.spinboxE.setValue(self.deal.hand["E"].target_points)
        self.spinboxW.setValue(self.deal.hand["W"].target_points)

        self.spinboxNbSpadesN.setValue(
            self.deal.hand["N"].target_distribution[Color.SPADES]
        )
        self.spinboxNbHeartsN.setValue(
            self.deal.hand["N"].target_distribution[Color.HEARTS]
        )
        self.spinboxNbDiamsN.setValue(
            self.deal.hand["N"].target_distribution[Color.DIAMONDS]
        )
        self.spinboxNbClubsN.setValue(
            self.deal.hand["N"].target_distribution[Color.CLUBS]
        )

        self.spinboxNbSpadesS.setValue(
            self.deal.hand["S"].target_distribution[Color.SPADES]
        )
        self.spinboxNbHeartsS.setValue(
            self.deal.hand["S"].target_distribution[Color.HEARTS]
        )
        self.spinboxNbDiamsS.setValue(
            self.deal.hand["S"].target_distribution[Color.DIAMONDS]
        )
        self.spinboxNbClubsS.setValue(
            self.deal.hand["S"].target_distribution[Color.CLUBS]
        )

        self.spinboxNbSpadesW.setValue(
            self.deal.hand["W"].target_distribution[Color.SPADES]
        )
        self.spinboxNbHeartsW.setValue(
            self.deal.hand["W"].target_distribution[Color.HEARTS]
        )
        self.spinboxNbDiamsW.setValue(
            self.deal.hand["W"].target_distribution[Color.DIAMONDS]
        )
        self.spinboxNbClubsW.setValue(
            self.deal.hand["W"].target_distribution[Color.CLUBS]
        )

        self.spinboxNbSpadesE.setValue(
            self.deal.hand["E"].target_distribution[Color.SPADES]
        )
        self.spinboxNbHeartsE.setValue(
            self.deal.hand["E"].target_distribution[Color.HEARTS]
        )
        self.spinboxNbDiamsE.setValue(
            self.deal.hand["E"].target_distribution[Color.DIAMONDS]
        )
        self.spinboxNbClubsE.setValue(
            self.deal.hand["E"].target_distribution[Color.CLUBS]
        )

        self.display_hand("N")
        self.display_hand("S")
        self.display_hand("E")
        self.display_hand("W")

    def display_hand(self, pos):
        """ """
        initial_x_position = {
            "N": {
                Color.SPADES: 200,
                Color.HEARTS: 225,
                Color.DIAMONDS: 250,
                Color.CLUBS: 275,
            },
            "S": {
                Color.SPADES: 200,
                Color.HEARTS: 225,
                Color.DIAMONDS: 250,
                Color.CLUBS: 275,
            },
            "W": {
                Color.SPADES: 90,
                Color.HEARTS: 115,
                Color.DIAMONDS: 140,
                Color.CLUBS: 165,
            },
            "E": {
                Color.SPADES: 310,
                Color.HEARTS: 335,
                Color.DIAMONDS: 360,
                Color.CLUBS: 385,
            },
        }

        initial_y_position = {
            "N": self.YY - 80,
            "S": self.YY + 180,
            "W": self.YY + 75,
            "E": self.YY + 75,
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

            max_nb_cards = max(
                max_nb_cards, self.deal.hand["N"].target_distribution[Color.SPADES]
            )
            max_nb_cards = max(
                max_nb_cards, self.deal.hand["N"].target_distribution[Color.HEARTS]
            )
            max_nb_cards = max(
                max_nb_cards, self.deal.hand["N"].target_distribution[Color.DIAMONDS]
            )
            max_nb_cards = max(
                max_nb_cards, self.deal.hand["N"].target_distribution[Color.CLUBS]
            )

        # --------------------------------------------------------------------------------

        for color in Color:
            target_cards[color] = self.deal.hand[pos].target_cards[color]

            x = initial_x_position[pos][color]
            y = initial_y_position[pos]

            if pos == "N":
                h = max_nb_cards * (25 + 5)
                y = y - h

            for card in target_cards[color]:
                item = self.card_item[card]
                item.setPos(x, y)
                y += 30

            missing = self.deal.hand[pos].target_distribution[color] - len(
                target_cards[color]
            )
            if missing > 0:
                for c in range(missing):
                    item = QtWidgets.QGraphicsPixmapItem(self.pixmaps["UNKNOWN"])
                    self.unknown_cards[pos].append(item)
                    self.addItem(item)
                    item.setPos(x, y)
                    y += 30

    def mousePressEvent(self, mouseEvent):
        """ """
        grabbedItem = self.itemAt(
            mouseEvent.buttonDownScenePos(QtCore.Qt.LeftButton), QtGui.QTransform()
        )

        if not grabbedItem:
            QtWidgets.QGraphicsScene.mousePressEvent(self, mouseEvent)
            return

        if grabbedItem in (
            self.itemSpinboxN,
            self.itemSpinboxW,
            self.itemSpinboxS,
            self.itemSpinboxE,
        ):
            QtWidgets.QGraphicsScene.mousePressEvent(self, mouseEvent)
            return

        if grabbedItem in (
            self.itemNP,
            self.itemNC,
            self.itemNK,
            self.itemNT,
            self.itemSP,
            self.itemSC,
            self.itemSK,
            self.itemST,
            self.itemWP,
            self.itemWC,
            self.itemWK,
            self.itemWT,
            self.itemEP,
            self.itemEC,
            self.itemEK,
            self.itemET,
        ):
            QtWidgets.QGraphicsScene.mousePressEvent(self, mouseEvent)
            return

        # ------------------------------------------------------------------
        try:
            if grabbedItem in (
                self.itemSpinboxNbSpadesN,
                self.itemSpinboxNbHeartsN,
                self.itemSpinboxNbDiamsN,
                self.itemSpinboxNbClubsN,
                self.itemSpinboxNbSpadesS,
                self.itemSpinboxNbHeartsS,
                self.itemSpinboxNbDiamsS,
                self.itemSpinboxNbClubsS,
                self.itemSpinboxNbSpadesW,
                self.itemSpinboxNbHeartsW,
                self.itemSpinboxNbDiamsW,
                self.itemSpinboxNbClubsW,
                self.itemSpinboxNbSpadesE,
                self.itemSpinboxNbHeartsE,
                self.itemSpinboxNbDiamsE,
                self.itemSpinboxNbClubsE,
            ):
                QtWidgets.QGraphicsScene.mousePressEvent(self, mouseEvent)
                return
        except Exception:
            pass
        # ------------------------------------------------------------------

        self.grabbedItem = grabbedItem

        mousePos = mouseEvent.scenePos().toPoint()

        # print("item  pos", self.grabbedItem.pos())
        # print("mouse pos", mousePos)

        itemPos = QtCore.QPoint(self.grabbedItem.pos().x(), self.grabbedItem.pos().y())

        self.delta_grab = mousePos - itemPos

        QtWidgets.QGraphicsScene.mousePressEvent(self, mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        """ """
        if self.grabbedItem:
            mousePos = mouseEvent.scenePos().toPoint()

            itemPos = mousePos - self.delta_grab
            item = mouseEvent.pos()

            self.grabbedItem.setPos(itemPos)

        QtWidgets.QGraphicsScene.mouseMoveEvent(self, mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        """ """
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
        """ """
        x = pos.x()
        y = pos.y()

        for hand in ("N", "S", "W", "E"):
            area = self.target_area[hand]

            if (
                area["x1"] <= x
                and x <= area["x2"]
                and area["y1"] <= y
                and y <= area["y2"]
            ):
                return self.deal.hand[hand]

        return None
