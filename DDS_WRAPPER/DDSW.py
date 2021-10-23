

'''
a wrapper around the dds ctypes "wrapper" dds.py
'''

import os
import ctypes

import dds
import hands
import functions

class DDS:
    '''
    '''
    NOTRUMP = hands.NOTRUMP
    SPADES = hands.SPADES
    HEARTS = hands.HEARTS
    DIAMONDS = hands.DIAMONDS
    CLUBS = hands.CLUBS
        
    NORTH = hands.NORTH
    EAST = hands.EAST
    SOUTH = hands.SOUTH
    WEST = hands.WEST

    def __init__(self):
        dds.SetMaxThreads(0)
            
    def show_pbn(self, pbn: str):
        '''
        '''
        tableDealPBN = dds.ddTableDealPBN()
        tableDealPBN.cards = pbn.encode('utf-8')

        line = ctypes.create_string_buffer(80)

        functions.PrintPBNHand(line, tableDealPBN.cards)

    def calc_dd_table(self, pbn: str):
        '''
        '''
        tableDealPBN = dds.ddTableDealPBN()
        tableDealPBN.cards = pbn.encode('utf-8')
        
        table = dds.ddTableResults()
        
        res = dds.CalcDDtablePBN(tableDealPBN, ctypes.pointer(table))

        if res != dds.RETURN_NO_FAULT:
            line = ctypes.create_string_buffer(80)

            dds.ErrorMessage(res, line)
            print("DDS error: {}".format(line.encode("utf-8")))
            return None
        else:
            line = ctypes.create_string_buffer(80)
            line = "CalcDDtable: {}".format("OK")

            functions.PrintPBNHand(line, tableDealPBN.cards)
            return table
  
    def print_dd_table(self, table):
        '''
        '''
        theTable = ctypes.pointer(table)
        functions.PrintTable(theTable)


if __name__ == '__main__':
    DDS = DDS()
    
    pbn = "N:KQ964.AK763.J6.Q AJ8.J5.Q92.KJ964 7.T42.AT84.AT875 T532.Q98.K753.32"
    
    DDS.show_pbn(pbn)

    res = DDS.calc_dd_table(pbn)
    DDS.print_dd_table(res)