from pythonccg.gamestate import Gamestate
from pythonccg.moves import *
from typing import List, Tuple

class MoveTreeNode:
    def __init__(self, move: object, parent: 'MoveTreeNode' = None):
        self.gamestate = move.get_new_gamestate()
        self.move = move
        self.parent = parent
        self.children: List['MoveTreeNode'] = []

    def add_followup_move(self, child_node: 'MoveTreeNode'):
        self.children.append(child_node)
        child_node.parent = self

    def get_rated_sequences(self, active_player: int) -> List[Tuple[List[object], int]]:
        sequences = []
        if self.is_pass():
            score = self.rate_gamestate(self.gamestate, active_player)
            sequences.append((self.get_sequence_to_node(), score))
        else:
            for child in self.children:
                sequences.extend(child.get_rated_sequences(active_player))
        return sequences

    def get_sequence_to_node(self) -> List[object]:
        sequence = []
        node = self
        while node is not None:
            sequence.append(node.move)
            node = node.parent
        sequence.reverse()
        return sequence

    def is_pass(self) -> bool:
        return len(self.children) == 0

    @staticmethod
    def rate_gamestate(gamestate: Gamestate, player: int) -> int:
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

    def __repr__(self):
        return f"MoveTreeNode(move={self.move}, score={self.score})"