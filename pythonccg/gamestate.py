from pythonccg.zone import Zone


class Gamestate:
    def __init__(self):
        self.health = [30, 30]
        self.draw_deck = [Zone(name="Draw Deck 1"), Zone(name="Draw Deck 2")]
        self.hand = [Zone(name="Hand 1"), Zone(name="Hand 2")]
        self.board = [Zone(name="Board 1"), Zone(name="Board 2")]
        self.active_player = 0
        self.max_mana = [1, 1]
        self.current_mana = [1, 1]

    def clone(self):
        new_state = Gamestate()
        new_state.health = self.health[:]
        new_state.draw_deck = [zone.clone() for zone in self.draw_deck]
        new_state.hand = [zone.clone() for zone in self.hand]
        new_state.board = [zone.clone() for zone in self.board]
        new_state.active_player = self.active_player
        new_state.max_mana = self.max_mana[:]
        new_state.current_mana = self.current_mana[:]
        return new_state
