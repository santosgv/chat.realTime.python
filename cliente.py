import socket
import threading
from tkinter import *
import tkinter
from tkinter import simpledialog

class Chat:
    def __init__(self):
        HOST = '127.0.0.1'
        PORT = 55555
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        login = Tk()
        login.withdraw()
        self.janela_carregada =False
        self.ativo = True

        self.nome = simpledialog.askstring('Nome','Digite seu Nome',parent=login)
        self.sala = simpledialog.askstring('Grupo', 'Digite o grupo', parent=login)

        thread= threading.Thread(target=self.conecta)
        thread.start()
        self.janela()

    def janela(self):
        self.root =Tk()
        self.root.geometry('800x800')
        self.root.title('Chat')
        self.caixa_texto=Text(self.root,background="black", foreground="green")
        self.caixa_texto.place(relx=0.05, rely=0.08, width=700,height=600)

        self.scroller = Scrollbar(self.root)
        self.scroller.place(relx=0.900, rely=0.08, width=20,height=600)
        self.scroller.config(command=self.caixa_texto.yview)
        self.caixa_texto.config(yscrollcommand = self.scroller.set)

        self.envia_mensagem= Entry(self.root)
        self.envia_mensagem.place(relx=0.05, rely=0.9, width=500,height=20)

        self.btn_envia =Button(self.root,text='Envia',command=self.enviarMensagem)
        self.btn_envia.place(relx=0.7, rely=0.9, width=100,height=20)
        self.root.protocol(self.fechar)

        self.root.mainloop()

    def fechar(self):
        self.client.close()
        self.root.destroy()


    def conecta(self):
        while True:
            recebido = self.client.recv(1024)
            if recebido ==b'SALA':
                self.client.send(self.sala.encode())
                self.client.send(self.nome.encode())
            else:
                try:
                    self.caixa_texto.insert('end', recebido.decode())
                except:
                    pass

    def enviarMensagem(self):
        mensagem = self.envia_mensagem.get()
        self.client.send(mensagem.encode())
        mensagem =self.envia_mensagem.delete(0,END)

Chat()