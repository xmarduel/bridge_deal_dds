# coding: utf8

import sys
import os

from typing import Optional
from typing import List
from typing import Set
from typing import Dict
from typing import Any

import copy
import logging
from enum import Enum, unique
import random
from colorama import Fore
from colorama import Style

from jinja2 import Template


sys.path.append("DDS")

# import only once !
import DDS.DDSW as DDSW
DDS = DDSW.DDS()


class DealError(Exception):
    msg = "Failed to generate deal"

    def getMsg(self):
        return self.msg


class DealBadSettingCardError(DealError):
    msg = "Failed to generate deal : inconsistent settings for fixed card"

    def __init__(self, color, card):
        self.color = color
        self.card = card


class DealBadSettingDistributionError(DealError):
    msg = "Failed to generate deal : inconsistent settings for distribution"

    def __init__(self, color):
        self.color = color


class DealBadSettingRandomDistributionError(DealError):
    msg = "Failed to generate deal : inconsistent settings for random distribution"

    def __init__(self):
        pass


class DealBadSettingBasicDistributionError(DealError):
    msg = "Failed to generate deal : inconsistent settings for 4 colors distribution"

    def __init__(self):
        pass


class DealGenerateTargetPointsDistributionError(DealError):
    msg = "Failed to distribute honours"

    def __init__(self, hand_pos):
        self.hand_pos = hand_pos


class DealNoDDS(DealError):
    msg = "No DDS module"

    def __init__(self):
        pass


@unique
class Color(Enum):
    """
    ['♠', '♦', '♥', '♣']
    """

    SPADES = "♠"
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"


@unique
class Card(Enum):
    """ """

    S_2 = (0, 0, Color.SPADES, "2", 13)
    S_3 = (1, 0, Color.SPADES, "3", 12)
    S_4 = (2, 0, Color.SPADES, "4", 11)
    S_5 = (3, 0, Color.SPADES, "5", 10)
    S_6 = (4, 0, Color.SPADES, "6", 9)
    S_7 = (5, 0, Color.SPADES, "7", 8)
    S_8 = (6, 0, Color.SPADES, "8", 7)
    S_9 = (7, 0, Color.SPADES, "9", 5)
    S_T = (8, 0, Color.SPADES, "T", 5)
    S_J = (9, 1, Color.SPADES, "J", 4)
    S_Q = (10, 2, Color.SPADES, "Q", 3)
    S_K = (11, 3, Color.SPADES, "K", 2)
    S_A = (12, 4, Color.SPADES, "A", 1)

    H_2 = (13 + 0, 0, Color.HEARTS, "2", 26)
    H_3 = (13 + 1, 0, Color.HEARTS, "3", 25)
    H_4 = (13 + 2, 0, Color.HEARTS, "4", 24)
    H_5 = (13 + 3, 0, Color.HEARTS, "5", 23)
    H_6 = (13 + 4, 0, Color.HEARTS, "6", 22)
    H_7 = (13 + 5, 0, Color.HEARTS, "7", 21)
    H_8 = (13 + 6, 0, Color.HEARTS, "8", 20)
    H_9 = (13 + 7, 0, Color.HEARTS, "9", 19)
    H_T = (13 + 8, 0, Color.HEARTS, "T", 18)
    H_J = (13 + 9, 1, Color.HEARTS, "J", 17)
    H_Q = (13 + 10, 2, Color.HEARTS, "Q", 16)
    H_K = (13 + 11, 3, Color.HEARTS, "K", 15)
    H_A = (13 + 12, 4, Color.HEARTS, "A", 14)

    D_2 = (2 * 13 + 0, 0, Color.DIAMONDS, "2", 39)
    D_3 = (2 * 13 + 1, 0, Color.DIAMONDS, "3", 38)
    D_4 = (2 * 13 + 2, 0, Color.DIAMONDS, "4", 37)
    D_5 = (2 * 13 + 3, 0, Color.DIAMONDS, "5", 36)
    D_6 = (2 * 13 + 4, 0, Color.DIAMONDS, "6", 35)
    D_7 = (2 * 13 + 5, 0, Color.DIAMONDS, "7", 34)
    D_8 = (2 * 13 + 6, 0, Color.DIAMONDS, "8", 33)
    D_9 = (2 * 13 + 7, 0, Color.DIAMONDS, "9", 32)
    D_T = (2 * 13 + 8, 0, Color.DIAMONDS, "T", 31)
    D_J = (2 * 13 + 9, 1, Color.DIAMONDS, "J", 30)
    D_Q = (2 * 13 + 10, 2, Color.DIAMONDS, "Q", 29)
    D_K = (2 * 13 + 11, 3, Color.DIAMONDS, "K", 28)
    D_A = (2 * 13 + 12, 4, Color.DIAMONDS, "A", 27)

    C_2 = (3 * 13 + 0, 0, Color.CLUBS, "2", 52)
    C_3 = (3 * 13 + 1, 0, Color.CLUBS, "3", 52)
    C_4 = (3 * 13 + 2, 0, Color.CLUBS, "4", 50)
    C_5 = (3 * 13 + 3, 0, Color.CLUBS, "5", 49)
    C_6 = (3 * 13 + 4, 0, Color.CLUBS, "6", 48)
    C_7 = (3 * 13 + 5, 0, Color.CLUBS, "7", 47)
    C_8 = (3 * 13 + 6, 0, Color.CLUBS, "8", 46)
    C_9 = (3 * 13 + 7, 0, Color.CLUBS, "9", 45)
    C_T = (3 * 13 + 8, 0, Color.CLUBS, "T", 44)
    C_J = (3 * 13 + 9, 1, Color.CLUBS, "J", 43)
    C_Q = (3 * 13 + 10, 2, Color.CLUBS, "Q", 42)
    C_K = (3 * 13 + 11, 3, Color.CLUBS, "K", 41)
    C_A = (3 * 13 + 12, 4, Color.CLUBS, "A", 40)

    def id(self) -> int:
        return self.value[0]

    def val(self) -> int:
        return self.value[1]

    def color(self):
        return self.value[2]

    def symbol(self) -> str:
        return self.value[3]

    def order_value(self) -> int:
        return self.value[4]

    def isSPADES(self) -> bool:
        return self.color() == Color.SPADES

    def isHEARTS(self) -> bool:
        return self.color() == Color.HEARTS

    def isDIAMONDS(self) -> bool:
        return self.color() == Color.DIAMONDS

    def isCLUBS(self) -> bool:
        return self.color() == Color.CLUBS

    @classmethod
    def fromSymbolAndColor(self, symbol: str, color: Color) -> "Card":
        for card in Card:
            card_symbol = card.symbol()
            card_color = card.color()

            if card_color != color:
                continue
            if card_symbol != symbol:
                continue

            return card

        # error fallback
        raise

    @classmethod
    def cardsFromPbn(cls, pbn):
        cards_pbn = pbn.split(".")
        cards = {}
        cards[Color.SPADES] = cards_pbn[0]
        cards[Color.HEARTS] = cards_pbn[1]
        cards[Color.DIAMONDS] = cards_pbn[2]
        cards[Color.CLUBS] = cards_pbn[3]
        target_cards = {}
        for color in cards:
            target_cards[color] = []
            for symbol in cards[color]:
                c = Card.fromSymbolAndColor(symbol, color)
                target_cards[color].append(c)
        return target_cards


