import json
import os
import subprocess
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

APP_TITLE = "Project Scaffold Builder"
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


class Tooltip:
    def __init__(self, widget, text: str):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, _event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw,
            text=self.text,
            justify=tk.LEFT,
            background="#ffffe0",
            relief=tk.SOLID,
            borderwidth=1,
            padx=8,
            pady=4,
            wraplength=300,
        )
        label.pack()

    def hide(self, _event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None


class ScaffoldApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1180x760")
        self.root.minsize(980, 650)

        self.base_dir_var = tk.StringVar(value=str(Path.home() / "Research_Code" / "02_learning_and_demos"))
        self.project_name_var = tk.StringVar(value="ai_code_practice")
        self.init_git_var = tk.BooleanVar(value=False)
        self.create_readme_var = tk.BooleanVar(value=True)
        self.create_gitignore_var = tk.BooleanVar(value=True)
        self.create_requirements_var = tk.BooleanVar(value=False)
        self.open_after_create_var = tk.BooleanVar(value=True)

        self._build_ui()
        self.structure_text.insert("1.0", DEFAULT_STRUCTURE)
        self.update_preview()

    def _build_ui(self):
        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        left = ttk.Frame(self.root, padding=16)
        left.grid(row=0, column=0, sticky="nsw")
        right = ttk.Frame(self.root, padding=(0, 16, 16, 16))
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)
        right.rowconfigure(3, weight=1)

        ttk.Label(left, text="Project settings", font=("TkDefaultFont", 13, "bold")).grid(row=0, column=0, sticky="w")

        ttk.Label(left, text="Base location").grid(row=1, column=0, sticky="w", pady=(14, 4))
        base_row = ttk.Frame(left)
        base_row.grid(row=2, column=0, sticky="ew")
        base_row.columnconfigure(0, weight=1)
        ttk.Entry(base_row, textvariable=self.base_dir_var, width=42).grid(row=0, column=0, sticky="ew")
        ttk.Button(base_row, text="Browse", command=self.choose_base_dir).grid(row=0, column=1, padx=(8, 0))

        ttk.Label(left, text="Project name").grid(row=3, column=0, sticky="w", pady=(14, 4))
        project_entry = ttk.Entry(left, textvariable=self.project_name_var, width=30)
        project_entry.grid(row=4, column=0, sticky="ew")
        project_entry.bind("<KeyRelease>", lambda e: self.update_preview())

        ttk.Label(left, text="Options").grid(row=5, column=0, sticky="w", pady=(18, 8))
        opts = [
            ("Create README.md content", self.create_readme_var, "Fills README.md with a simple starter template."),
            ("Create .gitignore content", self.create_gitignore_var, "Fills .gitignore with a practical Python/research default."),
            ("Create requirements.txt placeholder", self.create_requirements_var, "Adds a comment placeholder to requirements.txt if present."),
            ("Initialize Git repo", self.init_git_var, "Runs git init inside the new project folder if Git is installed."),
            ("Open folder after creation", self.open_after_create_var, "Opens the new folder in Finder or File Explorer."),
        ]
        for i, (text, var, tip) in enumerate(opts, start=6):
            cb = ttk.Checkbutton(left, text=text, variable=var)
            cb.grid(row=i, column=0, sticky="w", pady=2)
            Tooltip(cb, tip)

        btns = ttk.Frame(left)
        btns.grid(row=11, column=0, sticky="ew", pady=(20, 8))
        ttk.Button(btns, text="Reset defaults", command=self.reset_defaults).grid(row=0, column=0, sticky="ew")
        ttk.Button(btns, text="Save template", command=self.save_template).grid(row=1, column=0, sticky="ew", pady=(8, 0))
        ttk.Button(btns, text="Load template", command=self.load_template).grid(row=2, column=0, sticky="ew", pady=(8, 0))
        ttk.Button(btns, text="Create project", command=self.create_project).grid(row=3, column=0, sticky="ew", pady=(14, 0))

        ttk.Label(right, text="Editable structure", font=("TkDefaultFont", 13, "bold")).grid(row=0, column=0, sticky="w")
        structure_frame = ttk.Frame(right)
        structure_frame.grid(row=1, column=0, sticky="nsew", pady=(8, 16))
        structure_frame.rowconfigure(0, weight=1)
        structure_frame.columnconfigure(0, weight=1)

        self.structure_text = tk.Text(structure_frame, wrap="none", undo=True, font=("Courier", 11))
        self.structure_text.grid(row=0, column=0, sticky="nsew")
        self.structure_text.bind("<KeyRelease>", lambda e: self.update_preview())
        self.structure_text.bind("<FocusOut>", lambda e: self.update_preview())
        sy = ttk.Scrollbar(structure_frame, orient="vertical", command=self.structure_text.yview)
        sx = ttk.Scrollbar(structure_frame, orient="horizontal", command=self.structure_text.xview)
        self.structure_text.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)
        sy.grid(row=0, column=1, sticky="ns")
        sx.grid(row=1, column=0, sticky="ew")

        ttk.Label(right, text="Preview", font=("TkDefaultFont", 13, "bold")).grid(row=2, column=0, sticky="w")
        preview_frame = ttk.Frame(right)
        preview_frame.grid(row=3, column=0, sticky="nsew", pady=(8, 0))
        preview_frame.rowconfigure(0, weight=1)
        preview_frame.columnconfigure(0, weight=1)

        self.preview_text = tk.Text(preview_frame, wrap="none", state="disabled", font=("Courier", 11))
        self.preview_text.grid(row=0, column=0, sticky="nsew")
        py = ttk.Scrollbar(preview_frame, orient="vertical", command=self.preview_text.yview)
        px = ttk.Scrollbar(preview_frame, orient="horizontal", command=self.preview_text.xview)
        self.preview_text.configure(yscrollcommand=py.set, xscrollcommand=px.set)
        py.grid(row=0, column=1, sticky="ns")
        px.grid(row=1, column=0, sticky="ew")

        help_text = (
            "Tips: use 2 spaces per level. Example: src/ on one line, then two-space indented main.py below it. "
            "Folders may end with '/' but do not have to."
        )
        ttk.Label(right, text=help_text, foreground="#555555").grid(row=4, column=0, sticky="w", pady=(8, 0))

    def choose_base_dir(self):
        selected = filedialog.askdirectory(initialdir=self.base_dir_var.get() or str(Path.home()))
        if selected:
            self.base_dir_var.set(selected)
            self.update_preview()

    def reset_defaults(self):
        self.project_name_var.set("ai_code_practice")
        self.base_dir_var.set(str(Path.home() / "Research_Code" / "02_learning_and_demos"))
        self.init_git_var.set(False)
        self.create_readme_var.set(True)
        self.create_gitignore_var.set(True)
        self.create_requirements_var.set(False)
        self.open_after_create_var.set(True)
        self.structure_text.delete("1.0", tk.END)
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
        try:
            project_path = Path(self.base_dir_var.get()).expanduser() / self.project_name_var.get().strip()
            entries = self.parse_structure(self.structure_text.get("1.0", tk.END))
            preview = self.build_preview(project_path, entries)
        except Exception as exc:
            preview = f"Error: {exc}"
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert("1.0", preview)
        self.preview_text.configure(state="disabled")

    def save_template(self):
        filepath = filedialog.asksaveasfilename(
            title="Save template",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile="project_template.json",
        )
        if not filepath:
            return
        payload = {
            "structure": self.structure_text.get("1.0", tk.END),
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
        messagebox.showinfo(APP_TITLE, f"Template saved to:\n{filepath}")

    def load_template(self):
        filepath = filedialog.askopenfilename(
            title="Load template",
            filetypes=[("JSON files", "*.json")],
        )
        if not filepath:
            return
        with open(filepath, "r", encoding="utf-8") as f:
            payload = json.load(f)
        structure = payload.get("structure", DEFAULT_STRUCTURE)
        self.structure_text.delete("1.0", tk.END)
        self.structure_text.insert("1.0", structure)
        options = payload.get("options", {})
        self.create_readme_var.set(bool(options.get("create_readme", True)))
        self.create_gitignore_var.set(bool(options.get("create_gitignore", True)))
        self.create_requirements_var.set(bool(options.get("create_requirements", False)))
        self.init_git_var.set(bool(options.get("init_git", False)))
        self.open_after_create_var.set(bool(options.get("open_after_create", True)))
        self.update_preview()
        messagebox.showinfo(APP_TITLE, f"Template loaded from:\n{filepath}")

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
        try:
            if sys.platform.startswith("darwin"):
                subprocess.Popen(["open", str(path)])
            elif os.name == "nt":
                os.startfile(str(path))  # type: ignore[attr-defined]
            else:
                subprocess.Popen(["xdg-open", str(path)])
        except Exception:
            pass

    def create_project(self):
        project_name = self.project_name_var.get().strip()
        if not project_name:
            messagebox.showerror(APP_TITLE, "Please enter a project name.")
            return
        try:
            entries = self.parse_structure(self.structure_text.get("1.0", tk.END))
        except Exception as exc:
            messagebox.showerror(APP_TITLE, str(exc))
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
                "structure": self.structure_text.get("1.0", tk.END),
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
                    git_message = "\n\nGit repository initialized."

            if self.open_after_create_var.get():
                self.open_folder(project_path)

            messagebox.showinfo(APP_TITLE, f"Project created at:\n{project_path}{git_message}")
        except Exception as exc:
            messagebox.showerror(APP_TITLE, f"Failed to create project:\n{exc}")


def main():
    root = tk.Tk()
    try:
        from tkinter import ttk as _ttk
        style = _ttk.Style(root)
        if "clam" in style.theme_names():
            style.theme_use("clam")
    except Exception:
        pass
    app = ScaffoldApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
