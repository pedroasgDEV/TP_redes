#BIBLIOTECAS
import threading
import socket

#MODULOS
import game

#VETORES GLOBAIS
game_rooms = [] #salas de jogo
waiting_room = [] #jogadores na sala de espera

def Server(host = 'localhost', port = game.default_port):

    #Cria uma conexão TCP/IP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Tenta iniciar o servidor
    try:
        server.bind((host, port))
        server.listen()
    except:
        return print('\nNão foi possível iniciar o servidor!\n')

    
    while True:
        client, addr = server.accept() #aceita novo cliente
        
        #Recebe os dados do cliente
        username, character = client.recv(2048).decode('utf-8').split('/')

        #Cria um player
        player = game.Player(username, character, client)
        
        #coloca o novo cliente em uma threading
        threading.Thread(target=room_selector, args=[player]).start()

#Aloca o usuario em uma sala
def room_selector(player):
    while True:
        #Adiciona o cliente a sala de esperar
        waiting_room.append(player)
        
        #Monte a mensagem com as salas
        msg = montar_msg().encode('utf-8')
        
        #manda a mensagem para o cliente
        player.client.send(msg)
        
        #verifica o recebimento
        repeat = True #Possibilidades
        while (repeat):
            
            #Recebe a mensagem
            sala_id, senha = player.client.recv(2048).decode('utf-8').split('/')
            
            #Se for criar uma nova sala
            if(sala_id == "0"): 
                repeat = False
                waiting_room.remove(player)
                new_room(player)
            
            #Procura a sala
            else:
                for sala in game_rooms:    
                    #Se encontrou a sala
                    if(sala.isFull == False and sala.sala_id == int(sala_id) and sala.senha == senha): 
                        repeat = False
                        waiting_room.remove(player)
                        conect_room(player, sala)
                        break
                    
            if(repeat == True): #Se não tiver conseguido encontrar a sala manda uma mensagem de erro
                player.client.send("-1".encode('utf-8'))    
                
#Cria uma nova sala
def new_room(player):
    #envia mesagem para criar outra sala
    player.client.send("1".encode('utf-8'))
    
    #clinte recebe mensagem com os dados da sala
    nome, senha = player.client.recv(2048).decode('utf-8').split('/')
    
    #Cria uma nova sala
    game.salas_id += 1
    new_room = game.Room(nome, player, senha)
    game_rooms.append(new_room)
    
    #Informa ao cliente que se conectou a sala e direciona para o jogo
    player.client.send(f"Sala criada com sucesso".encode("utf-8"))
    play_game(new_room)
    

def conect_room(player, sala):
    #envia mesagem de conecxão a uma sala
    player.client.send("2".encode('utf-8'))
    
    #Adiciona o jogador a sala e marca ela como completa
    sala.players.append(player)
    sala.isFull = True

    #Informa ao cliente que se conectou a sala e direciona para o jogo
    player.client.send(f"\nSe conectou a sala com sucesso".encode("utf-8"))
    play_game(sala)
    
#Monte a mensagem com as salas
def montar_msg():
    msg = "\nSelecione uma sala:\n0 - Nova Sala\n"  
    for sala in game_rooms:
        if(sala.isFull == False): #Para imprimir somente as salas com vafa
            msg += f'ID: {sala.sala_id} -- Nome: {sala.nome} \n'
    return msg

#Joga o jogo
def play_game(sala):
    while True:
        #Espera algum jogador entrar
        while(sala.isFull == False): pass
        
        #Avisa os jogadores com quem estão jogando
        sala.players[0].client.send(f"\nO jogo irá comceçar\nVocê está jogando com {sala.players[1].username} ({sala.players[1].character})".encode('utf-8'))
        sala.players[0].vidas = 3
        sala.players[1].client.send(f"\nO jogo irá comceçar\nVocê está jogando com {sala.players[0].username} ({sala.players[0].character})".encode('utf-8'))
        sala.players[1].vidas = 3
        
        #Inicia o jogo
        while sala.isFull == True:
            #Recebe as jogadas
            sala.players[0].client.send(f"Sua vez de jogar\n".encode('utf-8'))
            sala.players[0].card = sala.players[0].client.recv(2048).decode('utf-8')
            sala.players[1].client.send(f"Sua vez de jogar\n".encode('utf-8'))
            sala.players[1].card = sala.players[1].client.recv(2048).decode('utf-8')
            
            #Anuncia as jogadas
            sala.players[0].client.send(f"\nJogador {sala.players[1].username} ({sala.players[1].character}) jogou {sala.players[1].card}".encode('utf-8'))
            sala.players[1].client.send(f"\nJogador {sala.players[0].username} ({sala.players[0].character}) jogou {sala.players[0].card}".encode('utf-8'))
            
            verifica_jogadas(sala)            
            
