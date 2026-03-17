"""
Project Scaffold Builder - Modern UI Edition
A tool for quickly creating project folder structures with customizable templates.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Optional

try:
    import customtkinter as ctk
    from customtkinter import CTkFont
except ImportError:
    print("CustomTkinter not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
    import customtkinter as ctk
    from customtkinter import CTkFont

from tkinter import filedialog, messagebox
import tkinter as tk

# ==================== Configuration ====================
APP_TITLE = "Project Scaffold Builder"
APP_VERSION = "2.0"

# Modern color palette
class Colors:
    # Primary colors
    PRIMARY = "#6366f1"       # Indigo
    PRIMARY_HOVER = "#4f46e5"
    PRIMARY_LIGHT = "#818cf8"
    
    # Secondary colors
    SECONDARY = "#10b981"     # Emerald
    SECONDARY_HOVER = "#059669"
    
    # Neutral colors
    BG_DARK = "#0f172a"       # Slate 900
    BG_DARK_SECONDARY = "#1e293b"  # Slate 800
    BG_LIGHT = "#f8fafc"      # Slate 50
    BG_LIGHT_SECONDARY = "#e2e8f0"  # Slate 200
    
    # Text colors
    TEXT_DARK = "#f1f5f9"     # Slate 100
    TEXT_LIGHT = "#1e293b"    # Slate 800
    TEXT_MUTED = "#94a3b8"    # Slate 400
    
    # Status colors
    SUCCESS = "#22c55e"
    WARNING = "#f59e0b"
    ERROR = "#ef4444"
    
    # Border colors
    BORDER_DARK = "#334155"   # Slate 700
    BORDER_LIGHT = "#cbd5e1"  # Slate 300


# Default templates
DEFAULT_STRUCTURE = """# One item per line. Indentation defines nesting.
# Folder names may optionally end with '/'.
# Files are lines without a trailing '/'.
README.md
.gitignore
requirements.txt
src/
  main.py
  utils/
data/
  raw/
  processed/
results/
  figures/
  tables/
