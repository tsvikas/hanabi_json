"""
Schema for a game of Hanabi.

This schema is based on the JSON format used by the "Hanabi Live" website:
https://raw.githubusercontent.com/Hanabi-Live/hanabi-live/main/misc/example_game_with_comments.jsonc
"""

import enum
from typing import Annotated, Literal

from pydantic import BaseModel, Discriminator, Field

PlayerName = str
SuitIndex = int
Rank = int
CardIndex = int
PlayerIndex = int
CardNote = str
PlayerNotes = list[CardNote]
GameNotes = list[PlayerNotes]


class Card(BaseModel):
    """
    A card in the game.

    suit_index: The index of the suit of the card
    rank: The rank of the card
    """

    suit_index: SuitIndex = Field(alias="suitIndex")
    rank: Rank


class ActionType(enum.IntEnum):
    """The type of action performed."""

    PLAY = 0
    DISCARD = 1
    COLOR_CLUE = 2
    RANK_CLUE = 3
    END_GAME = 4


class BaseAction(BaseModel):
    """
    An action that the players performed in the game.

    type: The type of action performed
    """

    type: ActionType


class PlayAction(BaseAction):
    """
    A "play" action (type 0).

    target: The index of the card that is being discarded
    """

    type: Literal[ActionType.PLAY]
    target: CardIndex


class DiscardAction(BaseAction):
    """
    A "discard" action (type 1).

    target: The index of the card that is being discarded
    """

    type: Literal[ActionType.DISCARD]
    target: CardIndex


class ColorClueAction(BaseAction):
    """
    A "color clue" action (type 2).

    target: The index of the player that is receiving the clue
    value: The value for a color clue is the index from the possible colors
    """

    type: Literal[ActionType.COLOR_CLUE]
    target: PlayerIndex
    value: SuitIndex


class RankClueAction(BaseAction):
    """
    A "rank clue" action (type 3).

    target: The index of the player that is receiving the clue
    value: The value for a rank clue is equal to the rank chosen for the clue (1
    corresponds to rank 1)
    """

    type: Literal[ActionType.RANK_CLUE]
    target: PlayerIndex
    value: Rank


class EndGameReason(enum.IntEnum):
    """
    The reason for ending the game.

    corresponding to the "endCondition" value in
    https://github.com/Hanabi-Live/hanabi-live/blob/main/packages/game/src/enums/EndCondition.ts
    """

    IN_PROGRESS = 0
    NORMAL = 1
    STRIKEOUT = 2
    TIMEOUT = 3
    TERMINATED_BY_PLAYER = 4
    SPEEDRUN_FAIL = 5
    IDLE_TIMEOUT = 6
    CHARACTER_SOFTLOCK = 7
    ALL_OR_NOTHING_FAIL = 8
    ALL_OR_NOTHING_SOFTLOCK = 9
    TERMINATED_BY_VOTE = 10


class EndGameAction(BaseAction):
    """
    An "end game" action (type 4).

    target: The index of the player that is ending the game
    value: The reason for ending the game
    """

    type: Literal[ActionType.END_GAME]
    target: PlayerIndex
    value: EndGameReason


Action = Annotated[
    PlayAction | DiscardAction | ColorClueAction | RankClueAction | EndGameAction,
    Discriminator("type"),
]


class HanabiGameVariant(enum.StrEnum):
    """
    The name of the variant (e.g. "No Variant" for the base game).

    A full list of variants can be found here:
    https://github.com/Hanabi-Live/hanabi-live/blob/main/misc/variants.txt
    """

    NO_VARIANT = "No Variant"


class HanabiGameOptions(BaseModel):
    """The options for the game."""

    variant: HanabiGameVariant = HanabiGameVariant.NO_VARIANT
    # https://github.com/Hanabi-Live/hanabi-live/blob/main/server/src/options.go
    starting_player: int = Field(alias="startingPlayer", default=0)
    timed: bool = Field(alias="timed", default=False)
    time_base: int = Field(alias="timeBase", default=0)
    time_per_turn: int = Field(alias="timePerTurn", default=0)
    speedrun: bool = Field(alias="speedrun", default=False)
    card_cycle: bool = Field(alias="cardCycle", default=False)
    deck_plays: bool = Field(alias="deckPlays", default=False)
    empty_clues: bool = Field(alias="emptyClues", default=False)
    one_extra_card: bool = Field(alias="oneExtraCard", default=False)
    one_less_card: bool = Field(alias="oneLessCard", default=False)
    all_or_nothing: bool = Field(alias="allOrNothing", default=False)
    detrimental_characters: bool = Field(alias="detrimentalCharacters", default=False)


class Character(BaseModel):
    """
    The "Detrimental Character" specification for each player.

    "Detrimental Characters" is an optional setting used on the website that is based
    on a post from Sean McCarthy:
    https://boardgamegeek.com/thread/1688194/hanabi-characters-variant
    """

    name: str
    metadata: int


class HanabiGame(BaseModel):
    """
    Represents a game of Hanabi.

    This also matches how games are stored in the database for the "Hanab Live" website.
    Format version: 3.0.0

    players: is an array that contains the names of the players. The 0th player will
    always go first.
    deck: is an array that contains all the cards in the deck. It lists the cards from
    top to bottom. Cards are dealt to the first player until they reach the maximum
    number of cards, then cards are dealt to the second player until they reach the
    maximum number of cards, and so forth.
    actions: is an array that contains all the actions that the players performed in
    the game.
    options: is an object that contains the options for the game.
    notes: is an array that contains the notes for each player. Each player's notes are
    an array of strings, where each string is a note for each card in the deck. This is
    an optional setting.
    characters: is an array that contains the "Detrimental Character" specification for
    each player. This is an optional setting.
    id: integer that corresponds to the database ID of the game on the "Hanab Live"
    website. This is an optional setting.
    seed: string corresponding to the seed of the game on the "Hanab Live" website. This
    is an optional setting.
    """

    players: list[PlayerName]
    deck: list[Card]
    actions: list[Action]
    options: HanabiGameOptions = HanabiGameOptions()
    notes: GameNotes | None = None
    characters: list[Character] | None = None
    id: int | None = None  # database ID
    seed: str | None = None
