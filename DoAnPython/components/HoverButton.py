import tkinter as tk

class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.default_bg = kw.get('bg', self['bg'])
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['bg'] = '#a99c80' # Màu hover
    
    def on_leave(self, e):
        self['bg'] = self.default_bg