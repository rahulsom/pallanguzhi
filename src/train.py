import time

import torch

from ai_player import AIPlayer
from board import Board
from game import play_game
from simple_players import RandomPlayer


def train(p: AIPlayer) -> None:
  for i in range(25):
    board = Board(verbose=False)
    start_time = time.time()
    play_game(board, p, p, prefix=f"[{p}]  Game {3 * i + 1:2d}")
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    play_game(board, RandomPlayer(), p, prefix=f"[{p}]  Game {3 * i + 2:2d}")
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    play_game(board, p, RandomPlayer(), prefix=f"[{p}]  Game {3 * i + 3:2d}")
    print("--- %s seconds ---" % (time.time() - start_time))

  torch.save(p.model.state_dict(), f"build/model.{p.depth}.pth")
  torch.save(p.target_model.state_dict(), f"build/target_model.{p.depth}.pth")


if __name__ == '__main__':
  all_players = [AIPlayer(128)]

  for p1 in all_players:
    train(p1)
