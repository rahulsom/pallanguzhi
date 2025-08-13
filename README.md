# Pallanguzhi

Pallanguzhi is a traditional mancala game played in South India.
This repo builds the game rules and a few bot players to play the game.

## Docs

See the [GH pages](https://rahulsom.github.io/pallanguzhi/) for more details.

## Developer Notes

You need [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.

To train the AI

```shell
mkdir -p build
uv run src/train.py
```

To play the game, run this. It assumes player 1 is an AI and player 2 is a human.

```shell
uv run src/main.py
```

To adjust the players, you can change the `player1` and `player2`.
E.g.

```shell
uv run src/main.py -- --player1 human --player2 ai:64
```

The full list of choices for players are:

- `human`
- `ai:64`
- `random`
- `first`
- `emptiest`


To run the tests

```shell
uv run -m unittest discover -s src -p "test_*.py"
```

To run a demo

```shell
uv run src/demo.py
```
