#coding: utf8

VERSION = "0.1"

import argparse
import logging
import colorama

from deal import Deal
from deal import Color
from deal import Card
from deal import Hand
from deal import DealError


def main(options):
    '''
    generate/print deal(s)
    '''
    logger = logging.Logger('Deal')

    for _ in range(options.nbTry):
        deal = Deal()

        test = 3

        if test == 1:
            deal.hand["N"].target_distribution[Color.SPADES] = 5
            deal.hand["N"].target_distribution[Color.HEARTS] = 5
            deal.hand["N"].target_cards[Color.SPADES] = [Card.S_K, Card.S_Q]
            deal.hand["N"].target_cards[Color.HEARTS] = [Card.H_A]
            deal.hand["N"].target_points = 15
            deal.hand["S"].target_points = 8
            deal.hand["E"].target_points = 12

        if test == 2:
            deal.hand["N"].setTargetCardsFromPbn("JT62.AKQ5.5.AQT9")
            deal.hand["S"].setTargetCardsFromPbn("Q543.42.T842.542")
            deal.hand["E"].setTargetCardsFromPbn(".J9873.KJ76.KJ63")

        if test == 3:
            # this has an effect on the other hands
            deal.hand["N"].target_random_distribution = (4,3,3,3)
            deal.hand["S"].target_random_distribution = (4,3,3,3)
            deal.hand["N"].target_points = 9
            deal.hand["S"].target_points = 16


        try:
            deal.generate()
        except DealError as e:
            logger.error(e.msg)
        except Exception as e:
            logger.error(e.msg)
        else:
            try:
                deal.print_ultra_compact()
                #deal.print_compact()
                #deal.print()
                deal.print_table()
                #print(deal.to_pbn())
                print(deal.get_dds_results())
            except DealError as e:
                logger.error(e.msg)


if __name__ == '__main__':
    colorama.init()

    #logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.basicConfig(format='%(message)s', level=logging.INFO)

    parser = argparse.ArgumentParser(prog="PyDeal", description="Batch for PyDeal")

    # options
    parser.add_argument("-n", "--number", type=int, default=1, dest="nbTry",
                  help="number of deals to generate")


    options = parser.parse_args()

    main(options)
