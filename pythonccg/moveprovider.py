from pythonccg.gamestate import Gamestate
from pythonccg.moves import *

class MoveProvider:
    
    def get_all_moves(self, gamestate: Gamestate) -> list[object]:
        moves = []
        
        # Add moves for playing cards from hand
        for card in gamestate.hand[gamestate.active_player].cards:
            if gamestate.current_mana[gamestate.active_player] >= card.cost:
                moves.append(MovePlayCard(gamestate, card.id))
        
        # Add moves for minions attacking other minions
        for attacker in gamestate.board[gamestate.active_player].cards:
            for defender in gamestate.board[1 - gamestate.active_player].cards:
                moves.append(MoveMinionAttacksMinion(gamestate, attacker.id, defender.id))
        
        # Add moves for minions attacking the opposing player
        for minion in gamestate.board[gamestate.active_player].cards:
            moves.append(MoveMinionAttacksPlayer(gamestate, minion.id))
        
        # Add move for passing the turn
        moves.append(MovePass(gamestate))
        
        return moves