docs/
tests/
notes.md
"""

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

CONFIG_FILENAME = ".project_scaffold_template.json"


# ==================== Tooltip Widget ====================
class ModernTooltip:
    """Modern-styled tooltip that appears on hover."""
    
    def __init__(self, widget, text: str, delay: int = 500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tipwindow: Optional[tk.Toplevel] = None
        self.scheduled_id: Optional[str] = None
        
        widget.bind("<Enter>", self._schedule_show)
        widget.bind("<Leave>", self._hide)
        widget.bind("<ButtonPress>", self._hide)

    def _schedule_show(self, event=None):
        self._cancel_schedule()
        self.scheduled_id = self.widget.after(self.delay, self._show)

    def _cancel_schedule(self):
        if self.scheduled_id:
            self.widget.after_cancel(self.scheduled_id)
            self.scheduled_id = None

    def _show(self, event=None):
        if self.tipwindow or not self.text:
            return
            
        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_attributes("-topmost", True)
        
        # Modern tooltip styling
        frame = tk.Frame(
            tw,
            background=Colors.BG_DARK_SECONDARY,
            highlightbackground=Colors.BORDER_DARK,
            highlightthickness=1,
        )
        frame.pack()
        
        label = tk.Label(
            frame,
            text=self.text,
            justify=tk.LEFT,
            background=Colors.BG_DARK_SECONDARY,
            foreground=Colors.TEXT_DARK,
            font=("SF Pro Display", 11),
            padx=10,
            pady=6,
            wraplength=280,
        )
        label.pack()
        
        tw.update_idletasks()
        tw_width = tw.winfo_width()
        x = x - tw_width // 2
        tw.wm_geometry(f"+{x}+{y}")

    def _hide(self, event=None):
        self._cancel_schedule()
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None


# ==================== Main Application ====================
class ScaffoldApp:
    """Main application class with modern CustomTkinter UI."""
    
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.root.title(f"{APP_TITLE} v{APP_VERSION}")
        self.root.geometry("1280x820")
        self.root.minsize(1000, 700)
        
        # Set appearance mode and default color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configure fonts
        self.font_title = CTkFont(family="SF Pro Display", size=18, weight="bold")
        self.font_section = CTkFont(family="SF Pro Display", size=14, weight="bold")
        self.font_normal = CTkFont(family="SF Pro Display", size=13)
        self.font_mono = CTkFont(family="JetBrains Mono", size=12)
        self.font_small = CTkFont(family="SF Pro Display", size=11)
        
        # Variables
        self.base_dir_var = ctk.StringVar(value=str(Path.home() / "Research_Code" / "02_learning_and_demos"))
        self.project_name_var = ctk.StringVar(value="ai_code_practice")
        self.init_git_var = ctk.BooleanVar(value=False)
        self.create_readme_var = ctk.BooleanVar(value=True)
        self.create_gitignore_var = ctk.BooleanVar(value=True)
        self.create_requirements_var = ctk.BooleanVar(value=False)
        self.open_after_create_var = ctk.BooleanVar(value=True)
        
        self._build_ui()
        self.structure_text.insert("1.0", DEFAULT_STRUCTURE)
        self.update_preview()
    
    def _build_ui(self):
        """Build the modern UI layout."""
        # Main container with gradient effect simulation
        self.root.configure(fg_color=Colors.BG_DARK)
        
        # Create main frame with padding
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=0, minsize=320)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # ===== Left Panel (Settings) =====
        left_panel = ctk.CTkFrame(main_frame, fg_color=Colors.BG_DARK_SECONDARY, corner_radius=16)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        left_panel.grid_columnconfigure(0, weight=1)
        
        # Header with icon
        header_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            header_frame, 
            text="⚙️ Project Settings",
            font=self.font_title,
            text_color=Colors.TEXT_DARK
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header_frame,
            text="Configure your new project",
            font=self.font_small,
            text_color=Colors.TEXT_MUTED
        ).pack(anchor="w", pady=(4, 0))
        
        # Separator
        ctk.CTkFrame(left_panel, height=1, fg_color=Colors.BORDER_DARK).pack(fill="x", padx=20, pady=10)
        
        # Settings content
        settings_frame = ctk.CTkScrollableFrame(
            left_panel, 
            fg_color="transparent",
            scrollbar_button_color=Colors.BORDER_DARK,
            scrollbar_button_hover_color=Colors.PRIMARY_LIGHT
        )
        settings_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Base location
        self._create_input_group(
            settings_frame,
            "📁 Base Location",
            self.base_dir_var,
            with_browse=True
        )
        
        # Project name
        self._create_input_group(
            settings_frame,
            "📝 Project Name",
            self.project_name_var,
            on_change=self.update_preview
        )
        
        # Options section
        options_label = ctk.CTkLabel(
            settings_frame,
            text="🔧 Options",
            font=self.font_section,
            text_color=Colors.TEXT_DARK
        )
        options_label.pack(anchor="w", pady=(20, 12))
        
        options = [
            ("Create README.md content", self.create_readme_var, "Fills README.md with a starter template"),
            ("Create .gitignore content", self.create_gitignore_var, "Adds Python/research defaults to .gitignore"),
            ("Create requirements.txt", self.create_requirements_var, "Adds a placeholder to requirements.txt"),
            ("Initialize Git repository", self.init_git_var, "Runs git init in the new project folder"),
            ("Open folder after creation", self.open_after_create_var, "Opens the folder in Finder/Explorer"),
        ]
        
        for text, var, tooltip in options:
            self._create_checkbox(settings_frame, text, var, tooltip)
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        # Secondary buttons row
        secondary_row = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        secondary_row.pack(fill="x", pady=(0, 10))
        secondary_row.grid_columnconfigure((0, 1, 2), weight=1)
        
        ctk.CTkButton(
            secondary_row,
            text="Reset",
            width=80,
            height=36,
            corner_radius=8,
            fg_color="transparent",
            border_width=1,
            border_color=Colors.BORDER_DARK,
            hover_color=Colors.BG_DARK,
            font=self.font_small,
            command=self.reset_defaults
        ).grid(row=0, column=0, sticky="ew", padx=(0, 4))
        
        ctk.CTkButton(
            secondary_row,
            text="Save",
            width=80,
            height=36,
            corner_radius=8,
            fg_color="transparent",
            border_width=1,
            border_color=Colors.BORDER_DARK,
            hover_color=Colors.BG_DARK,
            font=self.font_small,
            command=self.save_template
        ).grid(row=0, column=1, sticky="ew", padx=4)
        
        ctk.CTkButton(
            secondary_row,
            text="Load",
            width=80,
            height=36,
            corner_radius=8,
            fg_color="transparent",
            border_width=1,
            border_color=Colors.BORDER_DARK,
            hover_color=Colors.BG_DARK,
            font=self.font_small,
            command=self.load_template
        ).grid(row=0, column=2, sticky="ew", padx=(4, 0))
        
        # Primary create button
        create_btn = ctk.CTkButton(
            buttons_frame,
            text="✨ Create Project",
            height=48,
            corner_radius=12,
            fg_color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_HOVER,
            font=self.font_section,
            command=self.create_project
        )
        create_btn.pack(fill="x")
        ModernTooltip(create_btn, "Create the project with the configured structure")
        
        # Theme toggle at bottom
        theme_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        theme_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(
            theme_frame,
            text="Theme:",
            font=self.font_small,
            text_color=Colors.TEXT_MUTED
        ).pack(side="left")
        
        self.theme_switch = ctk.CTkSwitch(
            theme_frame,
            text="Dark Mode",
            font=self.font_small,
            command=self._toggle_theme,
            onvalue=True,
            offvalue=False,
            progress_color=Colors.PRIMARY
        )
        self.theme_switch.pack(side="left", padx=(8, 0))
        self.theme_switch.select()
        
        # ===== Right Panel (Editor & Preview) =====
        right_panel = ctk.CTkFrame(main_frame, fg_color="transparent")
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=1)
        right_panel.grid_rowconfigure(3, weight=1)
        
        # Structure editor section
        structure_header = ctk.CTkFrame(right_panel, fg_color="transparent")
        structure_header.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        
        ctk.CTkLabel(
            structure_header,
            text="📂 Editable Structure",
            font=self.font_section,
            text_color=Colors.TEXT_DARK
        ).pack(side="left")
        
        ctk.CTkLabel(
            structure_header,
            text="Use 2-space indentation for nesting",
            font=self.font_small,
            text_color=Colors.TEXT_MUTED
        ).pack(side="right")
        
        structure_frame = ctk.CTkFrame(right_panel, fg_color=Colors.BG_DARK_SECONDARY, corner_radius=12)
        structure_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 12))
        structure_frame.grid_columnconfigure(0, weight=1)
        structure_frame.grid_rowconfigure(0, weight=1)
        
        self.structure_text = ctk.CTkTextbox(
            structure_frame,
            wrap="none",
            font=self.font_mono,
            fg_color=Colors.BG_DARK,
            text_color=Colors.TEXT_DARK,
            border_width=0,
            corner_radius=8,
            scrollbar_button_color=Colors.BORDER_DARK,
            scrollbar_button_hover_color=Colors.PRIMARY_LIGHT
        )
        self.structure_text.pack(fill="both", expand=True, padx=8, pady=8)
        self.structure_text.bind("<KeyRelease>", lambda e: self.update_preview())
        self.structure_text.bind("<FocusOut>", lambda e: self.update_preview())
        
        # Preview section
        preview_header = ctk.CTkFrame(right_panel, fg_color="transparent")
        preview_header.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        
        ctk.CTkLabel(
            preview_header,
            text="👁️ Preview",
            font=self.font_section,
            text_color=Colors.TEXT_DARK
        ).pack(side="left")
        
        self.status_label = ctk.CTkLabel(
            preview_header,
            text="Ready",
            font=self.font_small,
            text_color=Colors.SUCCESS
        )
        self.status_label.pack(side="right")
        
        preview_frame = ctk.CTkFrame(right_panel, fg_color=Colors.BG_DARK_SECONDARY, corner_radius=12)
        preview_frame.grid(row=3, column=0, sticky="nsew")
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_frame.grid_rowconfigure(0, weight=1)
        
        self.preview_text = ctk.CTkTextbox(
            preview_frame,
            wrap="none",
            font=self.font_mono,
            fg_color=Colors.BG_DARK,
            text_color=Colors.PRIMARY_LIGHT,
            border_width=0,
            corner_radius=8,
            scrollbar_button_color=Colors.BORDER_DARK,
            scrollbar_button_hover_color=Colors.PRIMARY_LIGHT
        )
        self.preview_text.pack(fill="both", expand=True, padx=8, pady=8)
        self.preview_text.configure(state="disabled")
    
    def _create_input_group(self, parent, label: str, variable, with_browse: bool = False, on_change=None):
        """Create a labeled input group with optional browse button."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=(0, 16))
        
        ctk.CTkLabel(
            frame,
            text=label,
            font=self.font_section,
            text_color=Colors.TEXT_DARK
        ).pack(anchor="w", pady=(0, 8))
        
        if with_browse:
            input_row = ctk.CTkFrame(frame, fg_color="transparent")
            input_row.pack(fill="x")
            input_row.grid_columnconfigure(0, weight=1)
            
            entry = ctk.CTkEntry(
                input_row,
                textvariable=variable,
                height=40,
                corner_radius=8,
                border_width=1,
                border_color=Colors.BORDER_DARK,
                fg_color=Colors.BG_DARK,
                text_color=Colors.TEXT_DARK,
                font=self.font_normal
            )
            entry.grid(row=0, column=0, sticky="ew")
            
            browse_btn = ctk.CTkButton(
                input_row,
                text="📂",
                width=40,
                height=40,
                corner_radius=8,
                fg_color=Colors.BG_DARK,
                hover_color=Colors.PRIMARY,
                border_width=1,
                border_color=Colors.BORDER_DARK,
                command=self.choose_base_dir
            )
            browse_btn.grid(row=0, column=1, padx=(8, 0))
            ModernTooltip(browse_btn, "Browse for folder")
        else:
            entry = ctk.CTkEntry(
                frame,
                textvariable=variable,
                height=40,
                corner_radius=8,
                border_width=1,
                border_color=Colors.BORDER_DARK,
                fg_color=Colors.BG_DARK,
                text_color=Colors.TEXT_DARK,
                font=self.font_normal
            )
            entry.pack(fill="x")
            
            if on_change:
                entry.bind("<KeyRelease>", lambda e: on_change())
    
    def _create_checkbox(self, parent, text: str, variable, tooltip: str):
        """Create a modern styled checkbox with tooltip."""
        cb = ctk.CTkCheckBox(
            parent,
            text=text,
            variable=variable,
            font=self.font_normal,
            text_color=Colors.TEXT_DARK,
            fg_color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_HOVER,
            border_color=Colors.BORDER_DARK,
            checkmark_color=Colors.TEXT_DARK,
            corner_radius=4
        )
        cb.pack(anchor="w", pady=4)
        ModernTooltip(cb, tooltip)
        return cb
    
    def _toggle_theme(self):
        """Toggle between dark and light mode."""
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("light")
            self.theme_switch.configure(text="Light Mode")
        else:
            ctk.set_appearance_mode("dark")
            self.theme_switch.configure(text="Dark Mode")

    def choose_base_dir(self):
        selected = filedialog.askdirectory(initialdir=self.base_dir_var.get() or str(Path.home()))
        if selected:
            self.base_dir_var.set(selected)
            self.update_preview()

    def reset_defaults(self):
        """Reset all settings to default values."""
        self.project_name_var.set("ai_code_practice")
        self.base_dir_var.set(str(Path.home() / "Research_Code" / "02_learning_and_demos"))
        self.init_git_var.set(False)
        self.create_readme_var.set(True)
        self.create_gitignore_var.set(True)
        self.create_requirements_var.set(False)
        self.open_after_create_var.set(True)
        self.structure_text.delete("1.0", "end")
        self.structure_text.insert("1.0", DEFAULT_STRUCTURE)
        self.update_preview()

    def parse_structure(self, text: str):
        entries = []
        stack = []
        for idx, raw_line in enumerate(text.splitlines(), start=1):
            if not raw_line.strip() or raw_line.lstrip().startswith("#"):
                continue
            indent = len(raw_line) - len(raw_line.lstrip(" "))
            if indent % 2 != 0:
                raise ValueError(f"Line {idx}: use multiples of 2 spaces for indentation.")
            level = indent // 2
            name = raw_line.strip()
            is_dir = name.endswith("/") or "." not in Path(name).name
            clean_name = name.rstrip("/")
            if not clean_name:
                raise ValueError(f"Line {idx}: invalid empty name.")
            while len(stack) > level:
                stack.pop()
            if len(stack) < level:
                raise ValueError(f"Line {idx}: indentation jumps too deeply. Check nesting.")
            parent_parts = list(stack)
            full_parts = parent_parts + [clean_name]
            rel_path = Path(*full_parts)
            entries.append((rel_path, is_dir))
            if is_dir:
                if len(stack) == level:
                    stack.append(clean_name)
                else:
                    stack[level] = clean_name
        return entries

    def build_preview(self, project_path: Path, entries):
        lines = [str(project_path)]
        seen = set()
        for rel_path, is_dir in entries:
            parts = rel_path.parts
            prefix = []
            for i, part in enumerate(parts):
                prefix.append(part)
                p = tuple(prefix)
                if p in seen:
                    continue
                seen.add(p)
                indent = "  " * (i + 1)
                if i < len(parts) - 1:
                    lines.append(f"{indent}{part}/")
                else:
                    lines.append(f"{indent}{part}{'/' if is_dir else ''}")
        return "\n".join(lines)

    def update_preview(self):
        """Update the preview panel with the current structure."""
        try:
            project_path = Path(self.base_dir_var.get()).expanduser() / self.project_name_var.get().strip()
            entries = self.parse_structure(self.structure_text.get("1.0", "end"))
            preview = self.build_preview(project_path, entries)
            self.status_label.configure(text="✓ Valid structure", text_color=Colors.SUCCESS)
        except Exception as exc:
            preview = f"⚠️ Error: {exc}"
            self.status_label.configure(text="⚠ Invalid structure", text_color=Colors.ERROR)
        
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")
        self.preview_text.insert("1.0", preview)
        self.preview_text.configure(state="disabled")

    def save_template(self):
        """Save current structure as a template file."""
        filepath = filedialog.asksaveasfilename(
            title="Save template",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile="project_template.json",
        )
        if not filepath:
            return
        payload = {
            "structure": self.structure_text.get("1.0", "end"),
            "options": {
                "create_readme": self.create_readme_var.get(),
                "create_gitignore": self.create_gitignore_var.get(),
                "create_requirements": self.create_requirements_var.get(),
                "init_git": self.init_git_var.get(),
                "open_after_create": self.open_after_create_var.get(),
            },
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        self._show_success("Template Saved", f"Template saved to:\n{filepath}")

    def load_template(self):
        """Load a template file."""
        filepath = filedialog.askopenfilename(
            title="Load template",
            filetypes=[("JSON files", "*.json")],
        )
        if not filepath:
            return
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                payload = json.load(f)
            structure = payload.get("structure", DEFAULT_STRUCTURE)
            self.structure_text.delete("1.0", "end")
            self.structure_text.insert("1.0", structure)
            options = payload.get("options", {})
            self.create_readme_var.set(bool(options.get("create_readme", True)))
            self.create_gitignore_var.set(bool(options.get("create_gitignore", True)))
            self.create_requirements_var.set(bool(options.get("create_requirements", False)))
            self.init_git_var.set(bool(options.get("init_git", False)))
            self.open_after_create_var.set(bool(options.get("open_after_create", True)))
            self.update_preview()
            self._show_success("Template Loaded", f"Template loaded from:\n{filepath}")
        except Exception as exc:
            self._show_error("Load Failed", f"Failed to load template:\n{exc}")

    def write_special_file(self, path: Path, project_name: str):
        if path.name == "README.md" and self.create_readme_var.get() and not path.exists():
            path.write_text(DEFAULT_README.format(project_name=project_name), encoding="utf-8")
        elif path.name == ".gitignore" and self.create_gitignore_var.get() and not path.exists():
            path.write_text(DEFAULT_GITIGNORE, encoding="utf-8")
        elif path.name == "requirements.txt" and self.create_requirements_var.get() and not path.exists():
            path.write_text("# Add your dependencies here\n", encoding="utf-8")
        elif path.name == "main.py" and not path.exists():
            path.write_text(DEFAULT_MAIN.format(project_name=project_name), encoding="utf-8")
        elif not path.exists():
            path.touch()

    def initialize_git(self, project_path: Path):
        try:
            subprocess.run(["git", "init"], cwd=str(project_path), check=True, capture_output=True, text=True)
            return True, "Git repository initialized."
        except FileNotFoundError:
            return False, "Git is not installed or not on PATH."
        except subprocess.CalledProcessError as exc:
            return False, exc.stderr.strip() or exc.stdout.strip() or "git init failed."

    def open_folder(self, path: Path):
        """Open the project folder in the system file manager."""
        try:
            if sys.platform.startswith("darwin"):
                subprocess.Popen(["open", str(path)])
            elif os.name == "nt":
                os.startfile(str(path))  # type: ignore[attr-defined]
            else:
                subprocess.Popen(["xdg-open", str(path)])
        except Exception:
            pass
    
    def _show_error(self, title: str, message: str):
        """Show a modern error dialog."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(fg_color=Colors.BG_DARK)
        
        # Center the dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 400) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 200) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Content
        ctk.CTkLabel(
            dialog,
            text="❌",
            font=CTkFont(size=40)
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            dialog,
            text=message,
            font=self.font_normal,
            text_color=Colors.TEXT_DARK,
            wraplength=350
        ).pack(pady=10, padx=20)
        
        ctk.CTkButton(
            dialog,
            text="OK",
            width=100,
            height=36,
            corner_radius=8,
            fg_color=Colors.ERROR,
            hover_color="#dc2626",
            command=dialog.destroy
        ).pack(pady=15)
    
    def _show_success(self, title: str, message: str):
        """Show a modern success dialog."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(title)
        dialog.geometry("450x220")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(fg_color=Colors.BG_DARK)
        
        # Center the dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 450) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 220) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Content
        ctk.CTkLabel(
            dialog,
            text="✅",
            font=CTkFont(size=40)
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            dialog,
            text=message,
            font=self.font_normal,
            text_color=Colors.TEXT_DARK,
            wraplength=400
        ).pack(pady=10, padx=20)
        
        ctk.CTkButton(
            dialog,
            text="OK",
            width=100,
            height=36,
            corner_radius=8,
            fg_color=Colors.SUCCESS,
            hover_color="#16a34a",
            command=dialog.destroy
        ).pack(pady=15)

    def create_project(self):
        """Create the project with the configured structure."""
        project_name = self.project_name_var.get().strip()
        if not project_name:
            self._show_error("Missing Project Name", "Please enter a project name.")
            return
        try:
            entries = self.parse_structure(self.structure_text.get("1.0", "end"))
        except Exception as exc:
            self._show_error("Structure Error", str(exc))
            return

        base_dir = Path(self.base_dir_var.get()).expanduser()
        project_path = base_dir / project_name
        try:
            project_path.mkdir(parents=True, exist_ok=True)
            for rel_path, is_dir in entries:
                target = project_path / rel_path
                if is_dir:
                    target.mkdir(parents=True, exist_ok=True)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    self.write_special_file(target, project_name)

            local_config = {
                "structure": self.structure_text.get("1.0", "end"),
                "options": {
                    "create_readme": self.create_readme_var.get(),
                    "create_gitignore": self.create_gitignore_var.get(),
                    "create_requirements": self.create_requirements_var.get(),
                    "init_git": self.init_git_var.get(),
                    "open_after_create": self.open_after_create_var.get(),
                },
            }
            with open(project_path / CONFIG_FILENAME, "w", encoding="utf-8") as f:
                json.dump(local_config, f, ensure_ascii=False, indent=2)

            git_message = ""
            if self.init_git_var.get():
                ok, git_message = self.initialize_git(project_path)
                if not ok:
                    git_message = f"\n\nGit note: {git_message}"
                else:
                    git_message = "\n\n✓ Git repository initialized."

            if self.open_after_create_var.get():
                self.open_folder(project_path)

            self._show_success("Project Created", f"Project created at:\n{project_path}{git_message}")
        except Exception as exc:
            self._show_error("Creation Failed", f"Failed to create project:\n{exc}")


def main():
    """Application entry point."""
    # Set appearance before creating window
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Create main window
    root = ctk.CTk()
    
    # Set window icon if available (macOS already has good defaults)
    if sys.platform.startswith("darwin"):
        try:
            root.iconbitmap(default="")
        except Exception:
            pass
    
    app = ScaffoldApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
