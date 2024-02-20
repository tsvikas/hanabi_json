"""
Schema for a game of Hanabi.

allows raeding and writing a JSON file with the game state.
"""

from .game import HanabiGame

__version__ = "0.0.0"  # managed by poetry-dynamic-versioning
__all__ = ["HanabiGame"]
