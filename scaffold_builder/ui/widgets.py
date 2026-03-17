"""
Custom widgets for the application.
"""

import tkinter as tk
from typing import Optional

from ..config import Colors


class ModernTooltip:
    """
    Modern-styled tooltip that appears on hover.
    
    Shows a tooltip with a small delay when the mouse enters a widget,
    and hides it when the mouse leaves or when clicked.
    """
    
    def __init__(self, widget, text: str, delay: int = 500):
        """
        Initialize the tooltip.
        
        Args:
            widget: The widget to attach the tooltip to
            text: The tooltip text to display
            delay: Delay in milliseconds before showing the tooltip
        """
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tipwindow: Optional[tk.Toplevel] = None
        self.scheduled_id: Optional[str] = None
        
        widget.bind("<Enter>", self._schedule_show)
        widget.bind("<Leave>", self._hide)
        widget.bind("<ButtonPress>", self._hide)
    
    def _schedule_show(self, event=None):
        """Schedule the tooltip to show after the delay."""
        self._cancel_schedule()
        self.scheduled_id = self.widget.after(self.delay, self._show)
    
    def _cancel_schedule(self):
        """Cancel any scheduled tooltip show."""
        if self.scheduled_id:
            self.widget.after_cancel(self.scheduled_id)
            self.scheduled_id = None
    
    def _show(self, event=None):
        """Show the tooltip."""
        if self.tipwindow or not self.text:
            return
        
        # Position tooltip centered below the widget
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
        
        # Center the tooltip
        tw.update_idletasks()
        tw_width = tw.winfo_width()
        x = x - tw_width // 2
        tw.wm_geometry(f"+{x}+{y}")
    
    def _hide(self, event=None):
        """Hide the tooltip."""
        self._cancel_schedule()
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None
    
    def update_text(self, text: str):
        """Update the tooltip text."""
        self.text = text
