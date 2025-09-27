from pythonccg.gamestate import Gamestate

class MoveMinionAttacksMinion:
    def __init__(self, gamestate: Gamestate, attacker_id: int, defender_id: int):
        self.gamestate = gamestate
        self.attacker_id = attacker_id
        self.defender_id = defender_id
        self._new_gamestate = None

    def get_new_gamestate(self) -> Gamestate:
        if self._new_gamestate is not None:
            return self._new_gamestate

        new_gamestate = self.gamestate.clone()
        attacker = next((m for m in new_gamestate.board[new_gamestate.active_player].cards if m.id == self.attacker_id), None)
        defender = next((m for m in new_gamestate.board[1 - new_gamestate.active_player].cards if m.id == self.defender_id), None)

        if attacker is None or defender is None:
            raise ValueError("Attacker or defender not found on the board.")

        # Both minions deal damage to each other
        defender.health -= attacker.attack
        attacker.health -= defender.attack

        # Remove dead minions from the board
        if defender.health <= 0:
            new_gamestate.board[1 - new_gamestate.active_player].cards.remove(defender)
        if attacker.health <= 0:
            new_gamestate.board[new_gamestate.active_player].cards.remove(attacker)

        self._new_gamestate = new_gamestate
        return self._new_gamestate