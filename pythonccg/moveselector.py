from pythonccg.gamestate import Gamestate
from pythonccg.moveprovider import MoveProvider
from pythonccg.moves import *
from pythonccg.movetreenode import MoveTreeNode
from typing import List, Tuple

class MoveSelector:
    def __init__(self):
        pass
 
    @staticmethod
    def select_move(active_player: int, gamestate: Gamestate) -> object:
        best_sequences = MoveSelector.get_sequences(active_player, gamestate)
        best_sequence = best_sequences[0][0]
        best_move = best_sequence[0]

        return best_move

    @staticmethod
    def get_sequences(active_player: int, gamestate: Gamestate) -> List[Tuple[List[object], int]]:
        initial_moves = MoveProvider().get_all_moves(gamestate)
        all_sequences: List[Tuple[List[object], int]] = []
        
        for move in initial_moves:
            movetree = MoveSelector.get_movetree(active_player, move)
            sequences = movetree.get_rated_sequences()
            all_sequences.extend(sequences)
        
        all_sequences.sort(key=lambda x: x[1], reverse=True)
        return all_sequences

    @staticmethod
    def get_movetree(active_player: int, move: object) -> MoveTreeNode:
        root_node = MoveTreeNode(move)

        possible_moves = MoveProvider().get_all_moves(root_node.gamestate)
        for next_move in possible_moves:
            if active_player != root_node.gamestate.active_player and isinstance(next_move, MovePlayCard):
                continue
            if isinstance(next_move, MovePass):
                child_node = MoveTreeNode(next_move, parent=root_node)
                child_node.score = MoveTreeNode.rate_gamestate(child_node.gamestate, active_player)
            else:
                child_node = MoveSelector.get_movetree(active_player, next_move)

            root_node.add_followup_move(child_node)
        return root_node