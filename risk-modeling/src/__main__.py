"""Allow `python -m src` from the project root."""

from src.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
