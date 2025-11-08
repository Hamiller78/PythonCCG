from pythonccg.gamestate import Gamestate
from pythonccg.move import Move


class MovePass(Move):
    def __init__(self, gamestate: Gamestate):
        super().__init__(gamestate)

    def __repr__(self):
        return f"Player {self.gamestate.active_player + 1} passes their turn."

    def get_new_gamestate(self) -> Gamestate:
        new_gamestate = self.gamestate.clone()
        new_gamestate.active_player = 1 - new_gamestate.active_player
        new_gamestate.max_mana[new_gamestate.active_player] = min(new_gamestate.max_mana[new_gamestate.active_player] + 1, 10)
        new_gamestate.current_mana[new_gamestate.active_player] = new_gamestate.max_mana[new_gamestate.active_player]
        
        # Draw a card at the start of the turn if possible
        if new_gamestate.draw_deck[new_gamestate.active_player].cards:
            drawn_card = new_gamestate.draw_deck[new_gamestate.active_player].remove_from_top()
            new_gamestate.hand[new_gamestate.active_player].add_to_top(drawn_card)
        
        # Ready all minions on the board for the new active player
        for minion in new_gamestate.board[new_gamestate.active_player].cards:
            minion.is_ready = True

        return new_gamestate