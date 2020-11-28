#coding: utf8

VERSION = "0.1"

import sys
import argparse
import logging
import colorama

from deal import Deal


def main(pbn):
    '''
    print deal from pbn & display dds
    '''
    deal = Deal()
    deal.from_pbn(pbn)
    deal.generate()

    deal.print_table()
    #print(deal.to_pbn())
    print(deal.dds_results())


if __name__ == '__main__':
    colorama.init()

    #logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.basicConfig(format='%(message)s', level=logging.INFO)

    parser = argparse.ArgumentParser(prog="PbnDds", description="Read Pbn, show DDSl")

    # options
    pbn = sys.argv[1]

    print("pbn : '%s'" % pbn)
    pbn = "N:KQJ65.AQT64..K52 AT32.J53.KQJ72.J .9872.A83.AT7643 9874.K.T9654.Q98"

    main(pbn)
