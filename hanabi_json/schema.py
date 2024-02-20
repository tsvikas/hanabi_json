# https://raw.githubusercontent.com/Hanabi-Live/hanabi-live/main/misc/example_game_with_comments.jsonc
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
    suit_index: SuitIndex = Field(alias="suitIndex")
    rank: Rank


class ActionType(enum.IntEnum):
    PLAY = 0
    DISCARD = 1
    COLOR_CLUE = 2
    RANK_CLUE = 3
    END_GAME = 4


class BaseAction(BaseModel):
    type: ActionType


class PlayAction(BaseAction):
    type: Literal[ActionType.PLAY]
    target: CardIndex  # card played


class DiscardAction(BaseAction):
    type: Literal[ActionType.DISCARD]
    target: CardIndex  # card discarded


class ColorClueAction(BaseAction):
    type: Literal[ActionType.COLOR_CLUE]
    target: PlayerIndex  # player receiving the clue
    value: SuitIndex  # suit of the clue


class RankClueAction(BaseAction):
    type: Literal[ActionType.RANK_CLUE]
    target: PlayerIndex  # player receiving the clue
    value: Rank  # rank of the clue


class EndGameReason(enum.IntEnum):
    # https://github.com/Hanabi-Live/hanabi-live/blob/main/packages/game/src/enums/EndCondition.ts
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
    type: Literal[ActionType.END_GAME]
    target: PlayerIndex  # player who caused the end of the game
    value: EndGameReason  # reason for the end of the game


Action = Annotated[
    PlayAction | DiscardAction | ColorClueAction | RankClueAction | EndGameAction,
    Discriminator("type"),
]


class HanabiGameVariant(enum.StrEnum):
    # https://github.com/Hanabi-Live/hanabi-live/blob/main/misc/variants.txt
    NO_VARIANT = "No Variant"


class HanabiGameOptions(BaseModel):
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
    name: str
    metadata: int


class HanabiGame(BaseModel):
    players: list[PlayerName]
    deck: list[Card]
    actions: list[Action]
    options: HanabiGameOptions = HanabiGameOptions()
    notes: GameNotes | None = None
    characters: list[Character] | None = None
    id: int | None = None  # database ID
    seed: str | None = None
