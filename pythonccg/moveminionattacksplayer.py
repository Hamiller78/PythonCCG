from pythonccg.gamestate import Gamestate

class MoveMinionAttacksPlayer:
    def __init__(self, gamestate: Gamestate, minion_id: int):
        self.minion_id = minion_id
        self.gamestate = gamestate
        self.minion_id = minion_id
        self._new_gamestate = None

    def get_new_gamestate(self) -> Gamestate:
        if self._new_gamestate is not None:
            return self._new_gamestate
        
        new_gamestate = self.gamestate.clone()
        attacker = next((m for m in new_gamestate.board[new_gamestate.active_player].cards if m.id == self.minion_id), None)

        if attacker is None:
            raise ValueError("Attacking minion not found on the board.")

        # Deal damage to the opposing player
        new_gamestate.health[1 - new_gamestate.active_player] -= attacker.attack
        self._new_gamestate = new_gamestate
        
        return new_gamestate