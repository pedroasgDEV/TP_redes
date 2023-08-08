import socket
import threading
import time

def client(): 
    # Cria uma conexão TCP/IP 
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # Tenta conectar ao servidor
    host = '200.239.138.242'
    port = 7777
    
   
    try: 
        sock.connect((host, port))      
    except: 
        return print ("Não foi possivel se conectar") 
    
    nome = input("Qual seu nome?")
    print("/n Conexão estabelecida")
    
    threading.Thread(target=MandarMensagem, args=[cliente, nome]).start()
    threading.Thread(target=ReceberMensagem, args=[cliente]).start()
    

def MandarMensagem(cliente, nome):
    while True:
        try:
            msg = input("/n Escolha (Pedra, Papel, Tesoura, Largato, Spock)\n")
            cliente.send("<{nome}> {msg}".encode('utf-8'))
        except:
            return

def ReceberMensagem(cliente):
    while True:
        try:
            msg = cliente.recv(2048).decode('utf-8')
            print("\n <SERVIDOR> {msg}")
        except:
            print("\nConexão perdida\n")
            cliente.close()
            break          



client()