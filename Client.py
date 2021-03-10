import socket
import threading
from tkinter import *
import tkinter.scrolledtext

host = '127.0.0.1'
port = 9090


class clinetttt:
    def __init__(self, HOST, PORT):
        self.gui_done = False
        self.running = True

        gui_threading = threading.Thread(target=self.gui_loop)
        running_threading = threading.Thread(target=self.receive)

        gui_threading.start()
        running_threading.start()

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((HOST, PORT))
        except:
            print("error")

    def gui_loop(self):
        self.root = Tk()
        self.root['background'] = "lightblue"
        self.root.geometry('500x630')
        self.root.maxsize(500, 630)
        self.root.minsize(500, 630)
        self.root.title('SecureChat Client - By Ritesh Kr. Gupta')

        self.chat_label = Label(self.root, text="CHAT:", bg='lightblue', font=(15,))
        self.chat_label.pack(padx=10, pady=5)

        self.chat = tkinter.scrolledtext.ScrolledText(self.root)
        self.chat.pack(padx=10, pady=5)
        self.chat.config(state='disable', bg='lightgreen')

        self.msg_label = Label(self.root, text='Message: ', bg='lightblue', font=(10,))
        self.msg_label.pack(padx=10, pady=5)

        self.text = tkinter.Text(self.root, height=3, bg='lightgreen')
        self.text.pack(padx=10, pady=5)

        self.button = Button(self.root, text='Send', bg='lightpink', width=15, height=1, font=("", 13), relief=SUNKEN,
                        command=self.send)
        self.button.pack(pady=15)

        self.gui_done = True

        self.root.protocol('WM_DELETE_WINDOW', self.stop)

        self.root.mainloop()

    def send(self):
        if self.gui_done:
            message = f"{self.text.get('1.0', 'end')}"
            self.chat.config(state='normal')
            self.chat.insert('end', "You : " + message)
            self.chat.yview('end')
            self.chat.config(state='disable')
            message = "Client: " + message
            self.client.send(message.encode('utf-8'))
            self.text.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.root.destroy()
        self.client.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if self.gui_done:
                    self.chat.config(state='normal')
                    self.chat.insert('end', message)
                    self.chat.yview('end')
                    self.chat.config(state='disable')
            except ConnectionError:
                break
            except:
                print("Connection Error")


clinetttt(host, port)
