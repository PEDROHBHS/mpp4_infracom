from tkinter import *

class Window:
    window = Tk()
    window.resizable(False, False)

    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title

        self.window.title(self.title)

        self.canva = Canvas(self.window, width=self.width, height=self.height)
        self.canva.grid(columnspan=6)
        
        self.create_widgets()

    def create_widgets(self):
        pass

    def start(self):
        self.window.mainloop()