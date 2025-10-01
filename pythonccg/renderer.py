from pythonccg.card import Card
from pythonccg.gamestate import Gamestate
from pythonccg.zone import Zone

class Renderer:
    def __init__ (self):
        pass

    def ascii_render_gamestate(self, gamestate: Gamestate) -> str:
        lines = []
        lines.append(f"Player 1 Health: {gamestate.health[0]} | Mana: {gamestate.current_mana[0]}/{gamestate.max_mana[0]} | Hand size: {len(gamestate.hand[0].cards)} | Deck size: {len(gamestate.draw_deck[0].cards)}")
        lines.append("Board: " + " | ".join([f"{m.name}(ID:{m.id}, HP:{m.health}, ATK:{m.attack})" for m in gamestate.board[0].cards]))
        lines.append("-" * 50)
        lines.append("Board: " + " | ".join([f"{m.name}(ID:{m.id}, HP:{m.health}, ATK:{m.attack})" for m in gamestate.board[1].cards]))
        lines.append(f"Player 2 Health: {gamestate.health[1]} | Mana: {gamestate.current_mana[1]}/{gamestate.max_mana[1]} | Hand size: {len(gamestate.hand[1].cards)} | Deck size: {len(gamestate.draw_deck[1].cards)}")
        return "\n".join(lines)
        