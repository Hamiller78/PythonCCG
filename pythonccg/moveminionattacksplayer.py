from pythonccg.gamestate import Gamestate

class MoveMinionAttacksPlayer:
    def __init__(self, gamestate: Gamestate, minion_id: int):
        self.minion_id = minion_id

    def get_new_gamestate(self) -> Gamestate:
        new_gamestate = self.gamestate.clone()
        attacker = next((m for m in new_gamestate.board[new_gamestate.active_player].cards if m.id == self.minion_id), None)

        if attacker is None:
            raise ValueError("Attacking minion not found on the board.")

        # Deal damage to the opposing player
        new_gamestate.health[1 - new_gamestate.active_player] -= attacker.attack

        return new_gamestate