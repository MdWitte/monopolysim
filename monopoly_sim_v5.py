# -*- coding: utf-8 -*-
"""
21-03-2021
Ik heb het idee opgevat om Monopoly te gaan simuleren. Het doel is om te weten 
te komen wat de optimale straat is om te kopen, afhankelijk van het aantal 
spelers. Ik heb alleen de worpen, gevangenis en kans/algemeen fonds kaarten 
gesimuleerd, niet het aan- en verkopen van straten en huizen.

"""

# =============================================================================
# Import packages
# =============================================================================
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from random import randint
import time
startingTime = time.time()
# random.seed(123)  # optioneel, vooral voor debugging



# =============================================================================
# Define classes & functions
# =============================================================================
class player:
    def __init__(self, name):
        self.name = name         # gebruik variabele user_name, geen string, want dan overwritten.
        self.pos = 0             # positie op het bord
        self.money = 1500        # startgeld
        self.properties = []     # lijst met vastgoed in bezit
        self.mortgages = []      # lijst met vastgoed belast met hypotheek
        self.in_jail = False     # boolean that indicates incarceration
        self.free_from_jail = 0  # is het aantal gratis-uit-gevangenis kaarten
        self.num_turns_jail = 0  # no. of turns player has been in jail (max 3)


def shuffle_chance_cards():
    chance_cards = [""]
    deck_chance = random.shuffle(chance_cards)
    return deck_chance


def shuffle_fonds_cards():
    fonds_cards = [""]
    deck_fonds = random.shuffle(fonds_cards)
    return deck_fonds


def player_turn(current_player, board):
    double_roll = True
    num_double_roll = 0
    while double_roll:  # play until no more double rolls are rolled
        roll1 = randint(1,6)
        roll2 = randint(1,6)
        
        # Check for double roll
        if show_outputs: print(current_player.name + ' rolled a %i and a %i, so %i' % (roll1, roll2, roll1+roll2) )
        if roll1 == roll2:  
            num_double_roll += 1  # noteer dubbel-worp
            if current_player.in_jail: 
                current_player.in_jail = False
                current_player.num_turns_jail = 1  # reset this number
                double_roll = False  
                # dit wordt niet genoemd in de NL spelregels, maar wel hier: https://monopoly.fandom.com/wiki/Jail
                # Er staat: "even if doubles are rolled, the player does NOT take another turn.
                if show_outputs: print('%s is now out of jail.' % current_player.name)
        else:
            double_roll = False
            if current_player.in_jail:
                current_player.num_turns_jail += 1
                if current_player.num_turns_jail == 3: 
                    if show_outputs: print('%s now pays €50 and continues on the board.' % current_player.name)
                    current_player.money -= 50 
                    current_player.in_jail = False  # get out of jail, DONT end turn!
                else:     
                    if show_outputs: print('%s did not roll double, so turn is over.' % current_player.name)
                    if show_outputs: print('Status: %s in jail is %s.' % (current_player.name, current_player.in_jail))
                    break  # stop because player is in jail
        
        # Check number of double rolls, else just walk the board
        if num_double_roll == 3:
            current_player.pos = 10  # you go to jail!
            current_player.in_jail = True
            if show_outputs: print('%s is now in jail.' % current_player.name)
            break  # stop turn
        else:
            current_player.pos += roll1 + roll2  # set new position
        
        # Play rest of turn, special cases only
        if current_player.pos == 30: 
            board.loc[current_player.pos, 'count'] += 1  # otherwise 'go to jail' is never counted
            current_player.pos = 10  # you go to jail!
            current_player.in_jail = True
            if show_outputs: print('%s is now in jail!' % current_player.name)
            break  # end turn, do NOT count position 10 in board counter
        # elif current_player.pos in [7, 22, 36]:
        #     current_player.pos = pick_chance_card(current_player.pos)    
        # elif current_player.pos in [4, 17, 33]:
        #     current_player.pos = pick_algemeen_fonds(current_player.pos)
        elif current_player.pos > 39:
            current_player.pos -= 40
            current_player.money += 200  # get €200 if you pass 'Start'
            
        # Also within while loop, increase count of 'vakje' occurences
        board.loc[current_player.pos, 'count'] += 1  
    return  # function returns nothing; only player position is altered
    
    
def pick_chance_card(position):
        
    return position


def pick_algemeen_fonds(position):
    
    return position
    


