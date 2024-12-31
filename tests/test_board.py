from unittest import TestCase

from src.board import Board


class TestBoard(TestCase):
  def test_player_to_string(self):
    board = Board(
      tokens_by_cup=[
        3, 2, 8, 0, 3, 2, -1,
        0, 0, 0, 0, 0, 0, 0,
      ],
      taken_tokens=[24, 25],
      turn=1
    )
    self.assertEqual(board.player_to_string(1), "  24 * P1: [3, 2, 8, 0, 3, 2, -1]        ")

  def test_choices_valid(self):
    board = Board(
      tokens_by_cup=[
        3, 2, 8, 0, 3, 2, -1,
        0, 0, 0, 0, 0, 0, 0,
      ],
      taken_tokens=[24, 25],
      turn=1,
    )
    self.assertEqual(board.choices(), [0, 1, 2, 4, 5])

  def test_choices_invalid(self):
    board = Board(
      tokens_by_cup=[
        3, 2, 8, 0, 3, 2, -1,
        0, 0, 0, 0, 0, 0, 0,
      ],
      turn=2
    )
    self.assertEqual(board.choices(), [])

  def test_is_game_over_true(self):
    board = Board(
      tokens_by_cup=[
        0, 0, 0, 0, 0, 0, 0,
        -1, -1, -1, -1, -1, -1, -1,
      ]
    )
    self.assertTrue(board.is_game_over())

  def test_is_game_over_false(self):
    board = Board(
      tokens_by_cup=[
        0, 0, 0, 0, 0, 0, 0,
        0, -1, -1, -1, -1, -1, -1,
      ]
    )
    self.assertFalse(board.is_game_over())

  def test_is_round_complete_0(self):
    board = Board(
      tokens_by_cup=[
        0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0,
      ]
    )
    self.assertTrue(board.is_round_complete())

  def test_is_round_complete_1(self):
    board = Board(
      tokens_by_cup=[
        0, 0, 0, 0, 0, 1, 0,
        0, 0, 0, 0, 0, 0, 0,
      ]
    )
    self.assertTrue(board.is_round_complete())

  def test_is_round_complete_1_with_minuses(self):
    board = Board(
      tokens_by_cup=[
        0, 0, 0, 0, 0, 1, -1,
        0, 0, 0, 0, 0, -1, -1,
      ]
    )
    self.assertTrue(board.is_round_complete())

  def test_is_round_complete_2(self):
    board = Board(
      tokens_by_cup=[
        0, 0, 0, 0, 0, 1, 0,
        0, 0, 0, 1, 0, 0, 0,
      ]
    )
    self.assertFalse(board.is_round_complete())

  def test_pass_turn_when_no_choices(self):
    board = Board(
      tokens_by_cup=[
        0, 0, 0, 0, 0, 0, 0,
        1, 2, 3, 4, 5, 6, 7,
      ],
      turn=1
    )
    board.pass_turn()

  def test_pass_turn_when_choices(self):
    board = Board(
      tokens_by_cup=[
        0, 0, 0, 0, 0, 0, 0,
        1, 2, 3, 4, 5, 6, 7,
      ],
      turn=2,
    )
    with self.assertRaises(ValueError):
      board.pass_turn()

  def test_play_1(self):
    board = Board(
      tokens_by_cup=[
        5, 5, 5, 5, 5, 5, 5,
        5, 5, 5, 5, 5, 5, 5,
      ],
      taken_tokens=[0, 0],
      turn=1,
    )
    board.play(0, "Test")
    self.assertEqual(board.tokens_by_cup, [
      2, 8, 8, 8, 0, 0, 1,
      7, 7, 7, 7, 0, 1, 7
    ])
    self.assertEqual(board.taken_tokens, [7, 0])

  def test_play_2(self):
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
    self.assertEqual(board.tokens_by_cup, [
      1, 2, 11, 11, 3, 0, 0,
      0, 10, 0, 1, 3, 0, 10
    ])
    self.assertEqual(board.taken_tokens, [11, 7])

  def test_play_3(self):
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
    self.assertEqual(reward, -100)
    self.assertEqual(board.tokens_by_cup, [
        1, 0, 1, 0, 15, 0, 0,
        3, 0, 3, 1, 0, -1, -1
    ])
    self.assertEqual(board.taken_tokens, [27, 19])

  def test_clear_empty(self):
    board = Board(
      tokens_by_cup=[
        0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0,
      ],
      taken_tokens=[45, 25]
    )
    board.clear()
    self.assertEqual(board.tokens_by_cup, [
      0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0,
    ])
    self.assertEqual(board.taken_tokens, [45, 25])

  def test_clear_partial(self):
    board = Board(
      tokens_by_cup=[
        0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 1,
      ],
      taken_tokens=[45, 24]
    )
    board.clear()
    self.assertEqual(board.tokens_by_cup, [
      0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0,
    ])
    self.assertEqual(board.taken_tokens, [45, 25])

  def test_prep_35_35(self):
    board = Board(
      tokens_by_cup=[
        0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0,
      ],
      taken_tokens=[35, 35]
    )
    board.prep()
    self.assertEqual(board.tokens_by_cup, [
      5, 5, 5, 5, 5, 5, 5,
      5, 5, 5, 5, 5, 5, 5
    ])
    self.assertEqual(board.taken_tokens, [0, 0])

  def test_prep_30_40(self):
    board = Board(
      tokens_by_cup=[
        0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0,
      ],
      taken_tokens=[30, 40],
    )
    board.prep()
    self.assertEqual(board.tokens_by_cup, [
      5, 5, 5, 5, 5, 5, -1,
      5, 5, 5, 5, 5, 5, 5
    ])
    self.assertEqual(board.taken_tokens, [0, 5])
