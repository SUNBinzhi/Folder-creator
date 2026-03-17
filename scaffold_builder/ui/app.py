"""
Main UI application class.
"""

import json
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk
from customtkinter import CTkFont

from ..config import (
    APP_TITLE,
    APP_VERSION,
    Colors,
    DEFAULT_TEMPLATE_NAME,
    PROJECT_TEMPLATES,
)
from ..config.settings import (
    DEFAULT_BASE_DIR,
    DEFAULT_PROJECT_NAME,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_MIN_HEIGHT,
    FONT_FAMILY,
    FONT_FAMILY_MONO,
    FONT_SIZE_TITLE,
    FONT_SIZE_SECTION,
    FONT_SIZE_NORMAL,
    FONT_SIZE_MONO,
    FONT_SIZE_SMALL,
)
from ..config.templates import get_default_names
from ..core.parser import StructureParser, build_preview
from ..core.builder import ProjectBuilder, BuildOptions
from .widgets import ModernTooltip
from .dialogs import show_error, show_success


class ScaffoldApp:
    """Main application class with modern CustomTkinter UI."""

    def __init__(self, root: ctk.CTk):
        self.root = root
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        self._setup_fonts()
        self._setup_variables()
        self._build_ui()

        self._on_template_change(DEFAULT_TEMPLATE_NAME)
        self.update_preview()

    def _setup_fonts(self):
        self.font_title = CTkFont(family=FONT_FAMILY, size=FONT_SIZE_TITLE, weight="bold")
        self.font_section = CTkFont(family=FONT_FAMILY, size=FONT_SIZE_SECTION, weight="bold")
        self.font_normal = CTkFont(family=FONT_FAMILY, size=FONT_SIZE_NORMAL)
        self.font_mono = CTkFont(family=FONT_FAMILY_MONO, size=FONT_SIZE_MONO)
        self.font_small = CTkFont(family=FONT_FAMILY, size=FONT_SIZE_SMALL)

    def _setup_variables(self):
        self.base_dir_var = ctk.StringVar(value=str(DEFAULT_BASE_DIR))
        self.project_name_var = ctk.StringVar(value=DEFAULT_PROJECT_NAME)
        self.template_type_var = ctk.StringVar(value=DEFAULT_TEMPLATE_NAME)

        self.init_git_var = ctk.BooleanVar(value=False)
        self.create_readme_var = ctk.BooleanVar(value=True)
        self.create_gitignore_var = ctk.BooleanVar(value=True)
        self.create_requirements_var = ctk.BooleanVar(value=False)
        self.open_after_create_var = ctk.BooleanVar(value=True)

    def _build_ui(self):
        self.root.configure(fg_color=Colors.BG_DARK)

        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=0, minsize=320)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        left_panel = self._build_left_panel(main_frame)
        self._build_right_panel(main_frame)

        self._build_theme_switch(left_panel)

    def _build_left_panel(self, main_frame):
        left_panel = ctk.CTkFrame(main_frame, fg_color=Colors.BG_DARK_SECONDARY, corner_radius=16)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        header_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            header_frame,
            text="⚙️ Project Settings",
            font=self.font_title,
            text_color=Colors.TEXT_DARK,
        ).pack(anchor="w")

        ctk.CTkLabel(
            header_frame,
            text="Configure your new project",
            font=self.font_small,
            text_color=Colors.TEXT_MUTED,
        ).pack(anchor="w", pady=(4, 0))

        ctk.CTkFrame(left_panel, height=1, fg_color=Colors.BORDER_DARK).pack(fill="x", padx=20, pady=10)

        settings_frame = ctk.CTkScrollableFrame(
            left_panel,
            fg_color="transparent",
            scrollbar_button_color=Colors.BORDER_DARK,
            scrollbar_button_hover_color=Colors.PRIMARY_LIGHT,
        )
        settings_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self._create_template_selector(settings_frame)
        self._create_input_group(settings_frame, "📁 Base Location", self.base_dir_var, with_browse=True)
        self._create_input_group(
            settings_frame,
            "📝 Project Name",
            self.project_name_var,
            on_change=self.update_preview,
        )

        options_label = ctk.CTkLabel(
            settings_frame,
            text="🔧 Options",
            font=self.font_section,
            text_color=Colors.TEXT_DARK,
        )
        options_label.pack(anchor="w", pady=(20, 12))

        options = [
            ("Create README.md content", self.create_readme_var, "Fills README.md with starter content"),
            ("Create .gitignore content", self.create_gitignore_var, "Adds Python/research defaults"),
            ("Create requirements.txt", self.create_requirements_var, "Adds requirements placeholder"),
            ("Initialize Git repository", self.init_git_var, "Runs git init in project folder"),
            ("Open folder after creation", self.open_after_create_var, "Opens folder in file manager"),
        ]
        for text, var, tip in options:
            self._create_checkbox(settings_frame, text, var, tip)

        self._create_action_buttons(left_panel)
        return left_panel

    def _build_right_panel(self, main_frame):
        right_panel = ctk.CTkFrame(main_frame, fg_color="transparent")
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=1)
        right_panel.grid_rowconfigure(3, weight=1)

        structure_header = ctk.CTkFrame(right_panel, fg_color="transparent")
        structure_header.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        ctk.CTkLabel(
            structure_header,
            text="📂 Editable Structure",
            font=self.font_section,
            text_color=Colors.TEXT_DARK,
        ).pack(side="left")
        ctk.CTkLabel(
            structure_header,
            text="Use 2-space indentation for nesting",
            font=self.font_small,
            text_color=Colors.TEXT_MUTED,
        ).pack(side="right")

        structure_frame = ctk.CTkFrame(right_panel, fg_color=Colors.BG_DARK_SECONDARY, corner_radius=12)
        structure_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 12))
        self.structure_text = ctk.CTkTextbox(
            structure_frame,
            wrap="none",
            font=self.font_mono,
            fg_color=Colors.BG_DARK,
            text_color=Colors.TEXT_DARK,
            border_width=0,
            corner_radius=8,
            scrollbar_button_color=Colors.BORDER_DARK,
            scrollbar_button_hover_color=Colors.PRIMARY_LIGHT,
        )
        self.structure_text.pack(fill="both", expand=True, padx=8, pady=8)
        self.structure_text.bind("<KeyRelease>", lambda _e: self.update_preview())
        self.structure_text.bind("<FocusOut>", lambda _e: self.update_preview())

        preview_header = ctk.CTkFrame(right_panel, fg_color="transparent")
        preview_header.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        ctk.CTkLabel(
            preview_header,
            text="👁️ Preview",
            font=self.font_section,
            text_color=Colors.TEXT_DARK,
        ).pack(side="left")

        self.status_label = ctk.CTkLabel(
            preview_header,
            text="Ready",
            font=self.font_small,
            text_color=Colors.SUCCESS,
        )
        self.status_label.pack(side="right")

        preview_frame = ctk.CTkFrame(right_panel, fg_color=Colors.BG_DARK_SECONDARY, corner_radius=12)
        preview_frame.grid(row=3, column=0, sticky="nsew")
        self.preview_text = ctk.CTkTextbox(
            preview_frame,
            wrap="none",
            font=self.font_mono,
            fg_color=Colors.BG_DARK,
            text_color=Colors.PRIMARY_LIGHT,
            border_width=0,
            corner_radius=8,
            scrollbar_button_color=Colors.BORDER_DARK,
            scrollbar_button_hover_color=Colors.PRIMARY_LIGHT,
        )
        self.preview_text.pack(fill="both", expand=True, padx=8, pady=8)
        self.preview_text.configure(state="disabled")

    def _create_action_buttons(self, left_panel):
        buttons_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)

        secondary_row = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        secondary_row.pack(fill="x", pady=(0, 10))
        secondary_row.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(
            secondary_row,
            text="Reset",
            height=36,
            corner_radius=8,
            fg_color="transparent",
            border_width=1,
            border_color=Colors.BORDER_DARK,
            hover_color=Colors.BG_DARK,
            font=self.font_small,
            command=self.reset_defaults,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 4))

        ctk.CTkButton(
            secondary_row,
            text="Save",
            height=36,
            corner_radius=8,
            fg_color="transparent",
            border_width=1,
            border_color=Colors.BORDER_DARK,
            hover_color=Colors.BG_DARK,
            font=self.font_small,
            command=self.save_template,
        ).grid(row=0, column=1, sticky="ew", padx=4)

        ctk.CTkButton(
            secondary_row,
            text="Load",
            height=36,
            corner_radius=8,
            fg_color="transparent",
            border_width=1,
            border_color=Colors.BORDER_DARK,
            hover_color=Colors.BG_DARK,
            font=self.font_small,
            command=self.load_template,
        ).grid(row=0, column=2, sticky="ew", padx=(4, 0))

        create_btn = ctk.CTkButton(
            buttons_frame,
            text="✨ Create Project",
            height=48,
            corner_radius=12,
            fg_color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_HOVER,
            font=self.font_section,
            command=self.create_project,
        )
        create_btn.pack(fill="x")
        ModernTooltip(create_btn, "Create the project with the configured structure")

    def _build_theme_switch(self, left_panel):
        theme_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        theme_frame.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkLabel(theme_frame, text="Theme:", font=self.font_small, text_color=Colors.TEXT_MUTED).pack(side="left")

        self.theme_switch = ctk.CTkSwitch(
            theme_frame,
            text="Dark Mode",
            font=self.font_small,
            command=self._toggle_theme,
            onvalue=True,
            offvalue=False,
            progress_color=Colors.PRIMARY,
        )
        self.theme_switch.pack(side="left", padx=(8, 0))
        self.theme_switch.select()

    def _create_input_group(self, parent, label, variable, with_browse=False, on_change=None):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(frame, text=label, font=self.font_section, text_color=Colors.TEXT_DARK).pack(
            anchor="w", pady=(0, 8)
        )

        if with_browse:
            row = ctk.CTkFrame(frame, fg_color="transparent")
            row.pack(fill="x")
            row.grid_columnconfigure(0, weight=1)
            entry = ctk.CTkEntry(
                row,
                textvariable=variable,
                height=40,
                corner_radius=8,
                border_width=1,
                border_color=Colors.BORDER_DARK,
                fg_color=Colors.BG_DARK,
                text_color=Colors.TEXT_DARK,
                font=self.font_normal,
            )
            entry.grid(row=0, column=0, sticky="ew")
            browse_btn = ctk.CTkButton(
                row,
                text="📂",
                width=40,
                height=40,
                corner_radius=8,
                fg_color=Colors.BG_DARK,
                hover_color=Colors.PRIMARY,
                border_width=1,
                border_color=Colors.BORDER_DARK,
                command=self.choose_base_dir,
            )
            browse_btn.grid(row=0, column=1, padx=(8, 0))
            ModernTooltip(browse_btn, "Browse for folder")
            return

        entry = ctk.CTkEntry(
            frame,
            textvariable=variable,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color=Colors.BORDER_DARK,
            fg_color=Colors.BG_DARK,
            text_color=Colors.TEXT_DARK,
            font=self.font_normal,
        )
        entry.pack(fill="x")
        if on_change:
            entry.bind("<KeyRelease>", lambda _e: on_change())

    def _create_checkbox(self, parent, text, variable, tooltip):
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
            corner_radius=4,
        )
        cb.pack(anchor="w", pady=4)
        ModernTooltip(cb, tooltip)

    def _create_template_selector(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(frame, text="🎯 Project Type", font=self.font_section, text_color=Colors.TEXT_DARK).pack(
            anchor="w", pady=(0, 8)
        )

        template_names = list(PROJECT_TEMPLATES.keys())
        self.template_dropdown = ctk.CTkComboBox(
            frame,
            values=template_names,
            variable=self.template_type_var,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color=Colors.BORDER_DARK,
            fg_color=Colors.BG_DARK,
            button_color=Colors.PRIMARY,
            button_hover_color=Colors.PRIMARY_HOVER,
            dropdown_fg_color=Colors.BG_DARK_SECONDARY,
            dropdown_hover_color=Colors.PRIMARY,
            dropdown_text_color=Colors.TEXT_DARK,
            text_color=Colors.TEXT_DARK,
            font=self.font_normal,
            dropdown_font=self.font_normal,
            command=self._on_template_change,
            state="readonly",
        )
        self.template_dropdown.pack(fill="x")

        self.template_desc_label = ctk.CTkLabel(
            frame,
            text=PROJECT_TEMPLATES[DEFAULT_TEMPLATE_NAME]["description"],
            font=self.font_small,
            text_color=Colors.TEXT_MUTED,
            wraplength=260,
            justify="left",
        )
        self.template_desc_label.pack(anchor="w", pady=(8, 0))

    def _on_template_change(self, template_name: str):
        if template_name not in PROJECT_TEMPLATES:
            return

        template = PROJECT_TEMPLATES[template_name]
        self.template_desc_label.configure(text=template["description"])

        current_name = self.project_name_var.get().strip()
        default_names = get_default_names() + [DEFAULT_PROJECT_NAME]
        if current_name in default_names:
            self.project_name_var.set(template["default_name"])

        self.structure_text.delete("1.0", "end")
        self.structure_text.insert("1.0", template["structure"])
        self.update_preview()

    def _toggle_theme(self):
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
        self.template_type_var.set(DEFAULT_TEMPLATE_NAME)
        self.project_name_var.set(PROJECT_TEMPLATES[DEFAULT_TEMPLATE_NAME]["default_name"])
        self.base_dir_var.set(str(DEFAULT_BASE_DIR))
        self.init_git_var.set(False)
        self.create_readme_var.set(True)
        self.create_gitignore_var.set(True)
        self.create_requirements_var.set(False)
        self.open_after_create_var.set(True)
        self._on_template_change(DEFAULT_TEMPLATE_NAME)

    def update_preview(self):
        try:
            project_path = Path(self.base_dir_var.get()).expanduser() / self.project_name_var.get().strip()
            entries = StructureParser(self.structure_text.get("1.0", "end")).parse()
            preview = build_preview(project_path, entries)
            self.status_label.configure(text="✓ Valid structure", text_color=Colors.SUCCESS)
        except Exception as exc:
            preview = f"⚠️ Error: {exc}"
            self.status_label.configure(text="⚠ Invalid structure", text_color=Colors.ERROR)

        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")
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
            "template_type": self.template_type_var.get(),
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
        show_success(self.root, "Template Saved", f"Template saved to:\n{filepath}")

    def load_template(self):
        filepath = filedialog.askopenfilename(
            title="Load template",
            filetypes=[("JSON files", "*.json")],
        )
        if not filepath:
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                payload = json.load(f)

            template_type = payload.get("template_type", "📝 Custom (Empty)")
            if template_type in PROJECT_TEMPLATES:
                self.template_type_var.set(template_type)
                self.template_desc_label.configure(text=PROJECT_TEMPLATES[template_type]["description"])

            structure = payload.get("structure", PROJECT_TEMPLATES[DEFAULT_TEMPLATE_NAME]["structure"])
            self.structure_text.delete("1.0", "end")
            self.structure_text.insert("1.0", structure)

            options = payload.get("options", {})
            self.create_readme_var.set(bool(options.get("create_readme", True)))
            self.create_gitignore_var.set(bool(options.get("create_gitignore", True)))
            self.create_requirements_var.set(bool(options.get("create_requirements", False)))
            self.init_git_var.set(bool(options.get("init_git", False)))
            self.open_after_create_var.set(bool(options.get("open_after_create", True)))

            self.update_preview()
            show_success(self.root, "Template Loaded", f"Template loaded from:\n{filepath}")
        except Exception as exc:
            show_error(self.root, "Load Failed", f"Failed to load template:\n{exc}")

    def create_project(self):
        project_name = self.project_name_var.get().strip()
        if not project_name:
            show_error(self.root, "Missing Project Name", "Please enter a project name.")
            return

        try:
            structure_text = self.structure_text.get("1.0", "end")
            entries = StructureParser(structure_text).parse()
        except Exception as exc:
            show_error(self.root, "Structure Error", str(exc))
            return

        options = BuildOptions(
            create_readme=self.create_readme_var.get(),
            create_gitignore=self.create_gitignore_var.get(),
            create_requirements=self.create_requirements_var.get(),
            init_git=self.init_git_var.get(),
            open_after_create=self.open_after_create_var.get(),
        )

        builder = ProjectBuilder(
            base_dir=Path(self.base_dir_var.get()),
            project_name=project_name,
            entries=entries,
            options=options,
            structure_text=structure_text,
            template_type=self.template_type_var.get(),
        )
        result = builder.build()

        if not result.success:
            show_error(self.root, "Creation Failed", result.message)
            return

        message = result.message
        if options.init_git:
            if result.git_initialized:
                message += "\n\n✓ Git repository initialized."
            elif result.git_message:
                message += f"\n\nGit note: {result.git_message}"

        show_success(self.root, "Project Created", message)
