import tkinter as tk

BTN_BG = "#8C6C42"        
BTN_HOVER = "#A3845A"    
BTN_ACTIVE = "#6E532F"   

class HoverButton(tk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.default_bg = self["background"]

        # Hover
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        # Nhấn nút
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

    def on_enter(self, e):
        self["background"] = BTN_HOVER

    def on_leave(self, e):
        self["background"] = self.default_bg

    def on_press(self, e):
        self["background"] = BTN_ACTIVE

    def on_release(self, e):
        self["background"] = BTN_HOVER
