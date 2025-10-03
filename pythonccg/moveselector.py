from pythonccg.gamestate import Gamestate
from pythonccg.moves import *
from typing import List, Tuple

class MoveSelector:
    def __init__(self):
        pass

    # def select_move(self, possible_moves: list[object]) -> list[object]:
    #     play_moves = [move for move in possible_moves if isinstance(move, MovePlayCard)]
    #     if len(play_moves) > 0:
    #         return play_moves
        
    #     attack_moves = [move for move in possible_moves if isinstance(move, MoveMinionAttacksMinion) or isinstance(move, MoveMinionAttacksPlayer)]
    #     if len(attack_moves) > 0:
    #         return attack_moves
        
    #     return [move for move in possible_moves if isinstance(move, MovePass)]
 
    def select_move(self, active_player: int, possible_moves: list[object]) -> object:
        if not possible_moves:
            raise ValueError("No possible moves to select from.")
        
        best_moves = self.get_best_moves(active_player, possible_moves, moves_to_keep=1)
        best_move = best_moves[0]  # Since we only keep one best move

        return best_move

    def get_best_moves(self, active_player: int, possible_moves: list[object], moves_to_keep: int) -> List[object]:
        scored_moves: List[Tuple[object, int]] = []
        for move in possible_moves:
            new_gamestate = move.get_new_gamestate()
            score = self.rate_gamestate(new_gamestate, active_player)
            scored_moves.append((move, score))
        
        scored_moves.sort(key=lambda x: x[1], reverse=True)

        # Print the scores for debugging
        print("Move Scores:")
        for move, score in scored_moves:
            print(f"{repr(move)}: {score}")

        best_moves = [move for move, score in scored_moves[:moves_to_keep]]
        
        return best_moves

    def rate_gamestate(self, gamestate: Gamestate, player: int) -> int:
        if gamestate.health[player] <= 0:
            return -100000  # Losing state

        if gamestate.health[1 - player] <= 0:
            return 100000  # Winning state

        score = 0
        score += gamestate.health[player] * 3
        score -= gamestate.health[1 - player] * 3
        score += sum(minion.attack + minion.health for minion in gamestate.board[player].cards) * 2
        score -= sum(minion.attack + minion.health for minion in gamestate.board[1 - player].cards) * 2
        score += len(gamestate.hand[player].cards)
        score -= len(gamestate.hand[1 - player].cards)
        score += gamestate.current_mana[player]
        score -= gamestate.current_mana[1 - player]

        return score