import socket
import threading

HOST='127.0.0.1'
PORT=55555

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()

salas = {}


def broadcast(sala,mensagem):
    for i in salas[sala]:
        if isinstance(mensagem, str):
            mensagem = mensagem.encode()
        i.send(mensagem)

def enviarMensagem(nome, sala , client):
    while True:
        mensagem = client.recv(1024)
        mensagem = f'{nome}: {mensagem.decode()}\n'
        broadcast(sala,mensagem)

while True:
    cliente, addr =server.accept()
    cliente.send(b'SALA')
    sala = cliente.recv(1024).decode()
    nome = cliente.recv(1024).decode()
    if sala not in salas.keys():
        salas[sala] = []
    salas[sala].append(cliente)
    print(f'{nome} se conectou na sala {sala} ! INFO {addr}')
    broadcast(sala, f'{nome} : Entrou na sala !\n')
    thread =threading.Thread(target=enviarMensagem,args=(nome , sala,cliente))
    thread.start()