"""Launch the MyBot Attack Generator desktop app.

Run this file from the attack-generator folder:

    python main.py

The window opens immediately with native PySide6 widgets (dark theme).
"""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from attackgen.ui_main import main as run_app
    run_app()


if __name__ == "__main__":
    main()