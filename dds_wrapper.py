

'''
a wrapper around the dds.dll with ctypes
'''

import os
import ctypes


class dds_ddTableResults(ctypes.Structure):
    '''
    '''
    _fields_ = [("resTable", ctypes.c_int * 4 * 5 ) ]

class dds_ddTableResultsWrapper:
    '''
    'cos cannot add method to a Structure directly
    '''
    def __init__(self, result):
        self.result = result
        
    def data(self, i, j):
        return self.result.contents.resTable[i][j]


class dds:
    '''
    '''
    NOTRUMP = 4
    SPADES = 0
    HEARTS = 1
    DIAMONDS = 2
    CLUBS = 3
        
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
        
    def __init__(self):
        os.add_dll_directory("C:\\msys64\\mingw64\\bin")
        self.dll = ctypes.WinDLL("C:\\Users\\xavie\\Documents\\GITHUB\\bridge_dds\\dds.dll")
        
        self.dll.calc_dd_table.restype = ctypes.POINTER(dds_ddTableResults)
        self.dll.show_result.argtypes  = [ctypes.POINTER(dds_ddTableResults)]
        
        
    def show_deal(self, pbn: str):
        '''
        '''
        b_pbn = pbn.encode('utf-8')
        c_pbn = ctypes.create_string_buffer(b_pbn)
        self.dll.show_deal(c_pbn)
        
    def calc_dd_table(self, pbn: str):
        '''
        '''
        b_pbn = pbn.encode('utf-8')
        c_pbn = ctypes.create_string_buffer(b_pbn)
        
        result = self.dll.calc_dd_table(c_pbn)
        
        return result
        
    def calc_and_show_result(self, pbn: str):
        '''
        '''
        b_pbn = pbn.encode('utf-8')
        c_pbn = ctypes.create_string_buffer(b_pbn)
        
        self.dll.calc_and_show_result(c_pbn)
        
    def show_result(self, result: any):
        '''
        '''                           
        self.dll.show_result(result)
        
    def solve_board(self, pbn: str, 
                    trump: int,
                    first: int,
                    first_card_suit: int,
                    first_card_rank: int,
                    target: int,
                    solutions: int,
                    mode: int):
        '''
        '''
        b_pbn = pbn.encode('utf-8')
        c_pbn = ctypes.create_string_buffer(b_pbn)
        
        self.dll.solve_board(c_pbn, 
            trump, 
            first,
            first_card_suit,
            first_card_rank,
            target,
            solutions, 
            mode)
        
        
        
if __name__ == '__main__':
    dds = dds()
    
    pbn = "N:KQ964.AK763.J6.Q AJ8.J5.Q92.KJ964 7.T42.AT84.AT875 T532.Q98.K753.32"
    dds.show_deal(pbn)
    
    dds.calc_and_show_result(pbn)
    
    res = dds.calc_dd_table(pbn)
    dds.show_result(res)     

    #print(dds_ddTableResultsWrapper(res).data(2,2))    