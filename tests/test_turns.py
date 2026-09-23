from __future__ import annotations

import pytest

from graph import Turn, TurnType


class Geometry:
    def __init__(self, coords) -> None:  # type: ignore
        self.coords = coords


def test_turn_type_predicates_and_parser() -> None:
    assert TurnType.parse("left_elbow") is TurnType.LEFT_ELBOW
    assert TurnType.is_left_turn("sharp_left", min_type="left_elbow")
    assert TurnType.is_right_turn(TurnType.SLIGHT_RIGHT)
    assert TurnType.is_u_turn("u_turn")
    assert TurnType.is_straight("straight")

    with pytest.raises(ValueError, match="unknown turn type"):
        TurnType.is_left_turn("not-a-turn")


def test_classify_turn_geometry() -> None:
    incoming = Geometry([(0, 0), (1, 0)])
    straight = Geometry([(1, 0), (2, 0)])
    left = Geometry([(1, 0), (1, 1)])

    assert Turn.classify_turn(incoming, straight) is TurnType.STRAIGHT
    assert TurnType.classify_turn(incoming, left) is TurnType.LEFT_ELBOW
