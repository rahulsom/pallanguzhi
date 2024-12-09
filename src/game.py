from board import Board
from player import Player


def play_game(board: Board, player1: Player, player2: Player):
  while not board.is_game_over():
    print(board.to_string(), end="")
    while not board.is_round_complete():
      if len(board.choices()) == 0:
        print("No valid choices for the current player. Passing turn")
        board.pass_turn()
      else:
        player = player1 if board.turn == 1 else player2
        player.play(board)
      print(board.to_string(), end="")
    board.clear()
    print("Clearing board")
    print(board.to_string(), end="")
    print()
    print()
    board.render()
    board.prep()
