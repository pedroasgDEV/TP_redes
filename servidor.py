
import threading
import socket

clientes = []

def server(host = 'localhost', port=8082):
    # Cria uma conexão TCP/IP 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Tenta iniciar o servidor
    try:
        server.bind((host, port))
        server.listen()
    except:
        return print('\nNão foi possível iniciar o servidor!\n')

    
    while True:
        cliente, addr = server.accept()
        clientes.append(cliente)

        threading.Thread(target=messagesTreatment, args=[cliente]).start()

def messagesTreatment(cliente):
    while True:
        try:
            msg = cliente.recv(2048)
            broadcast(msg, cliente)
        except:
            deleteCliente(cliente)
            break


def broadcast(msg, cliente):
    for clienteItem in clientes:
        if clienteItem != cliente:
            try:
                clienteItem.send(msg)
            except:
                deleteCliente(clienteItem)


def deleteCliente(cliente):
    clientes.remove(cliente)
            
server()