#Verifica as jogadas
def verifica_jogadas(sala):
    #Se o jogardor 0 jogar pedra
    if(sala.players[0].card == "Pedra"):
        #Empate
        if(sala.players[1].card == "Pedra"):
            for player in sala.players:
                player.client.send("Foi um empate".encode('utf-8'))
        
        #Vitoria jogador 1
        elif(sala.players[1].card == "Papel"):
            for player in sala.players:
                player.client.send(f"Papel cobre pedra\n{sala.players[1].username} ({sala.players[1].character}) Ganhou".encode('utf-8'))
            sala.players[0].vidas -= 1 #Retira uma vida do jogador 0
                
        #Vitoria jogador 0
        elif(sala.players[1].card == "Tesoura"):
            for player in sala.players:
                player.client.send(f"Pedra amassa tesoura\n{sala.players[0].username} ({sala.players[0].character}) Ganhou".encode('utf-8'))
            sala.players[1].vidas -= 1 #Retira uma vida do jogador 1
        
        #Vitoria jogador 0
        elif(sala.players[1].card == "Lagarto"):
            for player in sala.players:
                player.client.send(f"Pedra esmaga lagarto\n{sala.players[0].username} ({sala.players[0].character}) Ganhou".encode('utf-8'))
            sala.players[1].vidas -= 1 #Retira uma vida do jogador 1
        
        #Vitoria jogador 1
        elif(sala.players[1].card == "Spock"):
            for player in sala.players:
                player.client.send(f"Spock vaporiza pedra\n{sala.players[1].username} ({sala.players[1].character}) Ganhou".encode('utf-8'))
            sala.players[0].vidas -= 1 #Retira uma vida do jogador 0
    
    if(sala.players[0].card == "Papel"):
        
        #Vitoria do jogador 0
        if(sala.players[1].card == "Pedra"):
            for player in sala.players:
                player.client.send(f"Papel cobre pedra\n{sala.players[0].username} ({sala.players[0].character}) Ganhou".encode('utf-8'))
            sala.players[1].vidas -= 1 #Retira uma vida do jogador 1
        
        #Empate
        elif(sala.players[1].card == "Papel"):
            for player in sala.players:
                player.client.send("Foi um empate".encode('utf-8'))
        
        #Vitoria do jogador 1 
        elif(sala.players[1].card == "Tesoura"):
            for player in sala.players:
                player.client.send(f"Tesoura corta papel\n{sala.players[1].username} ({sala.players[1].character}) Ganhou".encode('utf-8'))
            sala.players[0].vidas -= 1 #Retira uma vida do jogador 0
        
        #Vitoria do jogador 1
        elif(sala.players[1].card == "Lagarto"):
            for player in sala.players:
                player.client.send(f"Lagarto come papel\n{sala.players[1].username} ({sala.players[1].character}) Ganhou".encode('utf-8'))
            sala.players[0].vidas -= 1 #Retira uma vida do jogador 0
        
        #Vitoria do jogador 0
        elif(sala.players[1].card == "Spock"):
            for player in sala.players:
                player.client.send(f"Papel refuta Spock\n{sala.players[0].username} ({sala.players[0].character}) Ganhou".encode('utf-8'))
            sala.players[1].vidas -= 1 #Retira uma vida do jogador 1
        
    elif(sala.players[0].card == "Tesoura"):
        
        #Vitoria do jogador 1
        if(sala.players[1].card == "Pedra"):
            for player in sala.players:
                player.client.send(f"Pedra amassa tesoura\n{sala.players[1].username} ({sala.players[1].character}) Ganhou".encode('utf-8'))
            sala.players[0].vidas -= 1 #Retira uma vida do jogador 0
        
        #Vitoria do jogador 0
        elif(sala.players[1].card == "Papel"):
            for player in sala.players:
                player.client.send(f"Tesoura corta papel\n{sala.players[0].username} ({sala.players[0].character}) Ganhou".encode('utf-8'))
            sala.players[1].vidas -= 1 #Retira uma vida do jogador 1
        
        #Empate
        elif(sala.players[1].card == "Tesoura"):
            for player in sala.players:
                player.client.send("Foi um empate".encode('utf-8'))
        
        #Vitoria do jogador 0   
        elif(sala.players[1].card == "Lagarto"):
            for player in sala.players:
                player.client.send(f"Tesoura decapita lagarto\n{sala.players[0].username} ({sala.players[0].character}) Ganhou".encode('utf-8'))
            sala.players[1].vidas -= 1 #Retira uma vida do jogador 1
        
        #Vitoria do jogador 1
        elif(sala.players[1].card == "Spock"):
            for player in sala.players:
                player.client.send(f"Spock derrete tesoura\n{sala.players[1].username} ({sala.players[1].character}) Ganhou".encode('utf-8'))
            sala.players[0].vidas -= 1 #Retira uma vida do jogador 0
        
    elif(sala.players[0].card == "Lagarto"):
        
        #Vitoria do jogador 1
        if(sala.players[1].card == "Pedra"):
            for player in sala.players:
                player.client.send(f"Pedra esmaga lagarto\n{sala.players[1].username} ({sala.players[1].character}) Ganhou".encode('utf-8'))
            sala.players[0].vidas -= 1 #Retira uma vida do jogador 0
        
        #Vitoria do jogador 0
        elif(sala.players[1].card == "Papel"):
            for player in sala.players:
                player.client.send(f"Lagarto come papel\n{sala.players[0].username} ({sala.players[0].character}) Ganhou".encode('utf-8'))
            sala.players[1].vidas -= 1 #Retira uma vida do jogador 1
        
        #Vitoria do jogador 1
        elif(sala.players[1].card == "Tesoura"):
            for player in sala.players:
                player.client.send(f"Tesoura decapita lagarto\n{sala.players[1].username} ({sala.players[1].character}) Ganhou".encode('utf-8'))
            sala.players[0].vidas -= 1 #Retira uma vida do jogador 0
        
        #Empate
        elif(sala.players[1].card == "Lagarto"):
            for player in sala.players:
                player.client.send("Foi um empate".encode('utf-8'))
        
        #Vitoria do jogador 0   
        elif(sala.players[1].card == "Spock"):
            for player in sala.players:
                player.client.send(f"Lagarto envenena Spock\n{sala.players[0].username} ({sala.players[0].character}) Ganhou".encode('utf-8'))
            sala.players[1].vidas -= 1 #Retira uma vida do jogador 1
        
    elif(sala.players[0].card == "Spock"):
        
        #Vitoria do jogador 0
        if(sala.players[1].card == "Pedra"):
            for player in sala.players:
                player.client.send(f"Spock vaporiza pedra\n{sala.players[0].username} ({sala.players[0].character}) Ganhou".encode('utf-8'))
            sala.players[1].vidas -= 1 #Retira uma vida do jogador 1
        
        #Vitoria do jogador 1
        elif(sala.players[1].card == "Papel"):
            for player in sala.players:
                player.client.send(f"Papel refuta Spock\n{sala.players[1].username} ({sala.players[1].character}) Ganhou".encode('utf-8'))
            sala.players[0].vidas -= 1 #Retira uma vida do jogador 0
        
        #Vitoria do jogador 0
        elif(sala.players[1].card == "Tesoura"):
            for player in sala.players:
                player.client.send(f"Spock derrete tesoura\n{sala.players[0].username} ({sala.players[0].character}) Ganhou".encode('utf-8'))
            sala.players[1].vidas -= 1 #Retira uma vida do jogador 1
        
        #Vitoria do jogador 1
        elif(sala.players[1].card == "Lagarto"):
            for player in sala.players:
                player.client.send(f"Lagarto envenena Spock\n{sala.players[1].username} ({sala.players[1].character}) Ganhou".encode('utf-8'))
            sala.players[0].vidas -= 1 #Retira uma vida do jogador 0
        
        #Empate
        elif(sala.players[1].card == "Spock"):
            for player in sala.players:
                player.client.send("Foi um empate".encode('utf-8'))
            
            

Server()