class Hand:
    """ """

    # -1: random distribution; n>=0 : nb Card in given color fixed value
    default_distribution = {
        Color.SPADES: -1,
        Color.HEARTS: -1,
        Color.DIAMONDS: -1,
        Color.CLUBS: -1,
    }  # type: Dict[Color,int]

    # mandatory cards, empty per default
    default_cards = {
        Color.SPADES: [],
        Color.HEARTS: [],
        Color.DIAMONDS: [],
        Color.CLUBS: [],
    }  # type: Dict[Color,List[Card]]

    # global hand points, not per color points
    default_points = -1  # type: int

    logger = logging.Logger("Deal")
    logger.setLevel(logging.INFO)

    def __init__(self, pos: str):
        """ """
        self.pos = pos
        self.cards = []  # type: List[Card]
        # to fill

        self.target_distribution = copy.deepcopy(self.default_distribution)
        self.target_cards = copy.deepcopy(self.default_cards)
        self.target_points = self.default_points

        self.distribution_type = "FIXED"  # "RANDOM"

    def reset(self):
        self.cards = []  # type: List[Card]

    def __repr__(self) -> str:
        return self.get_compact_repr()

    def to_pbn(self, color: "Color", sep: str) -> str:
        """ """
        res = self.get_formatted_cards(color)

        res = sep.join([c for c in res])

        return res

    @classmethod
    def from_pbn(cls, pos: str, hand_pbn: str) -> "Hand":
        """ """
        hand = Hand(pos)
        cards_pbn = hand_pbn.split(".")

        cards = {}
        cards[Color.SPADES] = cards_pbn[0]
        cards[Color.HEARTS] = cards_pbn[1]
        cards[Color.DIAMONDS] = cards_pbn[2]
        cards[Color.CLUBS] = cards_pbn[3]

        for color in cards:
            for symbol in cards[color]:
                c = Card.fromSymbolAndColor(symbol, color)
                hand.cards.append(c)

        return hand

    def setTargetCardsFromPbn(self, hand_pbn: str):
        """ """
        cards_pbn = hand_pbn.split(".")

        cards = {}
        cards[Color.SPADES] = cards_pbn[0]
        cards[Color.HEARTS] = cards_pbn[1]
        cards[Color.DIAMONDS] = cards_pbn[2]
        cards[Color.CLUBS] = cards_pbn[3]

        for color in cards:
            self.target_cards[color] = []
            for symbol in cards[color]:
                c = Card.fromSymbolAndColor(symbol, color)
                self.target_cards[color].append(c)

    def prio_targeted_points(self):
        """
        returns an integer function of the prio when considering target points
        """
        return self.target_points  # more target points -> higher prio

    def prio_distribution(self):
        """
        returns an integer function of the prio when considering distribution
        """
        if False:
            if self.target_points == -1:
                return 0
            if self.target_distribution == self.default_distribution:
                return 1

            return (
                len(self.target_cards[Color.SPADES])
                + len(self.target_cards[Color.HEARTS])
                + len(self.target_cards[Color.DIAMONDS])
                + len(self.target_cards[Color.CLUBS])
                + 2
            )

        nbS = (
            self.target_distribution[Color.SPADES]
            if self.target_distribution[Color.SPADES] != -1
            else 0
        )
        nbH = (
            self.target_distribution[Color.HEARTS]
            if self.target_distribution[Color.HEARTS] != -1
            else 0
        )
        nbD = (
            self.target_distribution[Color.DIAMONDS]
            if self.target_distribution[Color.DIAMONDS] != -1
            else 0
        )
        nbC = (
            self.target_distribution[Color.CLUBS]
            if self.target_distribution[Color.CLUBS] != -1
            else 0
        )

        prio = nbS + nbH + nbD + nbC

        return prio

    def cards_for_color(self, color: Color):
        cards = [card for card in self.cards if card.color() == color]
        cards = sorted(cards, key=lambda card: card.id(), reverse=True)

        return cards

    def get_formatted_cards(self, color: Color):
        cards = self.cards_for_color(color)
        cards_str = [card.symbol() for card in cards]

        return "".join(k for k in cards_str)

    def get_std_repr(self) -> str:
        """
        multiline repr
        """
        res = "%s  %s pts \n" % (self.pos, self.points())

        SS = self.get_formatted_cards(Color.SPADES)
        HH = self.get_formatted_cards(Color.HEARTS)
        DD = self.get_formatted_cards(Color.DIAMONDS)
        CC = self.get_formatted_cards(Color.CLUBS)

        res += Fore.BLUE + Style.BRIGHT + "    ♠:" + SS + Style.RESET_ALL + "\n"
        res += Fore.RED + Style.BRIGHT + "    ♥:" + HH + Style.RESET_ALL + "\n"
        res += Fore.YELLOW + Style.BRIGHT + "    ♦:" + DD + Style.RESET_ALL + "\n"
        res += Fore.BLUE + Style.BRIGHT + "    ♣:" + CC + Style.RESET_ALL + "\n"

        return res

    def get_pbn_repr(self) -> str:
        """
        "N:.63.AKQ987.A9732 A8654.KQ5.T.QJT6 J973.J98742.3.K4 KQT2.AT.J6542.85"
        """
        SS = self.get_formatted_cards(Color.SPADES)
        HH = self.get_formatted_cards(Color.HEARTS)
        DD = self.get_formatted_cards(Color.DIAMONDS)
        CC = self.get_formatted_cards(Color.CLUBS)

        return ".".join([SS, HH, DD, CC])

    def get_compact_repr(self) -> str:
        """
        one line repr
        """
        SS = self.get_formatted_cards(Color.SPADES)
        HH = self.get_formatted_cards(Color.HEARTS)
        DD = self.get_formatted_cards(Color.DIAMONDS)
        CC = self.get_formatted_cards(Color.CLUBS)

        # ['♠', '♦', '♥', '♣']
        return (
            Fore.BLUE
            + Style.BRIGHT
            + "♠"
            + SS
            + Fore.RED
            + Style.BRIGHT
            + "♥"
            + HH
            + Fore.YELLOW
            + Style.BRIGHT
            + "♦"
            + DD
            + Fore.BLUE
            + Style.BRIGHT
            + "♣"
            + CC
            + Style.RESET_ALL
        )

    def print_in_table(self, other_hand: Optional["Hand"] = None):
        """ """
        SS = self.get_formatted_cards(Color.SPADES)
        HH = self.get_formatted_cards(Color.HEARTS)
        DD = self.get_formatted_cards(Color.DIAMONDS)
        CC = self.get_formatted_cards(Color.CLUBS)

        if other_hand:
            xSS = other_hand.get_formatted_cards(Color.SPADES)
            xHH = other_hand.get_formatted_cards(Color.HEARTS)
            xDD = other_hand.get_formatted_cards(Color.DIAMONDS)
            xCC = other_hand.get_formatted_cards(Color.CLUBS)

        if self.pos == "N":
            print(Fore.BLUE + Style.BRIGHT + 10 * " " + "    ♠:" + SS + Style.RESET_ALL)
            print(Fore.RED + Style.BRIGHT + 10 * " " + "    ♥:" + HH + Style.RESET_ALL)
            print(
                Fore.YELLOW + Style.BRIGHT + 10 * " " + "    ♦:" + DD + Style.RESET_ALL
            )
            print(Fore.BLUE + Style.BRIGHT + 10 * " " + "    ♣:" + CC + Style.RESET_ALL)
            print(" ")

        if self.pos == "W":
            print(
                Fore.BLUE
                + Style.BRIGHT
                + 0 * " "
                + "    ♠:"
                + SS
                + (15 - len(SS)) * " "
                + "    ♠:"
                + xSS
                + Style.RESET_ALL
            )
            print(
                Fore.RED
                + Style.BRIGHT
                + 0 * " "
                + "    ♥:"
                + HH
                + (15 - len(HH)) * " "
                + "    ♥:"
                + xHH
                + Style.RESET_ALL
            )
            print(
                Fore.YELLOW
                + Style.BRIGHT
                + 0 * " "
                + "    ♦:"
                + DD
                + (15 - len(DD)) * " "
                + "    ♦:"
                + xDD
                + Style.RESET_ALL
            )
            print(
                Fore.BLUE
                + Style.BRIGHT
                + 0 * " "
                + "    ♣:"
                + CC
                + (15 - len(CC)) * " "
                + "    ♣:"
                + xCC
                + Style.RESET_ALL
            )
            print(" ")

        if self.pos == "S":
            print(Fore.BLUE + Style.BRIGHT + 10 * " " + "    ♠:" + SS + Style.RESET_ALL)
            print(Fore.RED + Style.BRIGHT + 10 * " " + "    ♥:" + HH + Style.RESET_ALL)
            print(
                Fore.YELLOW + Style.BRIGHT + 10 * " " + "    ♦:" + DD + Style.RESET_ALL
            )
            print(Fore.BLUE + Style.BRIGHT + 10 * " " + "    ♣:" + CC + Style.RESET_ALL)
            print(" ")

    def points(self) -> int:
        """ """
        total = 0

        for card in self.cards:
            total += card.val()

        return total

    def filter_honours_distribution_consistency(self, honours: Set[Card]):
        """
        restrict honours set based on target_distribution of all cards:

        Example: "N" with
        - target cards  -> ♠RD♥A
        - target points -> 15 pts
        - target_distribution[♠] = 5
        - target_distribution[♥] = 5

        so distributing the honours like this:
        ♠RD♥A♦DV♣DV     seemd ok , but infact not!
        the error comes from the fact that the distribution of honours may confict with the
        global distribution

        target cards : ♠RD♥A
        target points: ♠RD♥A♦DV♣DV   15 pts Ok
        ... but the target distribution will fails with demanded 5 cards ♠ and 5 cards ♥

        TODO: Can we restrict the honours choices in order to avoid this ?
        target cards : ♠RD♥A   -> only 3 honours in the others colors (the ones without restriction on the distribution)
        target cards : ♠RD♥A♦D -> only 2 honours in the others colors
        target cards : ♠RD♥A♦DV -> only 1 honour in the others colors
        target cards : ♠RD♥A♦DV♣D -> only 0 honours in the others colors -> choice is in [♠V♥V], not in [♠V♥V♣V]
        """
        # look at colors w/o distribution, get number of their cards
        n = 0
        if self.target_distribution[Color.SPADES] < 0:
            n += len([card for card in self.cards if card.color() == Color.SPADES])
        if self.target_distribution[Color.HEARTS] < 0:
            n += len([card for card in self.cards if card.color() == Color.HEARTS])
        if self.target_distribution[Color.DIAMONDS] < 0:
            n += len([card for card in self.cards if card.color() == Color.DIAMONDS])
        if self.target_distribution[Color.CLUBS] < 0:
            n += len([card for card in self.cards if card.color() == Color.CLUBS])

        xsum = n

        if self.target_distribution[Color.SPADES] >= 0:
            xsum += self.target_distribution[Color.SPADES]
        if self.target_distribution[Color.HEARTS] >= 0:
            xsum += self.target_distribution[Color.HEARTS]
        if self.target_distribution[Color.DIAMONDS] >= 0:
            xsum += self.target_distribution[Color.DIAMONDS]
        if self.target_distribution[Color.CLUBS] >= 0:
            xsum += self.target_distribution[Color.CLUBS]

        filtered_honours = honours

        if xsum == 13:
            # no place for honours of colors where no distribution is imposed -> filter them out
            filtered_honours = honours

            if self.target_distribution[Color.SPADES] < 0:  # filter the SPADES out
                filtered_honours = set(
                    [card for card in filtered_honours if card.color() != Color.SPADES]
                )
            if self.target_distribution[Color.HEARTS] < 0:  # filter the HEARTS out
                filtered_honours = set(
                    [card for card in filtered_honours if card.color() != Color.HEARTS]
                )
            if self.target_distribution[Color.DIAMONDS] < 0:  # filter the DIAMONDS out
                filtered_honours = set(
                    [
                        card
                        for card in filtered_honours
                        if card.color() != Color.DIAMONDS
                    ]
                )
            if self.target_distribution[Color.CLUBS] < 0:  # filter the CLUBS out
                filtered_honours = set(
                    [card for card in filtered_honours if card.color() != Color.CLUBS]
                )

        return filtered_honours

    def generate_handle_target_cards(self, items: Set[Card]) -> Set[Card]:
        """ """
        for color in self.target_cards:
            for card in self.target_cards[color]:
                if card.color() != color:
                    raise DealBadSettingCardError(color, card)
                if card not in items:
                    raise DealBadSettingCardError(color, card)

                self.cards.append(card)
                items = items - set([card])

        return items

    def generate_handle_target_points(self, items: Set[Card]) -> Set[Card]:
        """
        Distribute the honours conformely to the hand target points
        - target points can be given -> do distribute honours
        - no target points -> no honours distribution
        Take care of the colors distribution (do not distribute honours
           in a color leading to too many cards in a color)
        Note that some honours can have been already distributed
        """
        if self.target_points <= 0:
            return items

        self.logger.info('initial hand "%s" before targeting points :', self.pos)
        self.logger.info(self.get_compact_repr())
        self.logger.info(
            "and adding honours to reach targeted points %s", self.target_points
        )

        items_memo = copy.copy(items)
        cards_memo = copy.copy(self.cards)

        nbTrys = 100  # type: int
        cnt = 0  # type: int

        while cnt < nbTrys:

            # the distribution can fails, so we may try 100 times

            if self.points() != self.target_points:
                items_honours = set([card for card in items if card.val() > 0])

                # take into account already distributed cards
                delta_points = self.target_points - self.points()

                # chose 1 honour at a time, hoping not to surpass the target points
                while delta_points > 0:
                    if delta_points < 4:
                        # remove AS
                        items_honours = set(
                            [card for card in items_honours if card.val() < 4]
                        )
                    if delta_points < 3:
                        # remove KONIG
                        items_honours = set(
                            [card for card in items_honours if card.val() < 3]
                        )
                    if delta_points < 2:
                        # remove DAMEN
                        items_honours = set(
                            [card for card in items_honours if card.val() < 2]
                        )
                    if delta_points < 1:
                        # remove BUBEN
                        items_honours = set(
                            [card for card in items_honours if card.val() < 1]
                        )

                    # check "global" distribution condition from this "honours" distribution
                    if self.target_distribution[Color.SPADES] != -1:
                        if self.target_distribution[Color.SPADES] == len(
                            [card for card in self.cards if card.isSPADES()]
                        ):
                            # remove all SPADES honors
                            items_honours = set(
                                [card for card in items_honours if not card.isSPADES()]
                            )
                    if self.target_distribution[Color.HEARTS] != -1:
                        if self.target_distribution[Color.HEARTS] == len(
                            [card for card in self.cards if card.isHEARTS()]
                        ):
                            # remove all HEARTS honors
                            items_honours = set(
                                [card for card in items_honours if not card.isHEARTS()]
                            )
                    if self.target_distribution[Color.DIAMONDS] != -1:
                        if self.target_distribution[Color.DIAMONDS] == len(
                            [card for card in self.cards if card.isDIAMONDS()]
                        ):
                            # remove all DIAMONDS honors
                            items_honours = set(
                                [
                                    card
                                    for card in items_honours
                                    if not card.isDIAMONDS()
                                ]
                            )
                    if self.target_distribution[Color.CLUBS] != -1:
                        if self.target_distribution[Color.CLUBS] == len(
                            [card for card in self.cards if card.isCLUBS()]
                        ):
                            # remove all CLUBS honors
                            items_honours = set(
                                [card for card in items_honours if not card.isCLUBS()]
                            )

                    items_honours = self.filter_honours_distribution_consistency(
                        items_honours
                    )

                    if len(items_honours) == 0:
                        # this is an error
                        break

                    # pick 1 honour
                    honour = random.sample(list(items_honours), 1)[0]

                    items_honours = items_honours - set([honour])
                    self.cards.append(honour)

                    delta_points = self.target_points - self.points()

                    self.logger.info(self.get_compact_repr())  # show trys

                    if delta_points == 0:
                        # Youppi
                        break

            # points final check
            if self.target_points != self.points():
                # failure
                cnt += 1
                # self.logger.debug("failed distributing points -> restart for hand %s" % self.pos)
                # self.logger.debug("SET OF ALL HONOURS : %s " % hh_hand.get_compact_repr())
                # self.logger.debug("REACHED HAND : %s" % self.get_compact_repr()) # show trys
                # hh_hand.cards = list(set(hh_hand.cards) - set(self.cards))
                # self.logger.debug("REMAINING HONOURS : %s " % hh_hand.get_compact_repr())
                self.cards = copy.copy(cards_memo)
                items = copy.copy(items_memo)
            else:
                break

        # loop final check
        if self.points() != self.target_points:
            # failure after 100 trys
            # self.logger.error("FAILURE hand %s  - target points = %d -- points = %d" % (self.pos, self.target_points, self.points()))
            # hh_hand = Hand("?")
            # hh_hand.cards = [card for card in items if card.val() > 0 ]
            # self.logger.error("SET OF ALL HONOURS : %s " % hh_hand.get_compact_repr())
            # self.logger.error("REACHED HAND : %s" % self.get_compact_repr()) # show trys
            # hh_hand.cards = list(set(hh_hand.cards) - set(self.cards))
            # self.logger.error("REMAINING HONOURS : %s " % hh_hand.get_compact_repr())
            # self.cards = copy.copy(cards_memo)
            raise DealGenerateTargetPointsDistributionError(self.pos)

        return items

    def generate(self, items: Set[Card]):
        """ """
        nbAll = 13 - len(
            self.cards
        )  # the already distributed given ones (mandatory + honours for targeted points)

        self.logger.info(
            'end generation for "%s"   #nb cards to distribute = %s', self.pos, nbAll
        )
        self.logger.info(self.get_compact_repr())

        if self.target_distribution != self.default_distribution:

            for color in [Color.SPADES, Color.HEARTS, Color.DIAMONDS, Color.CLUBS]:

                if self.target_distribution[color] != -1:

                    nb = self.target_distribution[color]

                    curr = len([card for card in self.cards if card.color() == color])

                    nb = nb - curr
                    if nb < 0:
                        self.logger.error(
                            "target_distribution = %s but curr = %s  -> get only %s",
                            nb + curr,
                            curr,
                            nb,
                        )
                        raise DealBadSettingDistributionError(color)

                    self.logger.debug(
                        "must distribute %s %s cards (%s already there)",
                        nb,
                        color.value,
                        curr,
                    )
                    nbAll -= nb

                    if nb >= 0:
                        # get all cards of demanded color
                        itemsX = [card for card in items if card.color() == color]
                        if self.target_points > 0:
                            itemsX = [card for card in itemsX if card.val() == 0]

                        self.cards += random.sample(itemsX, nb)
                        # remove all cards of this color for further processing (ie exact number of cards when len != -1  specified)
                        items = items - set(itemsX)

        self.logger.debug(
            'last random distribute for "%s": #nb cards to distribute = %s for remaining %s cards...',
            self.pos,
            nbAll,
            len(items),
        )
        # the rest
        if nbAll > 0:
            if self.target_points == -1:
                self.cards += random.sample(list(items), nbAll)
            else:
                # no honours, points are already processed
                items = set([card for card in items if card.val() == 0])
                self.logger.debug(
                    'last random distribute for "%s": #nb cards to distribute = %s for remaining %s cards... (without honours)',
                    self.pos,
                    nbAll,
                    len(items),
                )
                nn = nbAll
                if nn > len(items):
                    nn = len(items)
                self.cards += random.sample(list(items), nn)
        else:
            pass

    def check_distribution_basic_settings(self):
        """ """
        distribution = {}

        for color in self.target_distribution:
            if self.target_distribution[color] != -1:
                # ignore the not specified color
                distribution[color] = self.target_distribution[color]

        # consistency check
        if len(distribution) == 4:
            # all colors specified: check there is a length of 13 cards specified
            total = 0
            for color in distribution:
                total += distribution[color]

            if total != 13:
                raise DealBadSettingBasicDistributionError()

    def generate_real_distribution(self):
        """
        recalculate distribution if a random distribution is given
        """
        distribution = {}

        for color in self.target_distribution:
            if self.target_distribution[color] != -1:
                # ignore the unspecified colors
                distribution[color] = self.target_distribution[color]

        if self.distribution_type == "RANDOM":

            colors = list(distribution.keys())
            values = list(distribution.values())

            def func(elem):
                return -len(self.target_cards[elem])

            # order the colors with the max target_cards
            colors.sort(key=func)

            for color in colors:
                # pick a value
                nbtrys = 0
                while True:
                    nbtrys += 1
                    nb = random.sample(values, 1)[0]
                    # set the distribution - check against possible imposed cards
                    if len(self.target_cards[color]) <= nb:
                        # set and next color
                        self.target_distribution[color] = nb
                        values.remove(nb)
                        break
                    if nbtrys == 1000:
                        # this is certainly an error
                        raise DealBadSettingRandomDistributionError()

                # TODO what if some target points are defined on the color ??? complicated
                pass

        return


