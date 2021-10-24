from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

from deal import Deal
from deal import Color

class BridgeDDSView(QtWidgets.QTextBrowser):
    '''
    '''
    def __init__(self):
        super().__init__()

    def display_dds(self, pbn: str):
        '''
        '''
        deal = Deal()
        deal.from_pbn(pbn)

        html = deal.get_dds_results_html()
        self.setHtml(html)