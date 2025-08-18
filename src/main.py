import argparse

from ai_player import AIPlayer
from board import Board
from human_player import HumanPlayer
from simple_players import Player, RandomPlayer, FirstPitPlayer, EmptiestPitPlayer
from game import play_game


def build_parser():
  parser = argparse.ArgumentParser(prog='pallanguzhi', description='Game Engine for Pallanguzhi')
  choices = [
    "random",
    "ai:64",
    "human",
    "first",
    "emptiest"
  ]
  parser.add_argument('--player1', type=str, default='ai:64', help='Player 1 type', choices=choices)
  parser.add_argument('--player2', type=str, default='human', help='Player 2 type', choices=choices)
  return parser


def build_player(player_type: str) -> Player:
  if player_type == "random":
    return RandomPlayer()
  if player_type == "first":
    return FirstPitPlayer()
  if player_type == "emptiest":
    return EmptiestPitPlayer()
  if player_type == "human":
    return HumanPlayer()
  if player_type.startswith("ai:"):
    return AIPlayer(int(player_type[3:]))


if __name__ == '__main__':
  args = build_parser().parse_args()
  player1 = build_player(args.player1)
  player2 = build_player(args.player2)
  print(args)

  board = Board(verbose=True)
  play_game(board, player1, player2)

  print("Player 1 wins" if board.taken_tokens[0] > board.taken_tokens[1] else "Player 2 wins")
  print()
