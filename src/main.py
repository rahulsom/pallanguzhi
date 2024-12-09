import argparse

from board import Board
from human_player import HumanPlayer
from simple_players import *
from game import play_game

parser = argparse.ArgumentParser(prog='pallanguzhi', description='Game Engine for Pallanguzhi')
choices = [
  "random",
  "human",
  "random",
  "first",
  "emptiest"
]
parser.add_argument('--player1', type=str, default='random', help='Player 1 type', choices=choices)
parser.add_argument('--player2', type=str, default='first', help='Player 2 type', choices=choices)

def build_player(type: str, number: int):
  if type == "random":
    return RandomPlayer(number)
  if type == "first":
    return FirstPitPlayer(number)
  if type == "emptiest":
    return EmptiestPitPlayer(number)
  if type == "human":
    return HumanPlayer(number)


if __name__ == '__main__':
  args = parser.parse_args()
  player1 = build_player(args.player1, 1)
  player2 = build_player(args.player2, 2)
  print(args)

  board = Board()
  play_game(board, player1, player2)

  print("Player 1 wins" if board.taken_tokens[0] > board.taken_tokens[1] else "Player 2 wins")
