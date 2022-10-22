from tkinter import *


class Chat():
    def __init__(self, width, height):

        self.window = Tk()
        self.window.title("Mpp4")
        self.canva = Canvas(self.window, width= width, height= height)
        self.canva.grid(columnspan=3)
        self.create_widgets()


    def create_widgets(self):
        self.txt_area = Text(self.canva, border = 1)
        self.txt_field = Entry(self.canva, width = 85, border = 1, bg = 'white')
        self.send_button = Button(self.canva, text='Send', padx = 40, command = self.send)
       
        self.txt_area.config(background = '#c8e2c8')

        self.txt_area.grid(column = 0, row = 0, columnspan = 3)
        self.txt_field.grid(column = 0, row = 1, columnspan = 2)
        self.send_button.grid(column = 2, row = 1)

    def send(self, event = None):
        text = self.txt_field.get() + '\n'
        self.txt_area.insert(END, text)
        self.txt_field.delete(0,END)

    def start(self):
        self.window.mainloop()

if __name__ == "__main__":
    chat = Chat(600,800).start()