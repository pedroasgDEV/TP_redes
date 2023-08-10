#BIBLIOTECAS
import threading
import socket
from sys import getsizeof

#MODULOS
import game

def Client(host = 'localhost', port = 1231):

    #Cria uma conexão TCP/IP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Tenta se conectar ao servidor
    try:
        client.connect((host, port))
    except:
        return print('Não foi possível se conectar ao servidor!') 
    
    #Selecionar o nome
    username = input('Seu nome: ')
    
    #Selecionar o personagem
    i = 0
    for char in game.characters:
        print(f'{i}- {char}')
        i += 1
    i = int(input('Digite o numero do seu personagem: '))
    while (i > 6 or i < 0):  i = int(input('ERRO: Digite o numero do seu personagem: '))
    character = game.characters[i] 
    
    #Cria Personagem
    player = game.Player(username, character)
    
    #Envia dados para o servidor
    print('\nConectado')

    #inicia as threads
    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client, player])

    thread1.start()
    thread2.start()

def receiveMessages(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print(msg+'\n')
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            client.close()
            break
            

def sendMessages(client, player):
    while True:
        try:
            msg = input('\n')
            client.send(f'{player.username} ({player.character}): {msg}'.encode('utf-8'))
        except:
            return


Client()