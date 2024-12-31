# Pallanguzhi

Pallanguzhi is a traditional mancala game played in South India.
This repo builds the game rules and a few bot players to play the game.

## Game Rules

There are 14 cups in the game.
Each player has 7 cups.

1. Fill each hole with 5 tokens.
2. The first player starts by picking up all the tokens in one hole from their side of the board.
  They then drop the tokens one by one in each hole in an anti-clockwise direction.
3. When there are no more tokens in hand, the player picks up all tokens in the next hole and continues distributing them around the board.
4. They continue until there are no more tokens in hand and they reach an empty hole.
5. When this happens, the player wins all tokens in the hole next to the empty one.
  If both holes are empty, they player does not win any tokens for that round.
6. The second player then takes their turn and follows steps 2-5.
7. The game continues until all tokens are taken from the board.
8. At any point in the game, if a cup has 4 tokens, the player on whose side it occurs can collect the 4 tokens.
10. The player with the greatest number of tokens at the end of the game wins.
11. You can continue playing additional rounds by setting the board with acquired tokens 5 per cup.
  You cannot have partial cups at the start of a new round.
  This repo assumes there are 12 rounds in a game.

## Usage

To train the AI

```shell
make train
```

To play the game, run this. It assumes player 1 is an AI and player 2 is a human.

```shell
make run
```

To adjust the players, you can change the `player1` and `player2`.
E.g.

```shell
ARGS="--player1 human --player2 ai:64" make run
```

The full list of choices for players are:

- `human`
- `ai:64`
- `random`
- `first`
- `emptiest`
