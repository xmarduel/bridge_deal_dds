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
    cards_pics = {
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

    label_to_card = {
    '2s' : Card.S_2,
    '3s' : Card.S_3,
    '4s' : Card.S_4,
    '5s' : Card.S_5,
    '6s' : Card.S_6,
    '7s' : Card.S_7,
    '8s' : Card.S_8,
    '9s' : Card.S_9,
    '10s' : Card.S_T,
    'Js' : Card.S_J,
    'Qs' : Card.S_Q,
    'Ks' : Card.S_K,
    'As' : Card.S_A,

    '2h' : Card.H_2,
    '3h' : Card.H_3,
    '4h' : Card.H_4,
    '5h' : Card.H_5,
    '6h' : Card.H_6,
    '7h' : Card.H_7,
    '8h' : Card.H_8,
    '9h' : Card.H_9,
    '10h' : Card.H_T,
    'Jh' : Card.H_J,
    'Qh' : Card.H_Q,
    'Kh' : Card.H_K,
    'Ah' : Card.H_A,

    '2d' : Card.D_2,
    '3d' : Card.D_3,
    '4d' : Card.D_4,
    '5d' : Card.D_5,
    '6d' : Card.D_6,
    '7d' : Card.D_7,
    '8d' : Card.D_8,
    '9d' : Card.D_9,
    '10d' : Card.D_T,
    'Jd' : Card.D_J,
    'Qd' : Card.D_Q,
    'Kd' : Card.D_K,
    'Ad' : Card.D_A,

    '2c' : Card.C_2,
    '3c' : Card.C_3,
    '4c' : Card.C_4,
    '5c' : Card.C_5,
    '6c' : Card.C_6,
    '7c' : Card.C_7,
    '8c' : Card.C_8,
    '9c' : Card.C_9,
    '10c' : Card.C_T,
    'Jc' : Card.C_J,
    'Qc' : Card.C_Q,
    'Kc' : Card.C_K,
    'Ac' : Card.C_A,
    }

    size = 24

    def __init__(self, parent):
        super().__init__(parent)

        self.setLayout(QtWidgets.QHBoxLayout())

        self.count_indicator = QtWidgets.QLabel("#count")
        self.count_indicator.setText("0: ")
        self.layout().addWidget(self.count_indicator)


        self.cards_widgets = {}

        for label, card in self.label_to_card.items():
            w = QtSvgWidgets.QSvgWidget(self.cards_pics[card.name])
            w.setFixedSize(self.size,self.size)
            self.cards_widgets[card.name] = w
            self.layout().addWidget(w)
            w.hide()

    def display_cards(self, cards: List[Card]):
        '''
        '''
        for w in self.cards_widgets.values():
            w.hide()

        # sort cards
        def sortEnum(card):
            return card.order_value()

        cards.sort(reverse=False, key=sortEnum)

        for card in cards:
            self.cards_widgets[card.name].show()

        self.count_indicator.setText("%d: " % len(cards))
        
    def hand_from_labels(self, labels : List[str]):
        '''
        '''
        return [ self.label_to_card[label] for label in labels ]
