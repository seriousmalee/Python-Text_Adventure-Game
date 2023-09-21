import cmd
import textwrap
import sys
import os
import time
import random

screen_width = 100

### Player Setup ###
class Player():
    def __init__(self):
        self.name = ''
        self.job = ''
        self.hp = 0
        self.mp = 0
        self.status_effects = []
        self.location = 'start'
        self.game_over = False
myPlayer = Player()

### Title Screen ###
def title_screen_selection():
    option = input(" -> ")
    if option.lower() == ("play"):
        setup_game()
    elif option.lower() == ("help"):
        help_menu()
    elif option.lower() == ("quit"):
        sys.exit()
    while option.lower() not in ['play', 'help', 'quit']:
        print("Please enter a valid command. ")
        option = input(" -> ")
        if option.lower() == ("play"):
            setup_game()
        elif option.lower() == ("help"):
            help_menu()
        elif option.lower() == ("quit"):
            sys.exit()

def title_screen():
    os.system('cls')
    print('----------------------------')
    print("# Welcome to the Text RPG! #")
    print('----------------------------')
    print('         -Play-             ')
    print('         -Help-             ')
    print('         -Quit-             ')
    print(' Copyright 2019 Isaacgeddon ')
    title_screen_selection()

def help_menu():
    print('----------------------------')
    print("#        Help Menu         #")
    print("- Use up, down, left, right to move")
    print("- Type in your commands to excute them")
    print("- Use 'look' to inspect something -")
    print("'-Good luck and have fun! -")
    title_screen_selection()

### MAP ###


"""
a1 a2... #player starts at b2
---------
| | | | | a4
---------
| | | | | b4
---------
| | | | |
---------
| | | | |
---------

"""

ZONE_NAME = ' '
DESCRIPTION = 'description'
EXAMINATION = 'examine'
SOLVED = False
UP = 'up', 'north'
DOWN = 'down', 'south'
LEFT = 'left', 'west'
RIGHT = 'right', 'east'


solved_places = {'a1': False, 'a2': False, 'a3': False, 'a4': False,
                 'b1': False, 'b2': False, 'b3': False, 'b4': False,
                 'c1': False, 'c2': False, 'c3': False, 'c4': False,
                 'd1': False, 'd2': False, 'd3': False, 'd4': False,
                         }
zone_map ={
    'a1': {
    ZONE_NAME: "Dragondia Market ",
    DESCRIPTION: '',
    EXAMINATION: '',
    SOLVED: False,
    UP:'Bonk! You cannot go that way!',
    DOWN:'b1',
    LEFT: 'Bonk! You cannot go that way!',
    RIGHT: 'a2',
        },
    'a2': {
    ZONE_NAME: "Dragondia Town Enterance",
    DESCRIPTION: 'description',
    EXAMINATION: 'examine',
    SOLVED: False,
    UP: 'Bonk! You cannot go that way!',
    DOWN: 'b2',
    LEFT: 'a1',
    RIGHT: 'a3',
        },
    'a3': {
    ZONE_NAME: "Dragondia Square",
    DESCRIPTION: 'description',
    EXAMINATION: 'examine',
    SOLVED: False,
    UP: 'Bonk! You cannot go that way!',
    DOWN: 'b3',
    LEFT: 'a2',
    RIGHT: 'a4',
        },
    'a4': {
    ZONE_NAME: "Dragondia Hall",
    DESCRIPTION: 'description',
    EXAMINATION: 'examine',
    SOLVED: False,
    UP: 'Bonk! You cannot go that way!',
    DOWN: 'b4',
    LEFT: 'a3',
    RIGHT: 'Bonk! You cannot go that way!',
        },
    'b1': {
    ZONE_NAME: " ",
    DESCRIPTION: 'description',
    EXAMINATION: 'examine',
    SOLVED: False,
    UP: 'a1',
    DOWN: 'c1',
    LEFT: 'Bonk! You cannot go that way!',
    RIGHT: 'b2',
        },
    'b2': {
    ZONE_NAME: "Home",
    DESCRIPTION: 'This is your home!',
    EXAMINATION: 'Your home looks the same - nothing has changed.',
    SOLVED: False,
    UP: 'a2',
    DOWN: 'c2',
    LEFT: 'b1',
    RIGHT: 'b3'
        },
    'b3': {
    ZONE_NAME: " ",
    DESCRIPTION: 'description',
    EXAMINATION: 'examine',
    SOLVED: False,
    UP: 'a3',
    DOWN: 'c3',
    LEFT: 'b2',
    RIGHT: 'b4'
        },
    'b4': {
    ZONE_NAME: " ",
    DESCRIPTION: 'description',
    EXAMINATION: 'examine',
    SOLVED: False,
    UP: 'a4',
    DOWN: 'c4',
    LEFT: 'b3',
    RIGHT: 'Bonk! You cannot go that way!'
        },
    'c1': {
    ZONE_NAME: " ",
    DESCRIPTION: 'description',
    EXAMINATION: 'examine',
    SOLVED: False,
    UP: 'b1',
    DOWN: 'd1',
    LEFT: 'Bonk! You cannot go that way!',
    RIGHT: 'c2'
        },
    'c2': {
    ZONE_NAME: " ",
    DESCRIPTION: 'description',
    EXAMINATION: 'examine',
    SOLVED: False,
    UP: 'b2',
    DOWN: 'd2',
    LEFT: 'c1',
    RIGHT: 'c3'
        },
    'c3': {
    ZONE_NAME: " ",
    DESCRIPTION: 'description',
    EXAMINATION: 'examine',
    SOLVED: False,
    UP: 'b3',
    DOWN: 'd3',
    LEFT: 'c2',
    RIGHT: 'c4'
        },
    'c4': {
    ZONE_NAME: " ",
    DESCRIPTION: 'description',
    EXAMINATION: 'examine',
    SOLVED: False,
    UP: 'b4',
    DOWN: 'd4',
    LEFT: 'c3',
    RIGHT: 'Bonk! You cannot go that way!'
        },
    'd1': {
    ZONE_NAME: " ",
    DESCRIPTION: 'description',
    EXAMINATION: 'examine',
    SOLVED: False,
    UP: 'c1',
    DOWN: 'Bonk! You cannot go that way!',
    LEFT: 'Bonk! You cannot go that way!',
    RIGHT: 'd2'
        },
    'd2': {
    ZONE_NAME: " ",
    DESCRIPTION: 'description',
    EXAMINATION: 'examine',
    SOLVED: False,
    UP: 'c2',
    DOWN: 'Bonk! You cannot go that way!',
    LEFT: 'd1',
    RIGHT: 'd3',
        },
    'd3': {
    ZONE_NAME: " ",
    DESCRIPTION: 'description',
    EXAMINATION: 'examine',
    SOLVED: False,
    UP: 'c3',
    DOWN: 'Bonk! You cannot go that way!',
    LEFT: 'd2',
    RIGHT: 'd4'
        },
    'd4': {
    ZONE_NAME: " ",
    DESCRIPTION: 'description',
    EXAMINATION: 'examine',
    SOLVED: False,
    UP: 'c4',
    DOWN: 'Bonk! You cannot go that way!',
    LEFT: 'd3',
    RIGHT: 'Bonk! You cannot go that way!'
        }


    }


