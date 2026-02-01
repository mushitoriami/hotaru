# Claude Code Configuration

## Python Environment

- Use `python3.13` when running python commands
- Example: `python3.13 -m pip install ...`, `python3.13 script.py`

## Testing

- Use `tox` for running tests
- Run all tests: `tox`
- Run specific environment: `tox -e py313`, `tox -e lint`, `tox -e type`, `tox -e format`
