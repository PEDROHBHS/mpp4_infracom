from tkinter import *
from tkinter.filedialog import askopenfilename
from datetime import datetime
from PIL import Image, ImageTk
from VideoPlayer import VideoPlayer
from ServerP2P import ServerP2P
from Client import Client
from Window import Window
from SenderUDP import SenderUDP
from ReceiverUDP import ReceiverUDP
import threading
import re


def validate_ip(str):
    return bool(re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", str)) or (str == "localhost")

filetypes = {
    'Images': ('.png', '.gif', '.jpg', '.jpeg'),
    'Videos': ('.mp4', '.avi', '.mkv'),
    'Audios': ('.mp3',)
}

filetype_list = [(t, f'*{e}') for t in filetypes.keys() for e in filetypes[t]]

def select_file():
    return askopenfilename(
        title='Choose a file',
        initialdir='/',
        filetypes=filetype_list
        )

class MainWindow(Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.serverChecker = False
        self.const = 0
        try:
            self.client = Client(
                ip, int(port), (ip_connect, int(port_connect)))
            self.const = 1
        except:
            self.server = ServerP2P(ip, int(port))
            self.serverChecker = True

        self.sum_port = (int(port_connect) + int(port)) % 65535
        self.udp_receiver = ReceiverUDP(ip, self.sum_port + 3 + self.const, ip_connect, self.sum_port + 4 + self.const)

        threading.Thread(target=self.udp_receiver.receive).start()
        threading.Thread(target=self.receive, daemon=True).start()

    def clear_txt(self):
        self.txt_area.config(state='normal')
        self.txt_area.delete("1.0", END)
        self.txt_area.config(state='disabled')

    def create_file(self):
        file = select_file()

        self.udp_sender = SenderUDP(ip_connect, self.sum_port + 1 + self.const, ip, self.sum_port + 2 + self.const, file)
        threading.Thread(target=self.udp_sender.send).start()

        if file.endswith(filetypes['Images']):
            global pack_img

            img = Image.open(file).resize((200, 200))
            pack_img = ImageTk.PhotoImage(img)
            self.txt_area.image_create(END, image=pack_img)

        elif file.endswith(filetypes['Videos']):
            VideoPlayer(self.txt_area, file)

        self.txt_area.config(state='normal')
        self.txt_area.insert(END, '\n')
        self.txt_area.config(state='disabled')
        

    def create_widgets(self):
        self.txt_area = Text(self.canva, border=1, wrap='word',
                             background='#c8a2c8', state='disabled')
        self.txt_field = Entry(self.canva, width=85, border=1, bg='white')
        self.send_button = Button(self.canva, text='Enviar', padx=40)
        self.archive_button = Button(self.canva, text='Anexar', padx=40, command=self.create_file)

        self.send_button.bind('<Button-1>', self.send)
        self.txt_field.bind('<Return>', self.send)

        self.menubar = Menu(self.window)
        self.chat_menu = Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label='Chat', menu=self.chat_menu)
        self.chat_menu.add_command(label='Clear', command=self.clear_txt)

        self.window.config(menu=self.menubar)

        self.scroll = Scrollbar(
            self.canva, orient=VERTICAL, command=self.txt_area.yview)
        self.txt_area.config(yscrollcommand=self.scroll.set)
        self.scroll.grid(column=5, row=0, sticky=(N, S))

        self.txt_area.grid(column=0, row=0, columnspan=6)
        self.txt_field.grid(column=0, row=1, columnspan=3)
        self.send_button.grid(column=4, row=1)
        self.archive_button.grid(column=3, row=1)
    

    def send(self, event):
        txt = self.txt_field.get()

        if txt.strip() == '':
            return

        def send_msg():
            dt = datetime.now()
            date = dt.strftime("%m-%d-%Y %H:%Mh")
            msg = f'-> {username} [{date}] : {txt}'

            if self.serverChecker:
                self.server.send(msg)
            else:
                self.client.send(msg)

            self.txt_area.config(state='normal')
            self.txt_area.insert(END, msg + '\n')
            self.txt_area.config(state='disabled')
            self.txt_field.delete(0, END)

        threading.Thread(target=send_msg).start()

    def receive(self):
        while True:
            dt = datetime.now()
            date = dt.strftime("%m-%d-%Y %H:%Mh")

            if self.serverChecker:
                msg = self.server.receive()
            else:
                msg = self.client.receive()

            if msg is None:
                break
        
            msg_date, msg_rcv = msg.split(' : ')
            msg_rcv = f'{msg_date}-[{date}] : {msg_rcv}'

            self.txt_area.config(state='normal')
            self.txt_area.insert(END, msg_rcv + '\n')
            self.txt_area.config(state='disabled')

class Username(Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

    def create_widgets(self):
        self.usernameLabel = Label(self.canva, text = 'Username:')
        self.usernameLabel.pack(padx=15,pady= 5)
        self.usernameEntry = Entry(self.canva, bd =5)
        self.usernameEntry.pack(padx=15, pady=5)
        
        self.create_button = Button(self.canva, text='Create')
        self.create_button.pack(side = LEFT , padx = 60)

        self.create_button.bind('<Button-1>', self.send)
        self.usernameEntry.bind('<Return>', self.send)

    def send(self, event):
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

    def delete_ip(self, event, ip_entry):
        ip_entry.delete(0, END)
        ip_entry.config(fg='#000000')
        ip_entry.unbind('<Button-1>')
        ip_entry.unbind('<Key>')

    def delete_port(self, event, port_entry):
        port_entry.delete(0, END)
        port_entry.config(fg='#000000')
        port_entry.unbind('<Button-1>')
        port_entry.unbind('<Key>')

    def invalid_ip(self, ip_entry):
        ip_entry.delete(0, END)

        ip_entry.config(fg='#ff0000')
        ip_entry.insert(0, "Digite um endereço válido")

        ip_entry.bind('<Button-1>', lambda e: self.delete_ip(event=e, ip_entry=ip_entry))
        ip_entry.bind('<Key>', lambda e: self.delete_ip(event=e, ip_entry=ip_entry))

    def invalid_port(self, port_entry):
        port_entry.delete(0, END)

        port_entry.config(fg='#ff0000')
        port_entry.insert(0, "Digite uma porta válida")

        port_entry.bind('<Button-1>', lambda e: self.delete_port(event=e, port_entry=port_entry))
        port_entry.bind('<Key>', lambda e: self.delete_port(event=e, port_entry=port_entry))

    def create_widgets(self):
        self.label_1 = Label(self.canva, text='Ip Address')
        self.label_2 = Label(self.canva, text='Port')
        self.label_3 = Label(self.canva, text='Ip Address of connection')
        self.label_4 = Label(self.canva, text='Port of connection')

        self.ip_entry = Entry(self.canva, width=85, border=1, bg='white')
        self.port_entry = Entry(self.canva, width=85, border=1, bg='white')
        self.ip_other_entry = Entry(self.canva, width=85, border=1, bg='white')
        self.port_other_entry = Entry(self.canva, width=85, border=1, bg='white')
        self.confirm_button = Button(self.canva, text='Confirm', padx=40)
        self.confirm_button.bind('<Button-1>', self.send)
        self.confirm_button.bind('<Return>', self.send)

        self.label_1.grid(column=0, row=0)
        self.label_2.grid(column=0, row=1)
        self.ip_entry.grid(column=1, row=0, columnspan=4)
        self.port_entry.grid(column=1, row=1, columnspan=4)

        self.label_3.grid(column=0, row=2)
        self.label_4.grid(column=0, row=3)
        self.ip_other_entry.grid(column=1, row=2, columnspan=4)
        self.port_other_entry.grid(column=1, row=3, columnspan=4)
        self.confirm_button.grid(column=2, row=4)

    def send(self, event):
        global ip
        global port
        global ip_connect
        global port_connect

        valid = True

        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()
        ip_connect = self.ip_other_entry.get().strip()
        port_connect = self.port_other_entry.get().strip()

        if not validate_ip(ip):
            valid = False
            self.invalid_ip(self.ip_entry)

        if not validate_ip(ip_connect):
            valid = False
            self.invalid_ip(self.ip_other_entry)

        if not port.isdigit() or int(port) > 65535:
            valid = False
            self.invalid_port(self.port_entry)

        if not port_connect.isdigit() or int(port_connect) > 65535:
            valid = False
            self.invalid_port(self.port_other_entry)

        if valid:
            self.clear()
            print((ip, int(port)))
            print((ip_connect, int(port_connect)))

            MainWindow(720, 540, self.title).start()    

    def clear(self):
        self.canva.destroy()


if __name__ == "__main__":
    start = Username(720, 540, 'Username').start()
