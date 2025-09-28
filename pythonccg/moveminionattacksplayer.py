from pythonccg.gamestate import Gamestate

class MoveMinionAttacksPlayer:
    def __init__(self, gamestate: Gamestate, minion_id: int):
        self.minion_id = minion_id
        self.gamestate = gamestate
        self.minion_id = minion_id
        self._new_gamestate = None
        self._output_text = f"MoveMinionAttacksPlayer(minion_id={self.minion_id})"

    def __repr__(self):
        return self._output_text

    def get_new_gamestate(self) -> Gamestate:
        if self._new_gamestate is not None:
            return self._new_gamestate
        
        new_gamestate = self.gamestate.clone()
        attacker = next((m for m in new_gamestate.board[new_gamestate.active_player].cards if m.id == self.minion_id), None)

        if attacker is None:
            raise ValueError("Attacking minion not found on the board.")

        self._output_text = (f"Player {new_gamestate.active_player + 1}'s Minion {attacker.name} (ID: {attacker.id}) attacks Player "
                f"{1 - new_gamestate.active_player + 1} for {attacker.attack} damage")

        # Deal damage to the opposing player
        new_gamestate.health[1 - new_gamestate.active_player] -= attacker.attack
        self._new_gamestate = new_gamestate
        
        return new_gamestate