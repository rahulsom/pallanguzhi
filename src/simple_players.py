from random import random
from player import Player


class FirstPitPlayer(Player):
  def play(self, board) -> None:
    board.play(board.choices()[0], "First Pit")

  def __str__(self):
    return "FirstPitPlayer"


class EmptiestPitPlayer(Player):
  def play(self, board) -> None:
    board.play(min(board.choices(), key=lambda x: board.tokens_by_cup[x]), "Emptiest Pit")

  def __str__(self):
    return "EmptiestPitPlayer"


class RandomPlayer(Player):
  def play(self, board) -> None:
    random_pit = board.choices()[int(random() * len(board.choices()))]
    board.play(random_pit, "Random")

  def __str__(self):
    return "RandomPlayer"