# =============================================================================
# Make the playing board
# =============================================================================
new_board = pd.DataFrame.from_dict({
    0: ["Start",                        0, "navajowhite"],
    1: ["Dorpsstraat, Ons Dorp",        0, "saddlebrown"],
    2: ["Algemeen fonds 1",             0, "paleturquoise"],
    3: ["Brink, Ons Dorp",              0, "saddlebrown"],
    4: ["Inkomstenbelasting",           0, "navajowhite"],
    5: ["Station Zuid",                 0, "navajowhite"],
    6: ["Steenstraat, Arnhem",          0, "deepskyblue"],
    7: ["Kans 1",                       0, "salmon"],
    8: ["Ketelstraat, Arnhem",          0, "deepskyblue"],
    9: ["Velperplein, Arnhem",          0, "deepskyblue"],
    10: ["Gevangenis / slechts op bezoek", 0, "navajowhite"],
    11: ["Barteljorisstraat, Haarlem",  0, "deeppink"],
    12: ["Elektriciteitsbedrijf",       0, "lime"],
    13: ["Zijlweg, Haarlem",            0, "deeppink"],
    14: ["Houtstraat, Haarlem",         0, "deeppink"],
    15: ["Station West",                0, "navajowhite"],
    16: ["Neude, Utrecht",              0, "tab:orange"],
    17: ["Algemeen fonds 2",            0, "paleturquoise"],
    18: ["Biltstraat, Utrecht",         0, "tab:orange"],
    19: ["Vreeburg, Utrecht",           0, "tab:orange"],
    20: ["Vrij parkeren",               0, "navajowhite"],
    21: ["A Kerkhof, Groningen",        0, "tab:red"],
    22: ["Kans 2",                      0, "salmon"],
    23: ["Grote Markt, Groningen",      0, "tab:red"], 
    24: ["Heerestraat, Groningen",      0, "tab:red"], 
    25: ["Station Noord",               0, "navajowhite"],
    26: ["Spui, \'s-Gravenhage",        0, "yellow"],
    27: ["Plein, \'s-Gravenhage",       0, "yellow"],
    28: ["Waterleiding",                0, "lime"],
    29: ["Lange Poten, \'s-Gravenhage", 0, "yellow"], 
    30: ["Naar de gevangenis",          0, "mediumspringgreen"],
    31: ["Hofplein, Rotterdam",         0, "green"],
    32: ["Blaak, Rotterdam",            0, "green"],
    33: ["Algemeen fonds 3",            0, "paleturquoise"],
    34: ["Coolsingel, Rotterdam",       0, "green"],
    35: ["Station Oost",                0, "navajowhite"],
    36: ["Kans 3",                      0, "salmon"],
    37: ["Leidsestraat, Amsterdam",     0, "darkblue"],
    38: ["Extra belasting",             0, "navajowhite"],
    39: ["Kalverstraat, Amsterdam",     0, "darkblue"],
}, orient='index', columns=["vakje", "count", "color"])



# =============================================================================
# Set the game up
# =============================================================================
# Settings
play_num = 2  # set to 0 if wanting to choose live
# while (play_num < 1 or play_num > 6):
#     play_num = int(input("How many players do you want? Type a number (2, 3, 4, 5, 6): "))
num_games = 10
all_games = pd.DataFrame(new_board.vakje, index=new_board.vakje, columns=range(num_games))
all_games['color'] = new_board.color.values
show_outputs = False  # toggle for displaying each turn's rolls and positions

# Shuffle cards and create players (names are adjustable!)
# deck_chance, deck_fonds = shuffle_cards()  # shuffle the Chance and General Fund
p1 = player("Speler 1")
p2 = player("Speler 2")
if play_num >= 3: 
    p3 = player("Speler 3")
    if play_num >= 4:
        p4 = player("Speler 4")
        if play_num >= 5:
            p5 = player("Speler 5")
            if play_num == 6: 
                p6 = player("Speler 6")



# =============================================================================
# Play the game!
# =============================================================================
# No. of turns that will be played: I think 100 turns (per player) for a full game
for game in range(num_games):
    board = new_board.copy()  # reset the couter of the vakjes occurred
    for turns in range(100):
        player_turn(p1, board)
        player_turn(p2, board)
        if play_num >= 3: 
            player_turn(p3, board)
            if play_num >= 4:
                player_turn(p4, board)
                if play_num >= 5:
                    player_turn(p5, board)
                    if play_num == 6: 
                        player_turn(p6, board)
        if show_outputs: 
            print("New position for player 1 and player 2: %i & %i" %(p1.pos, p2.pos))
            print()                
    all_games[game] = board['count'].values



# =============================================================================
# Plot the results
# =============================================================================

# Print settings for user to see
print("Number of players: %i \nNumber of simulated games: %i" % (play_num, num_games))

# ik wil nog een plot erboven met de ongesorteerde vakjes, alsof je over het bord
# loopt van boven naar beneden.

# Set up
all_games['average'] = all_games.mean(1)
# misschien is min, max ook interessant! Voor een idee van de spreiding van je simulatie! Kan met een soort 
# boxplot aan het einde van de horizontale bar? Heb dat ergens online gezien.
max_times = int(np.ceil(all_games.average.max()))
all_games = all_games.sort_values('average', ascending=True)  # sort the game results
title_font = {'font':'Calibri', 'weight':'bold', 'size':16}
axes_font = {'font':'Calibri', 'weight':'bold', 'size':14}

# Construct figure
plt.figure(figsize=(7,10))
plt.barh(all_games.index, all_games['average'], color=all_games.color, zorder=3)
plt.title("Monopoly Frequency Plot for "+str(play_num)+" players", fontdict = title_font)
plt.xlabel("Aantal keer op vakje gekomen, gem. over "+str(num_games)+" potjes",fontdict=axes_font)
plt.ylabel("Vakjes/straten", fontdict = axes_font)
plt.xticks(np.linspace(0, max_times, max_times*2+1))  # round up the average, then +1
plt.grid(which='both', axis='x', zorder=0)  # zorder 0 and 3 (above) necessary to put grid lines below graph


print('Elapsed time (seconds): ', time.time() - startingTime)

