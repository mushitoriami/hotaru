# hotaru
AI for Ludo.

Rules are based on the Ludo implementation used on [PlayOK](https://playok.com/en/ludo).

## Installation
```
uv tool install git+https://github.com/mushitoriami/hotaru.git
```

## Usage
Start the interactive CLI:
```
hotaru
```

By default all four seats (0-3) participate. To play with fewer than four (minimum two), pass `--players` as a comma-separated list of seat indices:
```
hotaru --players 0,2
```

Available commands at the `>` prompt:
- `move <piece>` — move the given piece (1-4)
- `pass` — pass the turn when no move is available
- `dice <n>` — set the dice roll (1-6)
- `eval` — show the evaluator's score for each legal move
- `auto` — let the evaluator pick and play a move
- `new` — start a new game
- `undo` — undo the last move
- `quit` / `exit` — exit the CLI

## Evaluation data
`hotaru` uses `HotaruEvaluator`, a trained evaluator, when `params_midgame.dat` is present in the current directory (`params_endgame.dat` additionally enables endgame lookups). Without these files, it falls back to `RandomEvaluator`.

Both files are published as assets on the [GitHub Releases](https://github.com/mushitoriami/hotaru/releases) page (e.g. v0.1.2). Download them and place them in the directory you run `hotaru` from.
