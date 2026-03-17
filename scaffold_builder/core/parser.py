"""
Structure parser for parsing text-based folder/file structure definitions.
"""

from pathlib import Path
from typing import List, Tuple


class StructureParser:
    """
    Parses a text-based structure definition into a list of paths.
    
    Structure format:
    - One item per line
    - Use 2-space indentation for nesting
    - Folder names optionally end with '/'
    - Lines starting with '#' are comments
    """
    
    INDENT_SIZE = 2
    
    def __init__(self, text: str):
        """
        Initialize parser with structure text.
        
        Args:
            text: Multi-line string defining the folder structure
        """
        self.text = text
        self._entries: List[Tuple[Path, bool]] = []
    
    def parse(self) -> List[Tuple[Path, bool]]:
        """
        Parse the structure text and return a list of (path, is_directory) tuples.
        
        Returns:
            List of tuples containing (relative_path, is_directory)
            
        Raises:
            ValueError: If the structure contains invalid indentation or syntax
        """
        self._entries = []
        stack: List[str] = []
        
        for idx, raw_line in enumerate(self.text.splitlines(), start=1):
            # Skip empty lines and comments
            if not raw_line.strip() or raw_line.lstrip().startswith("#"):
                continue
            
            # Calculate indentation level
            indent = len(raw_line) - len(raw_line.lstrip(" "))
            if indent % self.INDENT_SIZE != 0:
                raise ValueError(
                    f"Line {idx}: use multiples of {self.INDENT_SIZE} spaces for indentation."
                )
            
            level = indent // self.INDENT_SIZE
            name = raw_line.strip()
            
            # Determine if this is a directory
            is_dir = self._is_directory(name)
            clean_name = name.rstrip("/")
            
            if not clean_name:
                raise ValueError(f"Line {idx}: invalid empty name.")
            
            # Adjust stack to current level
            while len(stack) > level:
                stack.pop()
            
            if len(stack) < level:
                raise ValueError(
                    f"Line {idx}: indentation jumps too deeply. Check nesting."
                )
            
            # Build full path
            parent_parts = list(stack)
            full_parts = parent_parts + [clean_name]
            rel_path = Path(*full_parts)
            
            self._entries.append((rel_path, is_dir))
            
            # Update stack for directories
            if is_dir:
                if len(stack) == level:
                    stack.append(clean_name)
                else:
                    stack[level] = clean_name
        
        return self._entries
    
    def _is_directory(self, name: str) -> bool:
        """
        Determine if a name represents a directory.
        
        A name is considered a directory if:
        - It ends with '/'
        - It has no file extension (no '.' in the filename)
        
        Args:
            name: The file or folder name
            
        Returns:
            True if the name represents a directory
        """
        if name.endswith("/"):
            return True
        return "." not in Path(name).name


def parse_structure(text: str) -> List[Tuple[Path, bool]]:
    """
    Convenience function to parse a structure text.
    
    Args:
        text: Multi-line string defining the folder structure
        
    Returns:
        List of tuples containing (relative_path, is_directory)
    """
    parser = StructureParser(text)
    return parser.parse()


def build_preview(project_path: Path, entries: List[Tuple[Path, bool]]) -> str:
    """
    Build a preview string showing the project structure.
    
    Args:
        project_path: The root project path
        entries: List of (path, is_directory) tuples
        
    Returns:
        Formatted string showing the tree structure
    """
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
                suffix = "/" if is_dir else ""
                lines.append(f"{indent}{part}{suffix}")
    
    return "\n".join(lines)
