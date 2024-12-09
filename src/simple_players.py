from random import random
from player import Player


class FirstPitPlayer(Player):
  def play(self, board):
    print("First pit player chose pit", board.choices()[0])
    board.play(board.choices()[0])


class EmptiestPitPlayer(Player):
  def play(self, board):
    print("Emptiest pit player chose pit", min(board.choices(), key=lambda x: board.tokens_by_cup[x]))
    board.play(min(board.choices(), key=lambda x: board.tokens_by_cup[x]))


class RandomPlayer(Player):
  def play(self, board):
    random_pit = board.choices()[int(random() * len(board.choices()))]
    print("Random player chose pit", random_pit)
    board.play(random_pit)
