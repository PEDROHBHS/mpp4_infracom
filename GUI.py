from tkinter import *
from Window import Window
import re


def validate_ip(str):
    return bool(re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", str)) or (str == "localhost")


class MainWindow(Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

    def clear_txt(self):
        self.txt_area.config(state='normal')
        self.txt_area.delete("1.0", END)
        self.txt_area.config(state='disabled')

    def create_widgets(self):
        self.txt_area = Text(self.canva, border=1, wrap='word', background='#c8a2c8', state='disabled')
        self.txt_field = Entry(self.canva, width=85, border=1, bg='white')
        self.send_button = Button(self.canva, text='Send', padx=40)

        self.send_button.bind('<Button-1>', self.send)
        self.txt_field.bind('<Return>', self.send)

        self.menubar = Menu(self.window)
        self.chat_menu = Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label='Chat', menu=self.chat_menu)
        self.chat_menu.add_command(label='Clear', command= self.clear_txt)

        self.window.config(menu=self.menubar)

        self.scroll = Scrollbar(self.canva, orient=VERTICAL, command=self.txt_area.yview)
        self.txt_area.config(yscrollcommand=self.scroll.set)
        self.scroll.grid(column=5, row=0, sticky=(N, S))

        self.txt_area.grid(column=0, row=0, columnspan=5)
        self.txt_field.grid(column=0, row=1, columnspan=4)
        self.send_button.grid(column=4, row=1)

    def send(self, event):
        txt = self.txt_field.get()

        if txt.strip() != '':
            self.txt_area.config(state='normal')
            self.txt_area.insert(END, txt + '\n')
            self.txt_area.config(state='disabled')

        self.txt_field.delete(0, END)


class GetAddr(Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

    def delete_ip(self, event):
        self.ip_entry.delete(0, END)
        self.ip_entry.config(fg='#000000')
        self.ip_entry.unbind_all('<Button-1>')
        self.ip_entry.bind('<Key>', None)

    def delete_port(self, event):
        self.port_entry.delete(0, END)
        self.port_entry.config(fg='#000000')
        self.port_entry.unbind_all('<Button-1>')
        self.port_entry.bind('<Key>', None)

    def create_widgets(self):
        self.label_1 = Label(self.canva, text='Ip Address')
        self.label_2 = Label(self.canva, text='Port')

        self.ip_entry = Entry(self.canva, width=85, border=1, bg='white')
        self.port_entry = Entry(self.canva, width=85, border=1, bg='white')
        self.confirm_button = Button(self.canva, text='Confirm', padx=40, command=self.send)

        self.label_1.grid(column=0, row=0)
        self.label_2.grid(column=0, row=1)
        self.ip_entry.grid(column=1, row=0, columnspan=4)
        self.port_entry.grid(column=1, row=1, columnspan=4)
        self.confirm_button.grid(column=2, row=2)

    def send(self):
        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()

        if not validate_ip(ip):
            self.ip_entry.delete(0, END)
            self.port_entry.delete(0, END)

            self.ip_entry.config(fg='#ff0000')
            self.ip_entry.insert(0, "Digite um endereço válido")

            self.ip_entry.bind('<Button-1>', self.delete_ip)
            self.ip_entry.bind('<Key>', self.delete_ip)
            
        elif not port.isdigit() or int(port) > 65535:
            self.ip_entry.delete(0, END)
            self.port_entry.delete(0, END)

            self.port_entry.config(fg='#ff0000')
            self.port_entry.insert(0, "Digite uma porta válida")

            self.port_entry.bind('<Button-1>', self.delete_port)
            self.port_entry.bind('<Key>', self.delete_port)

        else:
            self.clear()
            print((ip, int(port)))
            MainWindow(720, 540, 'Teste').start()       

    def clear(self):
        self.canva.destroy()


if __name__ == "__main__":
    get_addr = GetAddr(720, 540, 'Teste').start()