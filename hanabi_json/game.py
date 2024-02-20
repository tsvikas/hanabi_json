"""Object for a game of Hanabi."""

from .schema import HanabiGameModel


class HanabiGame(HanabiGameModel):
    """Represents a game of Hanabi. Tracks the state over time."""

    @property
    def number_of_players(self) -> int:
        """The number of players in the game."""
        return len(self.players)

    @property
    def cards_per_player(self) -> int:
        """The number of cards each player starts with."""
        variant_effect = 0
        if self.options.one_less_card:
            variant_effect -= 1
        if self.options.one_extra_card:
            variant_effect += 1
        return variant_effect + {2: 5, 3: 5, 4: 4, 5: 4, 6: 3}[self.number_of_players]
