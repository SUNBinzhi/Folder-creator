"""
Application entry point for Project Scaffold Builder.
"""

import sys

from .config import APP_TITLE, APP_VERSION
from .utils import ensure_customtkinter


def main():
    """Start the application."""
    ctk = ensure_customtkinter()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    from .ui.app import ScaffoldApp

    root = ctk.CTk()

    if sys.platform.startswith("darwin"):
        try:
            root.iconbitmap(default="")
        except Exception:
            pass

    root.title(f"{APP_TITLE} v{APP_VERSION}")
    app = ScaffoldApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
