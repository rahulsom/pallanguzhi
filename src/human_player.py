from player import Player


class HumanPlayer(Player):
  def play(self, board) -> None:
    choices = board.choices()
    print("Valid choices:", choices)
    board.render(force=True)
    choice = None
    while choice not in choices:
      try:
        choice = int(input("Enter your choice: "))
        if choice not in choices:
          print("Invalid choice. Please choose from the valid choices.")
      except ValueError:
        print("Invalid input. Please enter a number.")

    board.play(choice, "Human")
