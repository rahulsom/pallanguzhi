from board import Board
from player import Player


def play_game(
  board: Board,
  player1: Player,
  player2: Player,
  prefix: str = "",
  max_rounds:int = 12
) -> int:
  rounds = 0
  while not board.is_game_over():
    board.prep()
    while not board.is_round_complete():
      if len(board.choices()) == 0:
        board.pass_turn()
      else:
        player = player1 if board.turn == 1 else player2
        player.play(board)

    board.clear()
    board.render()
    rounds += 1
    if rounds > max_rounds:
      break
  print(f"{prefix} Game over in {rounds-1:4d} rounds. ", end="")

  if board.taken_tokens[0] > board.taken_tokens[1]:
    winner = 1
    result = f"Player 1 ({player1}) wins"
  else:
    winner = 2
    result = f"Player 2 ({player2}) wins"

  print(f"{result} {board.taken_tokens[0]} - {board.taken_tokens[1]}")
  return winner
