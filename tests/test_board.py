import pytest

from board import Board


def test_player_to_string():
  board = Board(
    tokens_by_cup=[
      3, 2, 8, 0, 3, 2, -1,
      0, 0, 0, 0, 0, 0, 0,
    ],
    taken_tokens=[24, 25],
    turn=1
  )
  assert board.player_to_string(1) == "  24 * P1: [3, 2, 8, 0, 3, 2, -1]        "


def test_choices_valid():
  board = Board(
    tokens_by_cup=[
      3, 2, 8, 0, 3, 2, -1,
      0, 0, 0, 0, 0, 0, 0,
    ],
    taken_tokens=[24, 25],
    turn=1,
  )
  assert board.choices() == [0, 1, 2, 4, 5]


def test_choices_invalid():
  board = Board(
    tokens_by_cup=[
      3, 2, 8, 0, 3, 2, -1,
      0, 0, 0, 0, 0, 0, 0,
    ],
    turn=2
  )
  assert board.choices() == []


def test_is_game_over_true():
  board = Board(
    tokens_by_cup=[
      0, 0, 0, 0, 0, 0, 0,
      -1, -1, -1, -1, -1, -1, -1,
    ]
  )
  assert board.is_game_over()


def test_is_game_over_false():
  board = Board(
    tokens_by_cup=[
      0, 0, 0, 0, 0, 0, 0,
      0, -1, -1, -1, -1, -1, -1,
    ]
  )
  assert not board.is_game_over()


def test_is_round_complete_0():
  board = Board(
    tokens_by_cup=[
      0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0,
    ]
  )
  assert board.is_round_complete()


def test_is_round_complete_1():
  board = Board(
    tokens_by_cup=[
      0, 0, 0, 0, 0, 1, 0,
      0, 0, 0, 0, 0, 0, 0,
    ]
  )
  assert board.is_round_complete()


def test_is_round_complete_1_with_minuses():
  board = Board(
    tokens_by_cup=[
      0, 0, 0, 0, 0, 1, -1,
      0, 0, 0, 0, 0, -1, -1,
    ]
  )
  assert board.is_round_complete()


def test_is_round_complete_2():
  board = Board(
    tokens_by_cup=[
      0, 0, 0, 0, 0, 1, 0,
      0, 0, 0, 1, 0, 0, 0,
    ]
  )
  assert not board.is_round_complete()


def test_pass_turn_when_no_choices():
  board = Board(
    tokens_by_cup=[
      0, 0, 0, 0, 0, 0, 0,
      1, 2, 3, 4, 5, 6, 7,
    ],
    turn=1
  )
  board.pass_turn()


def test_pass_turn_when_choices():
  board = Board(
    tokens_by_cup=[
      0, 0, 0, 0, 0, 0, 0,
      1, 2, 3, 4, 5, 6, 7,
    ],
    turn=2,
  )
  with pytest.raises(ValueError):
    board.pass_turn()


def test_play_1():
  board = Board(
    tokens_by_cup=[
      5, 5, 5, 5, 5, 5, 5,
      5, 5, 5, 5, 5, 5, 5,
    ],
    taken_tokens=[0, 0],
    turn=1,
  )
  board.play(0, "Test")
  assert board.tokens_by_cup == [
    2, 8, 8, 8, 0, 0, 1,
    7, 7, 7, 7, 0, 1, 7
  ]
  assert board.taken_tokens == [7, 0]


def test_play_2():
  board = Board(
    tokens_by_cup=[
      2, 8, 8, 8, 0, 0, 1,
      7, 7, 7, 7, 0, 1, 7
    ],
    taken_tokens=[7, 0],
    turn=2,
    # visualize = True,
  )
  board.render()
  board.play(7, "Test")
  assert board.tokens_by_cup == [
    1, 2, 11, 11, 3, 0, 0,
    0, 10, 0, 1, 3, 0, 10
  ]
  assert board.taken_tokens == [11, 7]


def test_play_3():
  board = Board(
    tokens_by_cup=[
      1, 0, 1, 0, 15, 0, 0,
      3, 0, 3, 1, 0, -1, -1
    ],
    taken_tokens=[27, 19],
    turn=2,
    visualize=False,
    verbose=True
  )
  board.render(from_cup=10)
  reward = board.play(10, "Test")
  assert reward == -100
  assert board.tokens_by_cup == [
      1, 0, 1, 0, 15, 0, 0,
      3, 0, 3, 1, 0, -1, -1
  ]
  assert board.taken_tokens == [27, 19]


def test_clear_empty():
  board = Board(
    tokens_by_cup=[
      0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0,
    ],
    taken_tokens=[45, 25]
  )
  board.clear()
  assert board.tokens_by_cup == [
    0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0,
  ]
  assert board.taken_tokens == [45, 25]


def test_clear_partial():
  board = Board(
    tokens_by_cup=[
      0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 1,
    ],
    taken_tokens=[45, 24]
  )
  board.clear()
  assert board.tokens_by_cup == [
    0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0,
  ]
  assert board.taken_tokens == [45, 25]


def test_prep_35_35():
  board = Board(
    tokens_by_cup=[
      0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0,
    ],
    taken_tokens=[35, 35]
  )
  board.prep()
  assert board.tokens_by_cup == [
    5, 5, 5, 5, 5, 5, 5,
    5, 5, 5, 5, 5, 5, 5
  ]
  assert board.taken_tokens == [0, 0]


def test_prep_30_40():
  board = Board(
    tokens_by_cup=[
      0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0,
    ],
    taken_tokens=[30, 40],
  )
  board.prep()
  assert board.tokens_by_cup == [
    5, 5, 5, 5, 5, 5, -1,
    5, 5, 5, 5, 5, 5, 5
  ]
  assert board.taken_tokens == [0, 5]
