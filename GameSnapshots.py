import cv2
from termcolor import colored
import threading
import numpy as np
import keyboard
from time import sleep
from APICaller import APICaller
from Bot import Bot
from StateMachine import StateMachine
from StateMachine import DeckType, GameState
import sys
from download_card_sets import download_missing_card_sets, delete_card_sets

download_missing_card_sets()

state_machine = StateMachine()

sleep(0.1)  # Necessary if we want to call get_window_info_frames now

if state_machine.get_window_info_frames()[0][:2] == (-1, -1):  # Only check if x and y coords are -1
    print(colored("Legends of Runeterra isn't running!", "red"))
    exit(1)

print("Starting API caller...")
api_caller = APICaller()
api_thread = threading.Thread(target=api_caller.call_api)
api_thread.daemon = True
api_thread.start()
print("Ready.")

while True:
    
    # Missing: mana values, nexus health, card stats, game state
    print("Fetching info...")
    print("Getting game data...")
    state_machine.set_game_data(api_caller.get_game_data())
    state_machine.set_cards_data(api_caller.get_cards_data())
    state_machine.set_game_result(api_caller.get_game_result())
    print("Getting cards on board...")
    game_state, cards_on_board, deck_type, n_games, games_won = state_machine.get_game_info()
    print(game_state)
    for card_area, cards in cards_on_board.items():
        print(card_area)
        for card in cards:
            print(card)
    print("Done.")
    sleep(.5)