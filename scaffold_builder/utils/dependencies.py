"""
Dependency management utilities.
"""

import subprocess
import sys


def ensure_customtkinter():
    """
    Ensure CustomTkinter is installed and return the module.
    
    Returns:
        customtkinter module
    """
    try:
        import customtkinter as ctk
        return ctk
    except ImportError:
        print("CustomTkinter not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
        import customtkinter as ctk
        return ctk
