import dds

# DDS hands examples
pbn = "N:QJ6.K652.J85.T98 873.J97.AT764.Q4 K5.T83.KQ9.A7652 AT942.AQ4.32.KJ3"
pbn = "E:QJT5432.T.6.QJ82 .J97543.K7532.94 87.A62.QJT4.AT75 AK96.KQ8.A98.K63"
pbn = "N:73.QJT.AQ54.T752 QT6.876.KJ9.AQ84 5.A95432.7632.K6 AKJ9842.K.T8.J93"

# XM hand
pbn = "N:KQ964.AK763.J6.Q AJ8.J5.Q92.KJ964 7.T42.AT84.AT875 T532.Q98.K753.32"

dds.show_deal(pbn)
result = dds.calc_dd_table(pbn)
dds.show_results(result)

color_names = {
   dds.SPADES   : "SPADES",   # 0
   dds.HEARTS   : "HEARTS",   # 1
   dds.DIAMONDS : "DIAMONDS", # 2
   dds.CLUBS    : "CLUBS",    # 3
   dds.NOTRUMP  : "NOTRUMP",  # 4
}

player_names = {
   dds.NORTH : "NORTH",  # 0
   dds.EAST  : "EAST",   # 1
   dds.SOUTH : "SOUTH",  # 2
   dds.WEST  : "WEST",   # 3
}

#for color in (dds.NOTRUMP, dds.SPADES, dds.HEARTS, dds.DIAMONDS, dds.CLUBS):
#    print("%-10s" % color_names[color], end="  ")
#    for player in (dds.NORTH, dds.SOUTH, dds.EAST, dds.WEST):
#        print(player_names[player], ":", result.data(color, player), end="  ")
#    print()

trump           = dds.HEARTS
first           = dds.WEST
first_card_suit = dds.DIAMONDS
first_card_rank = 13 # 5
target          = -1   # number of tricks to be won by the side to play
solutions       = 3    # controls how many solutions should be returned
mode            = 0    # control the search behaviour

print("\nsolve_board:")
print("\t trump : ", color_names[trump])
print("\t first : ", player_names[first])
print("\t first_card : ", color_names[first_card_suit], first_card_rank)

# 1st call, East leads:  	SolveBoard(deal, -1, 1, 1, &fut, 0), deal.first=1
# 2nd call, South leads:  	SolveBoard(deal, -1, 1, 2, &fut, 0), deal.first=2
# 3rd call, West leads:  	SolveBoard(deal, -1, 1, 2, &fut, 0), deal.first=3
# 4th call, North leads:  	SolveBoard(deal, -1, 1, 2, &fut, 0), deal.first=0

dds.solve_board(pbn, trump, first, first_card_suit, first_card_rank, target, solutions, mode)