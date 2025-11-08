from pythonccg.gamestate import Gamestate
from pythonccg.move import Move


class MoveMinionAttacksMinion(Move):
    def __init__(self, gamestate: Gamestate, attacker_id: int, defender_id: int):
        super().__init__(gamestate)
        self.attacker_id = attacker_id
        self.defender_id = defender_id
        self._output_text = (f"MoveMinionAttacksMinion(attacker_id={self.attacker_id}, "
                f"defender_id={self.defender_id})")

    def get_new_gamestate(self) -> Gamestate:
        if self._new_gamestate is not None:
            return self._new_gamestate

        new_gamestate = self.gamestate.clone()
        attacker = next((m for m in new_gamestate.board[new_gamestate.active_player].cards if m.id == self.attacker_id), None)
        defender = next((m for m in new_gamestate.board[1 - new_gamestate.active_player].cards if m.id == self.defender_id), None)

        if attacker is None or defender is None:
            raise ValueError("Attacker or defender not found on the board.")

        self._output_text = (f"Player {new_gamestate.active_player + 1}'s Minion {attacker.name} (ID: {attacker.id}) attacks Minion {defender.name} (ID: {defender.id})")

        # Both minions deal damage to each other
        defender.health -= attacker.attack
        attacker.health -= defender.attack
        attacker.is_ready = False

        # Remove dead minions from the board
        if defender.health <= 0:
            new_gamestate.board[1 - new_gamestate.active_player].cards.remove(defender)
            self._output_text += f"; Defender {defender.name} (ID: {defender.id}) is destroyed!"

        if attacker.health <= 0:
            new_gamestate.board[new_gamestate.active_player].cards.remove(attacker)
            self._output_text += f"; Attacker {attacker.name} (ID: {attacker.id}) is destroyed!"

        self._new_gamestate = new_gamestate
        return self._new_gamestate