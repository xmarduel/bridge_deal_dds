
from PySide6 import QtWidgets

from deal import Deal

class BridgeDDSView(QtWidgets.QTextBrowser):
    '''
    '''
    def __init__(self, parent=None):
        '''
        '''
        QtWidgets.QTextBrowser.__init__(self, parent)

    def display_dds(self, pbn: str):
        '''
        '''
        deal = Deal()
        deal.from_pbn(pbn)

        html = deal.get_dds_results_html()
        self.setHtml(html)