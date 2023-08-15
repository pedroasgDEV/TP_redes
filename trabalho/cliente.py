#BIBLIOTECAS
import socket

#MODULOS
import game

def Client(host = 'localhost', port = game.default_port):

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
    
    #Cria um player
    player = game.Player(username, character, client)
    
    #tenta enviar as informações para o sevidor
    try:
        msg = username + '/' + character #junta as infomações para facilitar o envio
        client.send(msg.encode('utf-8'))
        print('\nConectado')
    except:
        return print("Falha na comunicação")
    
    conect_room(player)
        
def conect_room(player):
    #tenta se conectar a uma sala
    while True:
        
        #recebe uma lista com salas disponiveis
        try:
            msg = player.client.recv(2048).decode('utf-8')
            print(msg)
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            return player.client.close()
        
        while True:
            #O usuario vai selecionar a sala
            sala_id = input("\n\nDigite o ID: ")
            if(sala_id == "0"): #Se for criar outra sala
                player.client.send((sala_id + '/' + "1234").encode('utf-8'))
            else: #Se for entrar em uma sala já existente
                senha = input("Digite a senha: ")
                player.client.send((sala_id + '/' + senha).encode('utf-8'))
            
            #O cliente recebe uma mensagem do servidor
            msg = player.client.recv(2048).decode('utf-8')
            
            #Caso for criar uma sala
            if(msg == "1"):
                nome = input("\nDigite o nome da sala: ")
                senha = input("\nDigite a senha da sala: ")
                player.client.send((nome + '/' + senha).encode('utf-8'))
                print(player.client.recv(2048).decode('utf-8'))
                play_game(player)
                break
            
            #Caso se conecte a uma sala
            elif(msg == "2"):
                print(player.client.recv(2048).decode('utf-8'))
                play_game(player)
                break
                
            #Caso tenha dado erro
            else:
                print("ERRO!!! ID ou senha incorretos")
            
def play_game(player):
    #Imprime que o jogo começou
    print(player.client.recv(2048).decode('utf-8'))
    
    #Jogo se inicia
    while True:
        
        print("\n" + player.client.recv(2048).decode('utf-8'))
        #Imprime as possiveis jogadas    
        i = 0
        for cards in game.cards:
            print(f"{i}- {cards}")
            i += 1
        i = int(input('Qual sua jogada? '))
        while (i > 4 or i < 0):  i = int(input('ERRO: Qual sua jogada? '))
        #envia a escolha do jogador
        player.client.send(game.cards[i].encode('utf-8'))
        
        #Recebe o que o outro jogador jogou
        print("\n" + player.client.recv(2048).decode('utf-8'))
        
        #Recebe resultado da rodada
        print("\n" + player.client.recv(2048).decode('utf-8'))
        


Client()