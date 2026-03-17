"""
Application settings, constants, and color palette.
"""

from pathlib import Path

# ==================== Application Info ====================
APP_TITLE = "Project Scaffold Builder"
APP_VERSION = "2.1"
CONFIG_FILENAME = ".project_scaffold_template.json"

# ==================== Default Paths ====================
DEFAULT_BASE_DIR = Path.home() / "Research_Code" / "02_learning_and_demos"
DEFAULT_PROJECT_NAME = "ai_code_practice"

# ==================== Window Settings ====================
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 820
WINDOW_MIN_WIDTH = 1000
WINDOW_MIN_HEIGHT = 700

# ==================== Font Settings ====================
FONT_FAMILY = "SF Pro Display"
FONT_FAMILY_MONO = "JetBrains Mono"
FONT_SIZE_TITLE = 18
FONT_SIZE_SECTION = 14
FONT_SIZE_NORMAL = 13
FONT_SIZE_MONO = 12
FONT_SIZE_SMALL = 11


# ==================== Color Palette ====================
class Colors:
    """Modern color palette for the application UI."""
    
    # Primary colors (Indigo)
    PRIMARY = "#6366f1"
    PRIMARY_HOVER = "#4f46e5"
    PRIMARY_LIGHT = "#818cf8"
    
    # Secondary colors (Emerald)
    SECONDARY = "#10b981"
    SECONDARY_HOVER = "#059669"
    
    # Neutral colors (Slate)
    BG_DARK = "#0f172a"           # Slate 900
    BG_DARK_SECONDARY = "#1e293b"  # Slate 800
    BG_LIGHT = "#f8fafc"          # Slate 50
    BG_LIGHT_SECONDARY = "#e2e8f0" # Slate 200
    
    # Text colors
    TEXT_DARK = "#f1f5f9"    # Slate 100 (for dark theme)
    TEXT_LIGHT = "#1e293b"   # Slate 800 (for light theme)
    TEXT_MUTED = "#94a3b8"   # Slate 400
    
    # Status colors
    SUCCESS = "#22c55e"  # Green 500
    WARNING = "#f59e0b"  # Amber 500
    ERROR = "#ef4444"    # Red 500
    
    # Border colors
    BORDER_DARK = "#334155"   # Slate 700
    BORDER_LIGHT = "#cbd5e1"  # Slate 300


# ==================== Default File Contents ====================
DEFAULT_GITIGNORE = """__pycache__/
*.pyc
.ipynb_checkpoints/
.venv/
venv/
env/
.DS_Store
Thumbs.db
results/
"""

DEFAULT_README = """# {project_name}

## Overview
A project scaffold created with Project Scaffold Builder.

## Structure
- src/: source code
- data/: raw and processed data
- results/: generated outputs
- docs/: documentation
- tests/: tests

## Quick start
1. Put your code in `src/`
2. Track changes with Git
3. Push to GitHub when ready
"""

DEFAULT_MAIN = '''def main():
    print("Hello from {project_name}!")


if __name__ == "__main__":
    main()
'''
