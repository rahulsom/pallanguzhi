# Pallanguzhi

Pallanguzhi is a traditional mancala game played in South India.
This repo builds the game rules and a few bot players to play the game.

## Docs

See the [GH pages](https://rahulsom.github.io/pallanguzhi/) for more details.

## Developer Notes

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
