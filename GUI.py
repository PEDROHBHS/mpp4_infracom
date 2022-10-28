from tkinter import *
from datetime import datetime
from ServerP2P import ServerP2P
from Client import Client
from Window import Window
import re


def validate_ip(str):
    return bool(re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", str)) or (str == "localhost")


class MainWindow(Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.serverChecker = False
        try:
            self.client = Client(ip, int(port), (ip_connect, int(port_connect)))
        except:
            self.server = ServerP2P(ip,int(port))
            self.serverChecker = True 

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
        if self.serverChecker:
            dt = datetime.now()
            date = dt.strftime("%m-%d-%Y %H:%Mh")
            msg = f'-> {username} [{date}] : {txt}'
            self.server.send(msg)
            msg_date, msg_rcv = self.server.receive().split(' : ')
            msg_rcv = f'{msg_date}-[{date}] : {msg_rcv}'
        else:
            dt = datetime.now()
            date = dt.strftime("%m-%d-%Y %H:%Mh")
            msg = f'-> {username} [{date}] : {txt}'
            self.client.send(msg)
            msg_date, msg_rcv = self.client.receive().split(' : ')
            msg_rcv = f'{msg_date}-[{date}] : {msg_rcv}'

        if txt.strip() != '':
            self.txt_area.config(state='normal')
            self.txt_area.insert(END, msg + '\n')
            self.txt_area.config(state='disabled')
            if (msg_rcv):
                self.txt_area.config(state='normal')
                self.txt_area.insert(END, msg_rcv + '\n')
                self.txt_area.config(state='disabled')
        self.txt_field.delete(0, END)

class Username(Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

    def create_widgets(self):
        self.usernameLabel = Label(self.canva, text = 'Username:')
        self.usernameLabel.pack(padx=15,pady= 5)
        self.usernameEntry = Entry(self.canva, bd =5)
        self.usernameEntry.pack(padx=15, pady=5)
        
        self.create_button = Button(self.canva, text='Create', command=self.send)
        self.create_button.pack(side = LEFT , padx = 60)

    def send(self):
        global username
        username = self.usernameEntry.get().strip()
        self.usernameEntry.delete(0, END)
        self.clear()

        GetAddr(720, 540, username).start()

    def clear(self):
        self.canva.destroy()

class GetAddr(Window):
    def __init__(self, width, height, title):
        title = f'Chat P2P de {username}'
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
        self.label_3 = Label(self.canva, text='Ip Address of connection')
        self.label_4 = Label(self.canva, text='Port of connection')

        self.ip_entry = Entry(self.canva, width=85, border=1, bg='white')
        self.port_entry = Entry(self.canva, width=85, border=1, bg='white')
        self.ip_other_entry = Entry(self.canva, width=85, border=1, bg='white')
        self.port_other_entry = Entry(self.canva, width=85, border=1, bg='white')
        self.confirm_button = Button(self.canva, text='Confirm', padx=40, command=self.send)

        self.label_1.grid(column=0, row=0)
        self.label_2.grid(column=0, row=1)
        self.ip_entry.grid(column=1, row=0, columnspan=4)
        self.port_entry.grid(column=1, row=1, columnspan=4)

        self.label_3.grid(column=0, row=2)
        self.label_4.grid(column=0, row=3)
        self.ip_other_entry.grid(column=1, row=2, columnspan=4)
        self.port_other_entry.grid(column=1, row=3, columnspan=4)
        self.confirm_button.grid(column=2, row=4)

    def send(self):
        global ip
        global port
        global ip_connect
        global port_connect

        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()
        ip_connect = self.ip_other_entry.get().strip()
        port_connect = self.port_other_entry.get().strip()

        if not validate_ip(ip) and validate_ip(ip_connect):
            self.ip_entry.delete(0, END)
            self.port_entry.delete(0, END)

            self.ip_entry.config(fg='#ff0000')
            self.ip_entry.insert(0, "Digite um endereço válido")

            self.ip_entry.bind('<Button-1>', self.delete_ip)
            self.ip_entry.bind('<Key>', self.delete_ip)

            self.ip_other_entry.delete(0, END)
            self.port_other_entry.delete(0, END)
            
            self.ip_other_entry.config(fg='#ff0000')
            self.ip_other_entry.insert(0, "Digite um endereço válido")

            self.ip_other_entry.bind('<Button-1>', self.delete_ip)
            self.ip_other_entry.bind('<Key>', self.delete_ip)

        elif not port.isdigit() or int(port) > 65535:
            self.ip_entry.delete(0, END)
            self.port_entry.delete(0, END)

            self.port_entry.config(fg='#ff0000')
            self.port_entry.insert(0, "Digite uma porta válida")

            self.port_entry.bind('<Button-1>', self.delete_port)
            self.port_entry.bind('<Key>', self.delete_port)

            self.ip_other_entry.delete(0, END)
            self.port_other_entry.delete(0, END)

            self.port_other_entry.config(fg='#ff0000')
            self.port_other_entry.insert(0, "Digite uma porta válida")

            self.port_other_entry.bind('<Button-1>', self.delete_port)
            self.port_other_entry.bind('<Key>', self.delete_port)

        else:
            self.clear()
            print((ip, int(port)))
            print((ip_connect, int(port_connect)))

            MainWindow(720, 540, self.title).start()       

    def clear(self):
        self.canva.destroy()


if __name__ == "__main__":
    start = Username(720, 540, 'Username').start()