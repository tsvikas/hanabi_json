import json
from pathlib import Path

from hanabi_json import schema


def test_import():
    import hanabi_json  # noqa: F401


def test_schema():
    with Path(__file__).parent.joinpath("sample.json").open() as f:
        data = json.load(f)
        game = schema.HanabiGame.model_validate(data)
    assert game.players == ["Alice", "Bob", "Cathy", "Donald", "Emily"]
    assert len(game.deck) == 50
    assert game.deck[0].suit_index == 3
    assert game.deck[0].rank == 1
    assert game.actions == [
        schema.PlayAction(type=0, target=2),
        schema.DiscardAction(type=1, target=5),
        schema.ColorClueAction(type=2, target=1, value=0),
        schema.RankClueAction(type=3, target=1, value=3),
        schema.EndGameAction(type=4, target=1, value=3),
    ]
    assert isinstance(game.actions[4].value, schema.EndGameReason)
    assert game.options.variant == schema.HanabiGameVariant.NO_VARIANT
    assert isinstance(game.options.variant, schema.HanabiGameVariant)
    assert game.options.empty_clues is True
    assert game.options.deck_plays is False
    assert game.notes == [
        ["this is an important card", "this card should be trash"],
        ["finessed", "chop moved"],
        [],
        [],
        [],
    ]
    assert game.characters == [
        schema.Character(name="Fuming", metadata=2),
        schema.Character(name="Dumbfounded", metadata=3),
        schema.Character(name="Conservative", metadata=-1),
        schema.Character(name="Greedy", metadata=-1),
        schema.Character(name="Picky", metadata=-1),
    ]
    assert game.id == 12345
    assert game.seed == "p2v0s0"