import tkinter as tk

class RegionSelector:
    def __init__(self, callback):
        self.callback = callback

    def start(self):
        self.overlay = tk.Toplevel()
        self.overlay.attributes("-fullscreen", True)
        self.overlay.attributes("-alpha", 0.3)
        self.overlay.config(bg='gray')
        self.overlay.attributes("-topmost", True)

        self.start_x = self.start_y = self.rect = None
        self.canvas = tk.Canvas(self.overlay, cursor="cross", bg='gray')
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.overlay.bind("<Escape>", lambda e: self.overlay.destroy())

    def on_mouse_down(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_mouse_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_mouse_up(self, event):
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)
        self.callback((x1, y1, x2, y2))
        self.overlay.destroy()
