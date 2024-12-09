from abc import ABC, abstractmethod
from board import Board


class Player(ABC):

  def __init__(self, player_number):
    super().__init__()
    self.player_number = player_number


  @abstractmethod
  def play(self, board: Board):
    pass
