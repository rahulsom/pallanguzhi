import copy
import re

from texttable import Texttable

from constants import *


def rstr(s: int) -> str:
  return f"{s:2d}"


class Board:

  def __init__(
      self,
      tokens_by_cup=None,
      taken_tokens=None,
      turn=1,
      visualize=False,
      verbose=False
  ):
    self.tokens_by_cup = tokens_by_cup if tokens_by_cup is not None else [TOKENS_PER_CUP] * CUPS_PER_USER * 2
    self.taken_tokens = taken_tokens if taken_tokens is not None else [TOKENS_PER_CUP * CUPS_PER_USER] * 2
    self.turn = turn
    self.visualize = visualize
    self.verbose = verbose

  def describe(self) -> str:
    return "".join([
      self.player_to_string(1),
      self.player_to_string(2),
    ])

  def to_string(self):
    tbc_str = ("[ "
               + ",".join(map(rstr, self.tokens_by_cup[0:CUPS_PER_USER]))
               + ",  "
               + ",".join(map(rstr, self.tokens_by_cup[CUPS_PER_USER:2 * CUPS_PER_USER]))
               + " ]")
    tt_str = "[" + ",".join(map(rstr, self.taken_tokens)) + "]"
    return f"Board({tbc_str}, {tt_str}, {self.turn})"

  def player_to_string(self, player: int) -> str:
    fmt = "{taken_tokens:4d} {active} P{player}: {cups}"
    return fmt.format(
      active="*" if self.turn == player else " ",
      taken_tokens=self.taken_tokens[player - 1],
      player=player,
      cups=self.tokens_by_cup[CUPS_PER_USER * (player - 1):CUPS_PER_USER * player]
    ).ljust(20 + CUPS_PER_USER * 3)

  def choices(self) -> list[int]:
    choices = [i for i, x in enumerate(self.tokens_by_cup) if x > 0]
    return [i for i in choices if
            (self.turn == 1 and i < CUPS_PER_USER) or (self.turn == 2 and i >= CUPS_PER_USER)]

  def is_game_over(self) -> bool:
    return (
        (
            max(self.tokens_by_cup[0:CUPS_PER_USER]) == -1 or
            max(self.tokens_by_cup[CUPS_PER_USER:2 * CUPS_PER_USER]) == -1
        ) or
        (
            max(self.taken_tokens) < 5
        )
    )

  def is_round_complete(self) -> bool:
    return sum(self.tokens_by_cup) <= 1

  def pass_turn(self) -> None:
    if len(self.choices()) == 0:
      if self.verbose:
        print(f"{self.to_string()}.pass_turn()")
      self.turn = 1 if self.turn == 2 else 2
    else:
      raise ValueError("There are still valid choices for the current player")

  def render(self, old: list[int] = None, from_cup: int = None, force: bool = False) -> None:
    if old is None:
      old = self.tokens_by_cup
    if self.visualize or force:
      tbl = [[' '] * (CUPS_PER_USER - 1) for _ in range(4)]
      for i in range(CUPS_PER_USER * 2):
        if i in {CUPS_PER_USER - 1, CUPS_PER_USER * 2 - 1}:
          y, x = 2, CUPS_PER_USER - 2 if i == CUPS_PER_USER - 1 else 0
        else:
          y, x = (3, i) if i < CUPS_PER_USER - 1 else (1, 2 * CUPS_PER_USER - i - 2)

        marker = " "
        if old[i] < self.tokens_by_cup[i]:
          marker = "+"
        if i == from_cup:
          marker = "*"

        if self.tokens_by_cup[i] == -1:
          num_to_str = " X"
        else:
          num_to_str = rstr(self.tokens_by_cup[i])

        tbl[y][x] = f"{marker} {num_to_str}"

      tbl[2][1] = f"{'> ' if self.turn == 2 else '  '}{rstr(self.taken_tokens[1])}"
      tbl[2][CUPS_PER_USER - 3] = f"{'> ' if self.turn == 1 else '  '}{rstr(self.taken_tokens[0])}"

      table = Texttable()
      table.set_cols_align(['r'] * (CUPS_PER_USER - 1))
      table.set_cols_width([4] * (CUPS_PER_USER - 1))
      table.add_rows(tbl)
      tabletext = table.draw().replace('=', '-') + "\n"
      lines = tabletext.split('\n')[2:]
      lines[2] = re.sub('\\+------\\+------\\+$', '+======+======+', lines[2])
      lines[4] = re.sub('^\\+------\\+------\\+', '+======+======+', lines[4])
      lines[3] = re.sub('\\|( +)\\|( +)\\|', '║\\1 \\2║', lines[3])
      print('\n'.join(lines))

  def play(self, cup: int, player_type) -> int:
    """

    :rtype: int reward
    """
    backup_board = copy.deepcopy(self)
    score_diff_before = self.taken_tokens[0] - self.taken_tokens[1]

    if cup not in self.choices():
      raise ValueError("Invalid choice")

    if self.verbose:
      print(self.to_string(), end="")

    choice_message = f".play({cup:2d}, '{player_type}') #"
    if self.verbose:
      print(choice_message, end="")
    moves = 0
    while True:
      from_cup = cup
      shells = self.tokens_by_cup[cup]
      self.tokens_by_cup[cup] = 0
      moves += 1
      if moves > MAX_MOVES_PER_TURN:
        # set the board back to the original state
        self.tokens_by_cup = backup_board.tokens_by_cup
        self.taken_tokens = backup_board.taken_tokens
        self.turn = backup_board.turn
        return MAX_MOVES_PENALTY
      if shells == 0:
        cup = (cup + 1) % (CUPS_PER_USER * 2)
        while self.tokens_by_cup[cup] < 0:
          cup = (cup + 1) % (CUPS_PER_USER * 2)
        shells = self.tokens_by_cup[cup]
        self.taken_tokens[self.turn - 1] += shells
        self.tokens_by_cup[cup] = 0
        break
      old_tokens = self.tokens_by_cup.copy()
      while shells > 0:
        cup = (cup + 1) % (CUPS_PER_USER * 2)
        while self.tokens_by_cup[cup] < 0:
          cup = (cup + 1) % (CUPS_PER_USER * 2)
        if self.tokens_by_cup[cup] < 0:
          continue
        self.tokens_by_cup[cup] += 1
        shells -= 1
        if self.tokens_by_cup[cup] == QUICK_DRAW_COUNT:
          self.taken_tokens[int(cup / CUPS_PER_USER)] += self.tokens_by_cup[cup]
          self.tokens_by_cup[cup] = 0
      self.render(old_tokens, from_cup)

      cup = (cup + 1) % (CUPS_PER_USER * 2)
      while self.tokens_by_cup[cup] < 0:
        cup = (cup + 1) % (CUPS_PER_USER * 2)

    score_diff_after = self.taken_tokens[0] - self.taken_tokens[1]
    reward = (score_diff_after - score_diff_before) * (1 if self.turn == 1 else -1)
    if self.verbose:
      print(f" for reward {reward:2d} in {moves:3d} moves")
    self.turn = 1 if self.turn == 2 else 2
    return reward

  def clear(self) -> None:
    if self.verbose:
      print(f"{self.to_string()}.clear()\n")
    for i in range(0, CUPS_PER_USER):
      if self.tokens_by_cup[i] > 0:
        self.taken_tokens[0] += self.tokens_by_cup[i]
        self.tokens_by_cup[i] = 0
    for i in range(CUPS_PER_USER, 2 * CUPS_PER_USER):
      if self.tokens_by_cup[i] > 0:
        self.taken_tokens[1] += self.tokens_by_cup[i]
        self.tokens_by_cup[i] = 0

  def prep(self) -> None:
    if self.verbose:
      print(self.to_string(), end="")
    for i in range(0, CUPS_PER_USER):
      if self.taken_tokens[0] >= TOKENS_PER_CUP:
        self.tokens_by_cup[i] = TOKENS_PER_CUP
        self.taken_tokens[0] -= TOKENS_PER_CUP
      else:
        self.tokens_by_cup[i] = -1
    for i in range(CUPS_PER_USER, 2 * CUPS_PER_USER):
      if self.taken_tokens[1] >= TOKENS_PER_CUP:
        self.tokens_by_cup[i] = TOKENS_PER_CUP
        self.taken_tokens[1] -= TOKENS_PER_CUP
      else:
        self.tokens_by_cup[i] = -1
    if self.verbose:
      print(".prep()")
