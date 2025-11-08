from pythonccg.gamestate import Gamestate
from pythonccg.moveprovider import MoveProvider
from pythonccg.moves import *
from pythonccg.movetreenode import MoveTreeNode
from pythonccg.move import Move
from typing import List, Tuple

class MoveSelector:
    def __init__(self):
        pass
 
    @staticmethod
    def select_move(active_player: int, gamestate: Gamestate) -> Move:
        best_sequences = MoveSelector.get_sequences(active_player, gamestate)
        best_sequence = best_sequences[0][0]
        best_move = best_sequence[0]

        return best_move

    @staticmethod
    def get_sequences(active_player: int, gamestate: Gamestate) -> List[Tuple[List[Move], int]]:
        initial_moves = MoveProvider().get_all_moves(gamestate)
        all_sequences: List[Tuple[List[Move], int]] = []

        for move in initial_moves:
            movetree = MoveSelector.get_movetree(active_player, move)
            sequences = movetree.get_rated_sequences(active_player)
            all_sequences.extend(sequences)

        all_sequences.sort(key=lambda x: x[1], reverse=True)
        for seq in all_sequences:
            print(f"Sequence: {[repr(m) for m in seq[0]]}, Score: {seq[1]}")
        return all_sequences

    @staticmethod
    def get_movetree(active_player: int, move: Move) -> MoveTreeNode:
        root_node = MoveTreeNode(move)

        if isinstance(move, MovePass):
            root_node.score = MoveTreeNode.rate_gamestate(root_node.gamestate, active_player)
            return root_node

        possible_moves = MoveProvider().get_all_moves(root_node.gamestate)
        for next_move in possible_moves:
            if active_player != root_node.gamestate.active_player and isinstance(next_move, MovePlayCard):
                continue
            child_node = MoveSelector.get_movetree(active_player, next_move)

            root_node.add_followup_move(child_node)
        return root_node