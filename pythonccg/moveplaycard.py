from pythonccg.gamestate import Gamestate

class MovePlayCard:
    def __init__(self, gamestate: Gamestate, card_id: int):
        self.card_id = card_id
        self.gamestate = gamestate
        self.card_id = card_id
        self._new_gamestate = None

    def get_new_gamestate(self) -> Gamestate:
        if self._new_gamestate is not None:
            return self._new_gamestate

        new_gamestate = self.gamestate.clone()
        card = next((c for c in new_gamestate.hand[new_gamestate.active_player].cards if c.id == self.card_id), None)

        if card is None:
            raise ValueError("Card not found in hand.")

        if new_gamestate.current_mana[new_gamestate.active_player] < card.cost:
            raise ValueError("Not enough mana to play this card.")

        # Play the card: remove from hand, add to board, reduce mana
        new_gamestate.hand[new_gamestate.active_player].cards.remove(card)
        new_gamestate.board[new_gamestate.active_player].add_to_top(card)
        new_gamestate.current_mana[new_gamestate.active_player] -= card.cost

        self._new_gamestate = new_gamestate
        return new_gamestate