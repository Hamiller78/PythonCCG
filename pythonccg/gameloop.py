from pythonccg.cardpool import Cardpool
from pythonccg.gamestate import Gamestate
from pythonccg.moveprovider import MoveProvider
from pythonccg.moves import *
from pythonccg.zone import Zone
import os
import random

class Gameloop:

    def __init__(self):
        pass

    def setup_game(self) -> Gamestate:
        cardpool = Cardpool()
        assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets'))
        cardpool.load_from_csv(os.path.join(assets_dir, 'BasicSet.csv'))

        initial_state = Gamestate()
        decklist_path = os.path.join(assets_dir, 'Decklist.txt')
        initial_state.draw_deck[0].fill_from_file(decklist_path, cardpool)
        initial_state.draw_deck[1].fill_from_file(decklist_path, cardpool)

        for _ in range(3):
            initial_state.hand[0].add_to_bottom(initial_state.draw_deck[0].remove_from_top())
            initial_state.hand[1].add_to_bottom(initial_state.draw_deck[1].remove_from_top())
        initial_state.hand[1].add_to_bottom(initial_state.draw_deck[1].remove_from_top())

        return initial_state

    def run_game(self, initial_state: Gamestate) -> int:
        current_state = initial_state
        while True:
            available_moves = MoveProvider().get_all_moves(initial_state)
            selected_move = random.choice(available_moves)
            new_state = selected_move.get_new_gamestate()

            if new_state.health[0] <= 0 and new_state.health[1] <= 0:
                print("The game is a draw!")
                return -1  # Draw
            elif new_state.health[0] <= 0:
                print("Player 2 wins!")
                return 1  # Player 2 wins
            elif new_state.health[1] <= 0:
                print("Player 1 wins!")
                return 0  # Player 1 wins