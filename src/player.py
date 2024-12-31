from abc import ABC, abstractmethod
from board import Board


class Player(ABC):

  def __init__(self):
    super().__init__()


  @abstractmethod
  def play(self, board: Board) -> None:
    raise NotImplementedError

