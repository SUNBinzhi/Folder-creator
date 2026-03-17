"""
Dialog boxes for the application.
"""

import customtkinter as ctk
from customtkinter import CTkFont

from ..config import Colors


def show_error(parent: ctk.CTk, title: str, message: str):
    """
    Show a modern error dialog.
    
    Args:
        parent: Parent window
        title: Dialog title
        message: Error message to display
    """
    dialog = ctk.CTkToplevel(parent)
    dialog.title(title)
    dialog.geometry("400x200")
    dialog.transient(parent)
    dialog.grab_set()
    dialog.configure(fg_color=Colors.BG_DARK)
    
    # Center the dialog
    dialog.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() - 400) // 2
    y = parent.winfo_y() + (parent.winfo_height() - 200) // 2
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
        font=CTkFont(size=13),
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


def show_success(parent: ctk.CTk, title: str, message: str):
    """
    Show a modern success dialog.
    
    Args:
        parent: Parent window
        title: Dialog title
        message: Success message to display
    """
    dialog = ctk.CTkToplevel(parent)
    dialog.title(title)
    dialog.geometry("450x220")
    dialog.transient(parent)
    dialog.grab_set()
    dialog.configure(fg_color=Colors.BG_DARK)
    
    # Center the dialog
    dialog.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() - 450) // 2
    y = parent.winfo_y() + (parent.winfo_height() - 220) // 2
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
        font=CTkFont(size=13),
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


def show_confirm(parent: ctk.CTk, title: str, message: str, on_confirm=None, on_cancel=None):
    """
    Show a modern confirmation dialog.
    
    Args:
        parent: Parent window
        title: Dialog title
        message: Confirmation message to display
        on_confirm: Callback when confirmed
        on_cancel: Callback when cancelled
    """
    dialog = ctk.CTkToplevel(parent)
    dialog.title(title)
    dialog.geometry("400x200")
    dialog.transient(parent)
    dialog.grab_set()
    dialog.configure(fg_color=Colors.BG_DARK)
    
    # Center the dialog
    dialog.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() - 400) // 2
    y = parent.winfo_y() + (parent.winfo_height() - 200) // 2
    dialog.geometry(f"+{x}+{y}")
    
    # Content
    ctk.CTkLabel(
        dialog,
        text="❓",
        font=CTkFont(size=40)
    ).pack(pady=(20, 10))
    
    ctk.CTkLabel(
        dialog,
        text=message,
        font=CTkFont(size=13),
        text_color=Colors.TEXT_DARK,
        wraplength=350
    ).pack(pady=10, padx=20)
    
    # Buttons
    btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
    btn_frame.pack(pady=15)
    
    def handle_confirm():
        dialog.destroy()
        if on_confirm:
            on_confirm()
    
    def handle_cancel():
        dialog.destroy()
        if on_cancel:
            on_cancel()
    
    ctk.CTkButton(
        btn_frame,
        text="Cancel",
        width=100,
        height=36,
        corner_radius=8,
        fg_color="transparent",
        border_width=1,
        border_color=Colors.BORDER_DARK,
        hover_color=Colors.BG_DARK_SECONDARY,
        command=handle_cancel
    ).pack(side="left", padx=(0, 8))
    
    ctk.CTkButton(
        btn_frame,
        text="Confirm",
        width=100,
        height=36,
        corner_radius=8,
        fg_color=Colors.PRIMARY,
        hover_color=Colors.PRIMARY_HOVER,
        command=handle_confirm
    ).pack(side="left")
