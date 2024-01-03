import tkinter as tk


class NavBar(tk.Frame):
    def __init__(self, options, font=('UnifrakturMaguntia', 20), master=None):
        super().__init__(master=master)
        for option in options:
            tk.Button(self, text=option[0], command=option[1], font=font).pack(side=tk.LEFT)
        tk.Button(self, text="Închide", command=master.quit, font=font).pack(side=tk.RIGHT)
