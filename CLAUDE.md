# Claude Code 設定

## Python環境

- pythonコマンドを使用する際は `python3.13` を使用すること
- 例: `python3.13 -m pip install ...`, `python3.13 script.py`

## テスト

- テストの実行には `tox` を使用すること
- 全テスト実行: `tox`
- 特定の環境のみ: `tox -e py313`, `tox -e lint`, `tox -e type`, `tox -e format`
