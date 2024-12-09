from typing import Final

from texttable import Texttable

CUPS_PER_USER: Final[int] = 7
TOKENS_PER_CUP: Final[int] = 5


class Board:
  def __init__(self):
    self.tokens_by_cup = [TOKENS_PER_CUP] * CUPS_PER_USER * 2
    self.taken_tokens = [0, 0]
    self.turn = 1
    self.visualize = False

  def to_string(self) -> str:
    # board_total = sum([x for i, x in enumerate(self.tokens_by_cup) if x > 0])
    return "".join([
      self.player_to_string(1),
      self.player_to_string(2),
      # str(sum(self.taken_tokens) + board_total) + "    "
    ])

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
    return max(self.tokens_by_cup[0:CUPS_PER_USER]) == -1 or max(self.tokens_by_cup[CUPS_PER_USER:2*CUPS_PER_USER]) == -1

  def is_round_complete(self) -> bool:
    return sum(self.tokens_by_cup) <= 1

  def pass_turn(self):
    if len(self.choices()) == 0:
      self.turn = 1 if self.turn == 2 else 2
    else:
      raise ValueError("There are still valid choices for the current player")

  def render(self, old:list[int] = None):
    if old is None:
      old = self.tokens_by_cup
    if self.visualize:
      tbl = [[' '] * (CUPS_PER_USER - 1) for _ in range(4)]
      for i in range(CUPS_PER_USER * 2):
        if i in {CUPS_PER_USER - 1, CUPS_PER_USER * 2 - 1}:
          y, x = 2, CUPS_PER_USER - 2 if i == CUPS_PER_USER - 1 else 0
        else:
          y, x = (3, i) if i < CUPS_PER_USER - 1 else (1, 2 * CUPS_PER_USER - i - 2)
        curr = "*" if old[i] < self.tokens_by_cup[i] else " "
        tbl[y][x] = f"{curr} {self.tokens_by_cup[i]}"

      table = Texttable()
      table.set_cols_align(['r'] * (CUPS_PER_USER - 1))
      table.set_cols_width([4] * (CUPS_PER_USER - 1))
      table.add_rows(tbl)
      tabletext = table.draw() + "\n"
      lines = tabletext.split('\n')[2:]
      print('\n'.join(lines))

  def play(self, num: int) -> int:

    score_diff = self.taken_tokens[0] - self.taken_tokens[1]

    if num not in self.choices():
      raise ValueError("Invalid choice")

    while True:
      shells = self.tokens_by_cup[num]
      # print(f"Player {self.turn} chose cup {num} with {shells} shells")
      self.tokens_by_cup[num] = 0
      if shells == 0:
        num = (num + 1) % (CUPS_PER_USER * 2)
        while self.tokens_by_cup[num] < 0:
          num = (num + 1) % (CUPS_PER_USER * 2)
        shells = self.tokens_by_cup[num]
        self.taken_tokens[self.turn - 1] += shells
        self.tokens_by_cup[num] = 0
        break
      old_tokens = self.tokens_by_cup.copy()
      while shells > 0:
        num = (num + 1) % (CUPS_PER_USER * 2)
        while self.tokens_by_cup[num] < 0:
          num = (num + 1) % (CUPS_PER_USER * 2)
        if self.tokens_by_cup[num] < 0:
          continue
        self.tokens_by_cup[num] += 1
        shells -= 1
        if self.tokens_by_cup[num] == 4:
          self.taken_tokens[int(num / CUPS_PER_USER)] += 4
          self.tokens_by_cup[num] = 0
      self.render(old_tokens)

      num = (num + 1) % (CUPS_PER_USER * 2)
      while self.tokens_by_cup[num] < 0:
        num = (num + 1) % (CUPS_PER_USER * 2)

    self.turn = 1 if self.turn == 2 else 2

    score_diff_after = self.taken_tokens[1] - self.taken_tokens[0]
    reward = score_diff_after - score_diff * (1 if self.turn == 2 else -1)
    return reward

  def clear(self):
    for i in range(0 , CUPS_PER_USER):
      if self.tokens_by_cup[i] > 0:
        self.taken_tokens[0] += self.tokens_by_cup[i]
        self.tokens_by_cup[i] = 0
    for i in range(CUPS_PER_USER, 2 * CUPS_PER_USER):
      if self.tokens_by_cup[i] > 0:
        self.taken_tokens[1] += self.tokens_by_cup[i]
        self.tokens_by_cup[i] = 0

  def prep(self):
    for i in range(0 , CUPS_PER_USER):
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
