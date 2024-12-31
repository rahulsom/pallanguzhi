import os

import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque

from constants import CUPS_PER_USER
from player import Player

device = torch.device(
  "cuda" if torch.cuda.is_available() else
  "mps" if torch.backends.mps.is_available() else
  "cpu"
)


class DQN(nn.Module):
  def __init__(self, state_size, action_size):
    super(DQN, self).__init__()
    self.dqn = nn.Sequential(
      nn.Linear(state_size, CUPS_PER_USER * 2),
      nn.ReLU(),
      nn.Linear(CUPS_PER_USER * 2, CUPS_PER_USER * 2),
      nn.ReLU(),
      nn.Linear(CUPS_PER_USER * 2, action_size)
    ).to(device)

  def forward(self, x):
    return self.dqn(x)


class AIPlayer(Player):

  def __init__(self, depth: int = 32, epsilon: float = 1.0):
    super().__init__()
    self.state_size = (CUPS_PER_USER * 2 + 2)  # CUP STATE + TAKEN TOKENS
    self.action_size = 1
    self.memory = deque(maxlen=depth*depth)
    self.depth = depth
    self.gamma = 0.95
    self.epsilon = epsilon
    self.epsilon_min = 0.01
    self.epsilon_decay = 0.9999
    self.learning_rate = 0.0001
    self.model = DQN(self.state_size, self.action_size)
    self.target_model = DQN(self.state_size, self.action_size)
    if os.path.exists(f"build/model.{self.depth}.pth") and os.path.exists(f"build/target_model.{self.depth}.pth"):
      self.model.load_state_dict(torch.load(f"build/model.{self.depth}.pth", weights_only=True))
      self.target_model.load_state_dict(torch.load(f"build/target_model.{self.depth}.pth", weights_only=True))
      self.epsilon = self.epsilon_min
    self.update_target_model()
    self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
    self.criterion = nn.MSELoss()

  def __str__(self) -> str:
    return f"AIPlayer({self.depth})"

  def update_target_model(self) -> None:
    self.target_model.load_state_dict(self.model.state_dict())

  def remember(self, state, action, reward, next_state, done) -> None:
    self.memory.append((state, action, reward, next_state, done))

  def act(self, state, choices) -> int:
    self.epsilon = self.epsilon * self.epsilon_decay if self.epsilon > self.epsilon_min else self.epsilon_min
    if random.random() <= self.epsilon:
      return random.choice(choices)
    state = torch.Tensor(state).to(device).unsqueeze(0)
    act_values = self.model(state)
    choice_index = int(torch.argmax(act_values[-1]).item() * len(choices))
    return choices[choice_index]

  def optimize_model(self) -> None:
    if len(self.memory) < self.depth:
      return
    batch = random.sample(self.memory, self.depth)
    for state, action, reward, next_state, done in batch:
      state = torch.Tensor(state).to(device).unsqueeze(0)
      next_state = torch.Tensor(next_state).to(device).unsqueeze(0)
      target = reward
      if not done:
        target = reward + self.gamma * torch.max(self.target_model(next_state))
      target_f = self.model(state)
      target_f[0] = target
      self.optimizer.zero_grad()
      loss = self.criterion(self.model(state), target_f)
      loss.backward()
      self.optimizer.step()

  def play(self, board) -> None:
    state = board.tokens_by_cup + board.taken_tokens
    action = self.act(state, board.choices())
    if action not in board.choices():
      print(f"{action} -> ", end="")
      action = board.choices()[int(random.random() * len(board.choices()))]
    reward = board.play(action, "AI")
    next_state = board.tokens_by_cup + board.taken_tokens
    done = board.is_game_over()
    self.remember(state, action, reward, next_state, done)
    self.optimize_model()
    if done:
      self.update_target_model()
