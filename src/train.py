import torch

from ai_player import AIPlayer
from board import Board
from game import play_game
from simple_players import RandomPlayer
import time

def train(p1: AIPlayer) -> None:
  for i in range(25):
    board = Board(verbose=False)
    start_time = time.time()
    play_game(board, p1, p1, prefix = f"[{p1}]  Game {3*i+1:2d}")
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    play_game(board, RandomPlayer(), p1, prefix = f"[{p1}]  Game {3*i+2:2d}")
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    play_game(board, p1, RandomPlayer(), prefix = f"[{p1}]  Game {3*i+3:2d}")
    print("--- %s seconds ---" % (time.time() - start_time))

  torch.save(p1.model.state_dict(), f"build/model.{p1.depth}.pth")
  torch.save(p1.target_model.state_dict(), f"build/target_model.{p1.depth}.pth")


if __name__ == '__main__':
  all_players = [AIPlayer(64)]

  for p1 in all_players:
    train(p1)