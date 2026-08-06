# hotaru
AI for Ludo.

Rules are based on the Ludo implementation used on [PlayOK](https://playok.com/en/ludo).

## Installation
```
git clone https://github.com/mushitoriami/hotaru.git
cd hotaru
uv sync
```

## Usage
Start the interactive CLI:
```
uv run hotaru
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
