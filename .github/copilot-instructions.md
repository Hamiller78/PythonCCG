## Quick context

This repository is a small, self-contained Python collectible-card-game (CCG) engine. The runtime is in the `pythonccg/` package. Key runtime concepts are Gamestate (a simple immutable-by-convention clone-and-mutate pattern), Move objects (each implements `get_new_gamestate()`), a MoveProvider that enumerates legal moves, and a MoveSelector that builds move trees to rate sequences.

## Where to look first (core files)

- `pythonccg/gamestate.py` — the game state object and `clone()` behavior (shallow lists + zone/card clones).
- `pythonccg/moveprovider.py` — enumerates legal moves for the current player.
- `pythonccg/moves.py` and `pythonccg/move*.py` — move implementations. Each move class exposes `get_new_gamestate()` and `__repr__()` for human output.
- `pythonccg/movetreenode.py` — builds sequences and scores gamestates (see `rate_gamestate`).
- `pythonccg/moveselector.py` — orchestrates building move trees and selecting the best move sequence.
- `pythonccg/gameloop.py` and `pythonccg/main.py` — how the loop runs and renders output via `pythonccg/renderer.py`.
- `pythonccg/cardpool.py`, `pythonccg/assets/BasicSet.csv`, `pythonccg/assets/Decklist.txt` — card data and deck-building.

## Important patterns & conventions (strictly derived from code)

- Clone-before-mutate: all Move implementations call `gamestate.clone()` then apply changes and return the cloned state. Do not mutate the passed-in gamestate directly.
- Moves cache results: `get_new_gamestate()` implementations often cache `_new_gamestate` to make repeated calls idempotent and cheap.
- Identification by numeric `id`: cards carry an `id` assigned by `Cardpool._id()`. Code frequently looks up cards/minions by `id` (see `MovePlayCard` and minion-attack moves).
- Active player is an int 0 or 1 stored on `gamestate.active_player`. Many routines index arrays by player index (health, hand, board, mana).
- Pass is the terminal action: `MovePass` flips `active_player`, readies minions and draws. In `MoveSelector`, a node with no children is treated as a pass/leaf and scored.

## How to add a new Move

1. Create `pythonccg/moveyourmove.py` implementing `__init__(self, gamestate, ...)`, `__repr__()`, and `get_new_gamestate()` that clones the gamestate, mutates and returns it. Follow patterns from `moveplaycard.py`.
2. Add the class name to `pythonccg/moves.py` and update `MoveProvider.get_all_moves()` if the move needs to be enumerated.
3. Ensure any new card interactions that need IDs use `Cardpool.create_card_by_name()` and respect card cloning.

## Move base class (new)

This project now centralizes common move behavior in `pythonccg/move.py` as an abstract base class `Move`.

- Location: `pythonccg/move.py` — `class Move(ABC)`
- Contract: implement `get_new_gamestate(self) -> Gamestate` (it's an @abstractmethod). Subclasses must call `super().__init__(gamestate)` in `__init__`.
- Helpers: subclasses can use `self._new_gamestate` to cache results and `self._output_text` for a human-readable `__repr__()`.
- Pattern: do not mutate the passed `gamestate`; clone first, mutate the clone, set `self._new_gamestate` and return it.

Minimal move template (copy & adapt):

```python
from pythonccg.move import Move
from pythonccg.gamestate import Gamestate

class MoveYourMove(Move):
	def __init__(self, gamestate: Gamestate, ...):
		super().__init__(gamestate)
		self._output_text = "MoveYourMove(...)"

	def get_new_gamestate(self) -> Gamestate:
		if self._new_gamestate is not None:
			return self._new_gamestate
		new_state = self.gamestate.clone()
		# mutate new_state
		self._new_gamestate = new_state
		return new_state
```

## How move selection works (brief)

- `MoveProvider.get_all_moves(gamestate)` returns a flat list of legal move objects.
- `MoveSelector.get_movetree()` builds a MoveTreeNode recursively for each starting move; `MoveTreeNode.get_rated_sequences()` traverses leaves (passes) and uses `rate_gamestate()` to score.
- `rate_gamestate()` is a deterministic heuristic in `movetreenode.py` (health, minion stats, hand sizes, mana). Win/lose states produce +/-100000.

## Run / debug instructions

- Run a sample game from project root: `python -m pythonccg.main` (or `python pythonccg/main.py`). The game loop prints a text board via `Renderer.ascii_render_gamestate()` and pauses on `input()` between moves.
- To step through AI selection, add breakpoints in `pythonccg/moveselector.py` or `pythonccg/movetreenode.py`. Logging is produced via `print()` calls for sequences in `get_sequences()`.

## Tests & safety checks

- There are no tests in the repo by default. When adding behavior, preferred fast checks are small scripts that instantiate a `Gamestate`, call `MoveProvider.get_all_moves()` and `get_new_gamestate()` to validate cloning and invariants (IDs preserved/unique, no in-place mutation).

## Things an AI/code assistant should not change without care

- The `clone()` semantics in `Gamestate` and `Zone.clone()`—changing clone depth changes all move logic.
- `Card.id` allocation in `Cardpool._id()`—IDs are expected to be stable for lookups.

## Short examples (where to copy patterns)

- Play card pattern: `pythonccg/moveplaycard.py` — find card in hand by id, check mana, remove from hand, add to board, decrement mana.
- Attack pattern: `pythonccg/moveminionattacksminion.py` — locate attacker/defender by id on each player's board, exchange damage, remove dead minions.

If anything in this file is unclear or you'd like more detail (examples for tests, typing hints, or help adding a new move), tell me which section and I will iterate.