class Deal:
    """ """

    logger = logging.Logger("Deal")

    def __init__(self):
        """ """
        self.name = "default"  # type: str
        self.description = ""  # type: str
        self.difficulty = 1  # type: int

        self.hand = {
            "N": Hand("N"),
            "S": Hand("S"),
            "W": Hand("W"),
            "E": Hand("E"),
        }  # type: Dict[str,Hand]

    def reset(self):
        """
        empty deal
        """
        self.hand["N"].reset()
        self.hand["S"].reset()
        self.hand["W"].reset()
        self.hand["E"].reset()

    def print(self):
        print("--------------------------")
        print(self.hand["N"].get_std_repr())
        print(self.hand["S"].get_std_repr())
        print(self.hand["W"].get_std_repr())
        print(self.hand["E"].get_std_repr())
        print("--------------------------")

    def print_compact(self):
        print(" ")
        print("N:", self.hand["N"].get_compact_repr())
        print("S:", self.hand["S"].get_compact_repr())
        print("W:", self.hand["W"].get_compact_repr())
        print("E:", self.hand["E"].get_compact_repr())

    def print_ultra_compact(self):
        print("N:", self.hand["N"].get_compact_repr(), end=" - ")
        print("S:", self.hand["S"].get_compact_repr(), end=" - ")
        print("W:", self.hand["W"].get_compact_repr(), end=" - ")
        print("E:", self.hand["E"].get_compact_repr())

    def print_table(self):
        print(" ")
        self.hand["N"].print_in_table()
        self.hand["W"].print_in_table(self.hand["E"])
        self.hand["S"].print_in_table()

    def from_pbn(self, pbn: str):
        """
        "N:KQJ65.AQT64..K52 AT32.J53.KDJ72.J .9872.A83.AT7643 9874.K.T9654.Q98"
        """
        next_pos = {"N": "E", "E": "S", "S": "W", "W": "N"}

        pos = pbn[0]

        cards = pbn[2:]
        all_hands = cards.split(" ")

        hand_pbn = {}

        hand_pbn[pos] = all_hands[0]
        pos = next_pos[pos]
        hand_pbn[pos] = all_hands[1]
        pos = next_pos[pos]
        hand_pbn[pos] = all_hands[2]
        pos = next_pos[pos]
        hand_pbn[pos] = all_hands[3]

        for pos in ("N", "E", "S", "W"):
            # self.hand[pos].setTargetCardsFromPbn(hand_pbn[pos])
            self.hand[pos].setTargetCardsFromPbn(hand_pbn[pos])

    def to_pbn(self) -> str:
        """
        "N:.63.AKQ987.A9732 A8654.KQ5.T.QJT6 J973.J98742.3.K4 KQT2.AT.J6542.85"
        "N:KQ873.A9843.AQ9. 64.KQJ.J832.AJ63 AJ92.T72.54.K952 T5.65.KT76.QT874"
        """
        res = [
            "N:" + self.hand["N"].get_pbn_repr(),
            self.hand["E"].get_pbn_repr(),
            self.hand["S"].get_pbn_repr(),
            self.hand["W"].get_pbn_repr(),
        ]
        return " ".join(res)

    def get_dds_results_html(self) -> str:
        """
              North South East  West
        NT     4     4     8     8
         S     3     3    10    10
         H     9     9     4     4
         D     8     8     4     4
         C     3     3     9     9
        """
        # ---hand---------------------------------------
        contracts = {
            DDS.NOTRUMP: {},
            DDS.SPADES: {},
            DDS.HEARTS: {},
            DDS.DIAMONDS: {},
            DDS.CLUBS: {},
        }  # type: Dict[int, Dict[Any,Any]]

        pbn = self.to_pbn()

        print("pbn: ", pbn)

        r = DDS.calc_dd_table(pbn)

        if r:
            for i in range(0, 5):
                for j in range(0, 4):
                    if r.resTable[i][j] < 7:
                        contracts[i][j] = "-"
                    else:
                        contracts[i][j] = str(r.resTable[i][j] - 6)
        else:
            for i in range(0, 5):
                for j in range(0, 4):
                    contracts[i][j] = "e"

        template = Template(
            """
<html>
<head>
    <title></title>
    <style>
body {
  background-color: powderblue;
}
table {
  font-family: arial, sans-serif;
  font-size: 15px;
  border-collapse: separate;
}
td, th {
  text-align: center;
  padding: 1px;
}print_deal_html
</style>
</head>

<body>
<div>

<table width="100%">
  <tr>    <th></th>                               <th>North</th>                            <th>South</th>                            <th>East</th>	                        <th>West</th>  </tr>
  <tr>    <td>NT</td>                             <td>{{c[dds.NOTRUMP][dds.NORTH]}}</td>    <td>{{c[dds.NOTRUMP][dds.SOUTH]}}</td>    <td>{{c[dds.NOTRUMP][dds.EAST]}}</td>	<td>{{c[dds.NOTRUMP][dds.WEST]}}</td>  </tr>
  <tr>    <td style="color:black;">&spades;</td>  <td>{{c[dds.SPADES][dds.NORTH]}}</td>     <td>{{c[dds.SPADES][dds.SOUTH]}}</td>     <td>{{c[dds.SPADES][dds.EAST]}}</td>	<td>{{c[dds.SPADES][dds.WEST]}}</td>   </tr>
  <tr>    <td style="color:red;">&hearts;</td>    <td>{{c[dds.HEARTS][dds.NORTH]}}</td>     <td>{{c[dds.HEARTS][dds.SOUTH]}}</td>     <td>{{c[dds.HEARTS][dds.EAST]}}</td>	<td>{{c[dds.HEARTS][dds.WEST]}}</td>   </tr>
  <tr>    <td style="color:brown;">&diams;</td>   <td>{{c[dds.DIAMONDS][dds.NORTH]}}</td>   <td>{{c[dds.DIAMONDS][dds.SOUTH]}}</td>   <td>{{c[dds.DIAMONDS][dds.EAST]}}</td>	<td>{{c[dds.DIAMONDS][dds.WEST]}}</td> </tr>
  <tr>    <td style="color:green;">&clubs;</td>   <td>{{c[dds.CLUBS][dds.NORTH]}}</td>      <td>{{c[dds.CLUBS][dds.SOUTH]}}</td>      <td>{{c[dds.CLUBS][dds.EAST]}}</td>	<td>{{c[dds.CLUBS][dds.WEST]}}</td>    </tr>
</table> 

</div>
</body>
</html>
"""
        )
        return template.render(c=contracts, dds=DDS)

    def get_dds_results(self) -> str:
        """
              North South East  West
        NT     4     4     8     8
         S     3     3    10    10
         H     9     9     4     4
         D     8     8     4     4
         C     3     3     9     9
        """
        try:
            # TODO switch win32/others
            import DDS.DDSW as DDSW

            DDS = DDSW.DDS()
        except Exception as e:
            raise DealNoDDS

        # TODO switch win32/others
        import DDS.DDSW as DDSW

        DDS = DDSW.DDS()

        pbn = self.to_pbn()
        r = DDS.calc_dd_table(pbn)

        contracts = {
            DDS.NOTRUMP: {},
            DDS.SPADES: {},
            DDS.HEARTS: {},
            DDS.DIAMONDS: {},
            DDS.CLUBS: {},
        }  # type: Dict[int, Dict[Any,Any]]

        for i in range(0, 5):
            for j in range(0, 4):
                if r.resTable[i][j] < 7:
                    contracts[i][j] = "-"
                else:
                    contracts[i][j] = str(r.resTable[i][j] - 6)

        template = Template(
            """
             North South East  West 
       NT     {{c[dds.NOTRUMP][dds.NORTH]}}     {{c[dds.NOTRUMP][dds.SOUTH]}}     {{c[dds.NOTRUMP][dds.EAST]}}     {{c[dds.NOTRUMP][dds.WEST]}}
        ♠     {{c[dds.SPADES][dds.NORTH]}}     {{c[dds.SPADES][dds.SOUTH]}}     {{c[dds.SPADES][dds.EAST]}}     {{c[dds.SPADES][dds.WEST]}}
        ♥     {{c[dds.HEARTS][dds.NORTH]}}     {{c[dds.HEARTS][dds.SOUTH]}}     {{c[dds.HEARTS][dds.EAST]}}     {{c[dds.HEARTS][dds.WEST]}}
        ♦     {{c[dds.DIAMONDS][dds.NORTH]}}     {{c[dds.DIAMONDS][dds.SOUTH]}}     {{c[dds.DIAMONDS][dds.EAST]}}     {{c[dds.DIAMONDS][dds.WEST]}}
        ♣     {{c[dds.CLUBS][dds.NORTH]}}     {{c[dds.CLUBS][dds.SOUTH]}}     {{c[dds.CLUBS][dds.EAST]}}     {{c[dds.CLUBS][dds.WEST]}}
        """
        )
        return template.render(c=contracts, dds=DDS)

    def get_deal_html(self) -> str:
        """ """
        template = Template(
            """
    <html>

    <head>
    <style>
    body {
      background-color: lightgreen;
    }
    table {
      background-color: lightgreen;
      border: 1px solid black;
      font-family: "Times New Roman";
      font-size: large;
      font-weight: bold;
      table-layout:fixed;
    }
    table.middle {
      border: 0px solid black;
    }
    table.small {
      border: 1px solid black;
      width: 85px;
      height:85px;
    }
    td {
      padding: 3px;
    }
    td.small {
      font-family: "Times New Roman";
      font-size: small;
    }
    </style>
    </head>
    
    <body>
    
    <table align='center' frame='border' cellpadding='10' width='100%'>
    <!-- row 1 -->
    <tr>
      <!-- (1,1): empty -->
      <td> </td>
      <!-- (1,2): North hand -->
      <td colspan='2' >
        <font style='color:black; font-weight:bold'>&spades; {{deal.hand["N"].to_pbn(Color.SPADES, " ")}} </font> <br/>
        <font style='color:red;   font-weight:bold'>&hearts; {{deal.hand["N"].to_pbn(Color.HEARTS, " ")}} </font> <br/>
        <font style='color:brown; font-weight:bold'>&diams;  {{deal.hand["N"].to_pbn(Color.DIAMONDS, " ")}} </font> <br/>
        <font style='color:green; font-weight:bold'>&clubs;  {{deal.hand["N"].to_pbn(Color.CLUBS, " ")}} </font>
      </td>
    </tr>
    <!-- row 2 -->
    <tr>
      <!-- (2,1): west hand -->
      <td>
        <font style='color:black; font-weight:bold'>&spades; {{deal.hand["W"].to_pbn(Color.SPADES, " ")}} </font> <br/>
        <font style='color:red;   font-weight:bold'>&hearts; {{deal.hand["W"].to_pbn(Color.HEARTS, " ")}} </font> <br/>
        <font style='color:brown; font-weight:bold'>&diams;  {{deal.hand["W"].to_pbn(Color.DIAMONDS, " ")}} </font> <br/>
        <font style='color:green; font-weight:bold'>&clubs;  {{deal.hand["W"].to_pbn(Color.CLUBS, " ")}} </font>
      </td>
      <!-- (2,2) central cube -->
      <td colspan='2'> 
        <table class="middle">
          <tr>
            <td>
              <table class='small'>
                <tr>
                  <td class='small' colspan='3' align='center'> N </td>
                </tr>
                <tr>
                  <td class='small' align='left'> W </td>
                  <td></td>
                  <td class='small' align='right'> E </td>
                </tr>
                <tr>
                  <td class='small' colspan='3' align='center'> S </td>
                </tr>
              </table>
            </td>
            <!-- space -->
            <td width="25px"> </td>
            <!-- (2,3) east hand -->
            <td>
              <font style='color:black; font-weight:bold'>&spades; {{deal.hand["E"].to_pbn(Color.SPADES, " ")}} </font> <br/>
              <font style='color:red;   font-weight:bold'>&hearts; {{deal.hand["E"].to_pbn(Color.HEARTS, " ")}} </font> <br/>
              <font style='color:brown; font-weight:bold'>&diams;  {{deal.hand["E"].to_pbn(Color.DIAMONDS, " ")}} </font> <br/>
              <font style='color:green; font-weight:bold'>&clubs;  {{deal.hand["E"].to_pbn(Color.CLUBS, " ")}} </font>
            </td>
          </tr>
        </table>
      </td>
    </tr>
    <!-- row 3 -->
    <tr>
      <!-- (3,1): empty -->
      <td> </td>
      <!-- (3,2): south hand -->
      <td colspan='2'>
        <font style='color:black; font-weight:bold'>&spades; {{deal.hand["S"].to_pbn(Color.SPADES, " ")}} </font> <br/>
        <font style='color:red;   font-weight:bold'>&hearts; {{deal.hand["S"].to_pbn(Color.HEARTS, " ")}} </font> <br/>
        <font style='color:brown; font-weight:bold'>&diams;  {{deal.hand["S"].to_pbn(Color.DIAMONDS, " ")}} </font> <br/>
        <font style='color:green; font-weight:bold'>&clubs;  {{deal.hand["S"].to_pbn(Color.CLUBS, " ")}} </font>
      </td>
    </tr>
    </table>
    
    </body>
    
    </html>
        """
        )
        return template.render(deal=self, Color=Color)

    def generate(self) -> bool:
        """ """
        try:
            list_items = []

            for card in Card:
                list_items.append(card)

            items = set(list_items)

            # first for all hands the mandatory cards
            self.hand["N"].generate_handle_target_cards(items)
            items = items - set(self.hand["N"].cards)
            self.hand["S"].generate_handle_target_cards(items)
            items = items - set(self.hand["S"].cards)
            self.hand["E"].generate_handle_target_cards(items)
            items = items - set(self.hand["E"].cards)
            self.hand["W"].generate_handle_target_cards(items)
            items = items - set(self.hand["W"].cards)

            # then for all hands the imposed points -> distribute honours

            hands = [self.hand["N"], self.hand["S"], self.hand["E"], self.hand["W"]]

            for hand in hands:
                hand.generate_handle_target_points(items)
                items = items - set(hand.cards)

            # the rest : distribution and general
            # process the hand in special order:
            # - first the ones with conditions
            # - then the others

            for hand in hands:
                hand.check_distribution_basic_settings()

            for hand in hands:
                hand.generate_real_distribution()

            hands = [self.hand["N"], self.hand["S"], self.hand["E"], self.hand["W"]]
            hands = sorted(hands, key=self.hand_prio_distribution, reverse=True)

            for hand in hands:
                hand.generate(items)

                items = items - set(hand.cards)

                if len(hand.cards) < 13:
                    self.logger.error(
                        "Failed to distribute cards for hand %s" % hand.pos
                    )

            if len(items) > 0:
                self.logger.error("Failed to distribute all cards...")
                self.logger.error(items)
                return False

        except DealBadSettingCardError as e:
            self.logger.error(DealBadSettingCardError.msg)
            self.logger.error(e.color)
            self.logger.error(e.card)
            raise
        except DealGenerateTargetPointsDistributionError as e:
            self.logger.error(DealGenerateTargetPointsDistributionError.msg)
            self.logger.error(e.hand_pos)
            raise
        except Exception as msg:
            self.logger.error(msg)
            self.logger.error(self.hand["N"].get_compact_repr())
            self.logger.error(self.hand["S"].get_compact_repr())
            self.logger.error(self.hand["W"].get_compact_repr())
            self.logger.error(self.hand["E"].get_compact_repr())
            raise

        # sort cards
        self.hand["N"].cards = sorted(
            self.hand["N"].cards, key=lambda card: card.id(), reverse=True
        )
        self.hand["S"].cards = sorted(
            self.hand["S"].cards, key=lambda card: card.id(), reverse=True
        )
        self.hand["W"].cards = sorted(
            self.hand["W"].cards, key=lambda card: card.id(), reverse=True
        )
        self.hand["E"].cards = sorted(
            self.hand["E"].cards, key=lambda card: card.id(), reverse=True
        )

        return True

    def hand_prio_distribution(self, hand: Hand):
        return hand.prio_distribution()

    def hand_prio_targeted_points(self, hand: Hand):
        return hand.prio_targeted_points()
