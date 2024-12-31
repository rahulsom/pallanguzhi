from ai_player import AIPlayer
from board import Board
from game import play_game
from simple_players import RandomPlayer


def demo_player(player: AIPlayer) -> None:
  ai_wins = 0
  random_wins = 0
  for i in range(5):
    board = Board(verbose=False)
    winner = play_game(board, player, RandomPlayer(), prefix=f"{player} - Game {2*i+1:2d}")
    if winner == 1:
      ai_wins += 1
    else:
      random_wins += 1
    winner = play_game(board, RandomPlayer(), player, prefix=f"{player} - Game {2*i+2:2d}")
    if winner == 2:
      ai_wins += 1
    else:
      random_wins += 1
  print(f"{player} wins {ai_wins} times, RandomPlayer wins {random_wins} times.")

if __name__ == '__main__':
  demo_player(AIPlayer(64, epsilon=0.01))