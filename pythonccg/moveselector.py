from pythonccg.moves import *

class MoveSelector:
    def __init__(self):
        pass

    def select_move(self, possible_moves: list[object]) -> list[object]:
        play_moves = [move for move in possible_moves if isinstance(move, MovePlayCard)]
        if len(play_moves) > 0:
            return play_moves
        
        attack_moves = [move for move in possible_moves if isinstance(move, MoveMinionAttacksMinion) or isinstance(move, MoveMinionAttacksPlayer)]
        if len(attack_moves) > 0:
            return attack_moves
        
        return [move for move in possible_moves if isinstance(move, MovePass)]