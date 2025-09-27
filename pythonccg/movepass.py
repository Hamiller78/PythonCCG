from pythonccg.zone import Gamestate

class MovePass:
    def __init__(self, gamestate: Gamestate):
        self.gamestate = gamestate

    def get_new_gamestate(self) -> Gamestate:
        new_gamestate = self.gamestate.clone()
        new_gamestate.active_player = 1 - new_gamestate.active_player
        new_gamestate.max_mana[new_gamestate.active_player] = min(new_gamestate.max_mana[new_gamestate.active_player] + 1, 10)
        new_gamestate.current_mana[new_gamestate.active_player] = new_gamestate.max_mana[new_gamestate.active_player]
        
        # Draw a card at the start of the turn if possible
        if new_gamestate.draw_deck[new_gamestate.active_player].cards:
            drawn_card = new_gamestate.draw_deck[new_gamestate.active_player].remove_top()
            new_gamestate.hand[new_gamestate.active_player].add_to_top(drawn_card)
        
        return new_gamestate