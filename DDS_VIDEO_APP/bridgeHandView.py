from typing import List

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets
from PySide6 import QtSvgWidgets

from deal import Deal
from deal import Card

class BridgeHandView(QtWidgets.QWidget):
    '''
    '''
    cards_files = {
    'S_2' : 'cardset-quadrat/2s.svg',
    'S_3' : 'cardset-quadrat/3s.svg',
    'S_4' : 'cardset-quadrat/4s.svg',
    'S_5' : 'cardset-quadrat/5s.svg',
    'S_6' : 'cardset-quadrat/6s.svg',
    'S_7' : 'cardset-quadrat/7s.svg',
    'S_8' : 'cardset-quadrat/8s.svg',
    'S_9' : 'cardset-quadrat/9s.svg',
    'S_T' : 'cardset-quadrat/10s.svg',
    'S_J' : 'cardset-quadrat/Js.svg',
    'S_Q' : 'cardset-quadrat/Qs.svg',
    'S_K' : 'cardset-quadrat/Ks.svg',
    'S_A' : 'cardset-quadrat/As.svg',

    'H_2' : 'cardset-quadrat/2h.svg',
    'H_3' : 'cardset-quadrat/3h.svg',
    'H_4' : 'cardset-quadrat/4h.svg',
    'H_5' : 'cardset-quadrat/5h.svg',
    'H_6' : 'cardset-quadrat/6h.svg',
    'H_7' : 'cardset-quadrat/7h.svg',
    'H_8' : 'cardset-quadrat/8h.svg',
    'H_9' : 'cardset-quadrat/9h.svg',
    'H_T' : 'cardset-quadrat/10h.svg',
    'H_J' : 'cardset-quadrat/Jh.svg',
    'H_Q' : 'cardset-quadrat/Qh.svg',
    'H_K' : 'cardset-quadrat/Kh.svg',
    'H_A' : 'cardset-quadrat/Ah.svg',

    'D_2' : 'cardset-quadrat/2d.svg',
    'D_3' : 'cardset-quadrat/3d.svg',
    'D_4' : 'cardset-quadrat/4d.svg',
    'D_5' : 'cardset-quadrat/5d.svg',
    'D_6' : 'cardset-quadrat/6d.svg',
    'D_7' : 'cardset-quadrat/7d.svg',
    'D_8' : 'cardset-quadrat/8d.svg',
    'D_9' : 'cardset-quadrat/9d.svg',
    'D_T' : 'cardset-quadrat/10d.svg',
    'D_J' : 'cardset-quadrat/Jd.svg',
    'D_Q' : 'cardset-quadrat/Qd.svg',
    'D_K' : 'cardset-quadrat/Kd.svg',
    'D_A' : 'cardset-quadrat/Ad.svg',

    'C_2' : 'cardset-quadrat/2c.svg',
    'C_3' : 'cardset-quadrat/3c.svg',
    'C_4' : 'cardset-quadrat/4c.svg',
    'C_5' : 'cardset-quadrat/5c.svg',
    'C_6' : 'cardset-quadrat/6c.svg',
    'C_7' : 'cardset-quadrat/7c.svg',
    'C_8' : 'cardset-quadrat/8c.svg',
    'C_9' : 'cardset-quadrat/9c.svg',
    'C_T' : 'cardset-quadrat/10c.svg',
    'C_J' : 'cardset-quadrat/Jc.svg',
    'C_Q' : 'cardset-quadrat/Qc.svg',
    'C_K' : 'cardset-quadrat/Kc.svg',
    'C_A' : 'cardset-quadrat/Ac.svg',
    }

    size = 24

    def __init__(self):
        super().__init__()

        self.setLayout(QtWidgets.QHBoxLayout())

    def clear(self):
        '''
        '''
        if self.layout() != None:
            while self.layout().itemAt(0) != None:
                item = self.layout().takeAt(0)
                w = item.widget()
                w.destroy()

    def display_cards(self, cards: List[Card]):
        '''
        '''
        self.clear()

        # sort cards
        def sortEnum(a):
            return a.order_value()

        cards.sort(reverse=False, key=sortEnum)

        for card in cards:
            card_widget = QtSvgWidgets.QSvgWidget(self.cards_files[card.name])
            card_widget.setFixedSize(self.size,self.size)
            self.layout().addWidget(card_widget)

        self.layout().addStretch(1)