### GAME INTERACTIVITY ###
def print_location():
    print('\n' + ('#' * (4 + len(myPlayer.location))))
    print('# ' + myPlayer.location.upper() + '#')
    print('# ' + zone_map[myPlayer.position][DESCRIPTION] + ' #')
    print('\n' + ('#' * (4 + len(myPlayer.location))))

def prompt():
    print("\n" + "=======================")
    print("What would you like to do?")
    action = input(" -> ")
    acceptable_actions = ['move', 'go', 'travel', 'walk', 'quit', 'examine', 'inspect', 'interact', 'look']
    while action.lower() not in acceptable_actions:
        print("Unknown action, try again.\n")
        action = input(" -> ")
    if action.lower() == 'quit':
        sys.exit
    elif action.lower() == ['move', 'go', 'travel', 'walk']:
        player_move(action.lower())
    elif action.lower() == ['examine', 'inspect', 'interact', 'look']:
        player_examine(action.lower())

def player_move(myAction):
    ask = "where would you like to move to?\n"
    dest = input(ask)
    if dest in ['up', 'north']:
        destination = zone_map[myPlayer.location][UP]
        movement_handler(destination)
    elif dest in ['down', 'south']:
        destination = zone_map[myPlayer.location][DOWN]
        movement_handler(destination)
    elif dest in ['left', 'west']:
        destination = zone_map[myPlayer.location][LEFT]
        movement_handler(destination)
    elif dest in ['right', 'east']:
        destination = zone_map[myPlayer.location][RIGHT]
        movement_handler(destination)

def movement_handler(destination):
    print("\n" + "You have moved to the" + destination + ".")
    myPlayer.location = destination
    print_location()

def player_examine(action):
    if zone_map[myPlayer.location][SOLVED]:
        print("You have already exhausted this zone.")
    else:
        print("You can trigger puzzle here")

### GAME FUNCTIONALITY###
def main_game_loop():
    while myPlayer.game_over is False:
        prompt()
    if myPlayer.game_over is True:
        sys.exit
    # here handle if puzzles have been solved, boss defeated, explored everything

def setup_game():
    os.system('cls')

### Name Collecting ###
    question1= "Hello, what is you name?\n"
    for character in question1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    player_name = input(" -> ")
    myPlayer.name = player_name
### Job Handling ###
    question2= "What role do you want to play?\n"
    question2added = "{You can only play as a warrior, mage, priest, archer, or worker.}\n"
    for character in question2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in question2added:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.01)
    player_job = input(" -> ")
    myPlayer.job = player_job
    valid_jobs = ['warrior', 'mage', 'priest', 'archer','worker']
    while player_job.lower() not in valid_jobs:
        player_job = input(" -> ")
        if player_job.lower() in valid_jobs:
            myPlayer.job = player_job
            print("You are now a " + player_job + "!\n")

    if myPlayer.job is 'warrior':
        self.hp = 120
        self.mp = 20
        print("You are now a Warrior!\n")
    elif myPlayer.job is 'mage':
        self.hp = 60
        self.mp = 120
        print("You are now a Mage!\n")
    elif myPlayer.job is 'priest':
        self.hp = 80
        self.mp = 80
        print("You are now a Priest!\n")
    elif myPlayer.job is 'archer':
        self.hp = 100
        self.mp = 40
        print("You are now an Archer!\n")
    elif myPlayer.job is 'worker':
        self.hp = 75
        self.mp = 15
        print("You are now a Worker!\n")
    ###Introduction###
    question3= "Welcome, " + player_name + " the " + player_job + ".\n"
    for character in question3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    speech1 = "Welcome to the enchanting land of Dragondia, where dragons are in control of floating continents made from the Mother Brood Dragon.\n"
    speech2 = "Within this land, one can .\n"
    speech3 = "Farthead Test 1. \n "
    speech4 = "Farthead Test 2.\n"

    for character in speech1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.03)
    myPlayer.name = player_name
    for character in speech2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.03)
    myPlayer.name = player_name
    for character in speech3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.01)
    myPlayer.name = player_name
    for character in speech4:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.2)

    os.system('cls')
    print("######################")
    print("#  Let's start now!  #")
    print("######################")
    main_game_loop()

title_screen()

main_game_loop()





































































































