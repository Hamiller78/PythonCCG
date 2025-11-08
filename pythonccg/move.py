from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional
from pythonccg.gamestate import Gamestate


class Move(ABC):
    """Abstract base class for all moves.

    Subclasses must implement `get_new_gamestate()` and may use the
    `_new_gamestate` cache and `_output_text` helpers provided here.
    """

    def __init__(self, gamestate: Gamestate):
        self.gamestate: Gamestate = gamestate
        # Cache for idempotent get_new_gamestate calls. Child classes may set
        # self._new_gamestate when they compute the resulting state.
        self._new_gamestate: Optional[Gamestate] = None
        # Friendly output text used by __repr__. Child classes should set
        # this to provide a human-readable description of the move.
        self._output_text: Optional[str] = None

    def __repr__(self) -> str:
        if self._output_text is not None:
            return self._output_text
        return f"{self.__class__.__name__}"

    @abstractmethod
    def get_new_gamestate(self) -> Gamestate:
        """Return a new Gamestate produced by applying this move.

        Implementations should cache the result in `self._new_gamestate` and
        return it on subsequent calls to make repeated evaluation cheap.
        """
        raise NotImplementedError()
