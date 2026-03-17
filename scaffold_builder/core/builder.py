"""
Project builder for creating folder structures on disk.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Optional, Callable
from dataclasses import dataclass

from ..config import (
    CONFIG_FILENAME,
    DEFAULT_GITIGNORE,
    DEFAULT_README,
    DEFAULT_MAIN,
)


@dataclass
class BuildOptions:
    """Options for building a project."""
    create_readme: bool = True
    create_gitignore: bool = True
    create_requirements: bool = False
    init_git: bool = False
    open_after_create: bool = True


@dataclass
class BuildResult:
    """Result of a project build operation."""
    success: bool
    project_path: Path
    message: str
    git_initialized: bool = False
    git_message: str = ""


class ProjectBuilder:
    """
    Builds project folder structures on disk.
    """
    
    def __init__(
        self,
        base_dir: Path,
        project_name: str,
        entries: List[Tuple[Path, bool]],
        options: Optional[BuildOptions] = None,
        structure_text: str = "",
        template_type: str = "",
    ):
        """
        Initialize the project builder.
        
        Args:
            base_dir: Base directory where the project will be created
            project_name: Name of the project (becomes the root folder name)
            entries: List of (relative_path, is_directory) tuples
            options: Build options
            structure_text: Original structure text for saving config
        """
        self.base_dir = Path(base_dir).expanduser()
        self.project_name = project_name
        self.entries = entries
        self.options = options or BuildOptions()
        self.structure_text = structure_text
        self.template_type = template_type
        self.project_path = self.base_dir / project_name
    
    def build(self) -> BuildResult:
        """
        Build the project structure.
        
        Returns:
            BuildResult with status and messages
        """
        try:
            # Create project root
            self.project_path.mkdir(parents=True, exist_ok=True)
            
            # Create all entries
            for rel_path, is_dir in self.entries:
                target = self.project_path / rel_path
                if is_dir:
                    target.mkdir(parents=True, exist_ok=True)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    self._write_file(target)
            
            # Save local config
            self._save_config()
            
            # Initialize git if requested
            git_message = ""
            git_initialized = False
            if self.options.init_git:
                git_initialized, git_message = self._initialize_git()
            
            # Open folder if requested
            if self.options.open_after_create:
                self._open_folder()
            
            return BuildResult(
                success=True,
                project_path=self.project_path,
                message=f"Project created at:\n{self.project_path}",
                git_initialized=git_initialized,
                git_message=git_message,
            )
            
        except Exception as exc:
            return BuildResult(
                success=False,
                project_path=self.project_path,
                message=f"Failed to create project:\n{exc}",
            )
    
    def _write_file(self, path: Path):
        """Write a file with appropriate content based on filename."""
        if path.exists():
            return
        
        if path.name == "README.md" and self.options.create_readme:
            content = DEFAULT_README.format(project_name=self.project_name)
            path.write_text(content, encoding="utf-8")
        
        elif path.name == ".gitignore" and self.options.create_gitignore:
            path.write_text(DEFAULT_GITIGNORE, encoding="utf-8")
        
        elif path.name == "requirements.txt" and self.options.create_requirements:
            path.write_text("# Add your dependencies here\n", encoding="utf-8")
        
        elif path.name == "main.py":
            content = DEFAULT_MAIN.format(project_name=self.project_name)
            path.write_text(content, encoding="utf-8")
        
        else:
            path.touch()
    
    def _save_config(self):
        """Save the project configuration to a local file."""
        config = {
            "template_type": self.template_type,
            "structure": self.structure_text,
            "options": {
                "create_readme": self.options.create_readme,
                "create_gitignore": self.options.create_gitignore,
                "create_requirements": self.options.create_requirements,
                "init_git": self.options.init_git,
                "open_after_create": self.options.open_after_create,
            },
        }
        
        config_path = self.project_path / CONFIG_FILENAME
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def _initialize_git(self) -> Tuple[bool, str]:
        """Initialize a git repository in the project folder."""
        try:
            subprocess.run(
                ["git", "init"],
                cwd=str(self.project_path),
                check=True,
                capture_output=True,
                text=True,
            )
            return True, "Git repository initialized."
        except FileNotFoundError:
            return False, "Git is not installed or not on PATH."
        except subprocess.CalledProcessError as exc:
            error_msg = exc.stderr.strip() or exc.stdout.strip() or "git init failed."
            return False, error_msg
    
    def _open_folder(self):
        """Open the project folder in the system file manager."""
        try:
            if sys.platform.startswith("darwin"):
                subprocess.Popen(["open", str(self.project_path)])
            elif os.name == "nt":
                os.startfile(str(self.project_path))  # type: ignore[attr-defined]
            else:
                subprocess.Popen(["xdg-open", str(self.project_path)])
        except Exception:
            pass  # Silently ignore if we can't open the folder


def create_project(
    base_dir: Path,
    project_name: str,
    entries: List[Tuple[Path, bool]],
    options: Optional[BuildOptions] = None,
    structure_text: str = "",
    template_type: str = "",
) -> BuildResult:
    """
    Convenience function to create a project.
    
    Args:
        base_dir: Base directory where the project will be created
        project_name: Name of the project
        entries: List of (relative_path, is_directory) tuples
        options: Build options
        structure_text: Original structure text for saving config
        
    Returns:
        BuildResult with status and messages
    """
    builder = ProjectBuilder(
        base_dir=base_dir,
        project_name=project_name,
        entries=entries,
        options=options,
        structure_text=structure_text,
        template_type=template_type,
    )
    return builder.build()
