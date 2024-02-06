import threading
import socket
import random

class Carta( object ):
  def __init__(self, nome, valor, naipe, simbolo):
    self.valor = valor
    self.naipe = naipe
    self.nome = nome
    self.simbolo = simbolo
    self.mostrar = False

  #Função para mostrar mostrar as carta
  def __repr__(self):
    if self.mostrar:
      return self.simbolo
    else:
      return "Carta"
    
class Baralho( object ):
    #Embaralha o baralho
    def embaralha(self, times = 1 ):
        random.shuffle(self.cartas)
        #Faz permutações aleatorias com as cartas

    #Entrega uma carta e a retira do deck inicial
    def retira(self):
        return self.cartas.pop(0)

#Essa classe cria um baralho inicial
class BaralhoInicial( Baralho ):
    def __init__(self):
        self.cartas = []
        naipes = {"Copas":"♡", "Espadas":"♠", "Ouros":"♢", "Paus":"♣"}
        valores = {"Dois":2, "Tres":3, "Quatro":4, "Cinco":5, "Seis":6, "Sete":7, "Oito":8,
                   "Nove":9, "Dez":10, "Jack":11, "Queen":12, "King":13, "Ace":14 }
        #Cria um baralho combinando todos nomes\valores com os naipes/simbolos
        for nome in valores:
            for naipe in naipes:
                icone = naipes[naipe]
                if valores[nome] < 11:
                    simbolo = str(valores[nome])+icone
                else:
                    simbolo = nome[0]+icone
                self.cartas.append( Carta(nome, valores[nome], naipe, simbolo) )

class Pontuacao(object):
    def __init__(self, cartas):
        self.cartas = cartas
    
    #Flush são 5 cartas do mesmo naipe
    def flush(self):
        naipes = [carta.naipe for carta in self.cartas]
        valores = [carta.valor for carta in self.cartas]
        maiorValor = 0
        #Verifica se só possui um naipe
        if len( set(naipes) ) == 1:
            for valor in valores:
                if valor > maiorValor:
                    maiorValor = valor
            return maiorValor
        
        return False
    
    #straight são 5 valores seguidos
    def straight(self):
        valores = [carta.valor for carta in self.cartas]
        valores.sort()

        #Se não tiver 5 valores diferentes
        if not len( set(valores)) == 5:
            return False 
        
        #Trata a exceção do A que em uma mão de straight pode começar e terminar uma sequencia
        if valores[4] == 14 and valores[0] == 2 and valores[1] == 3 and valores[2] == 4 and valores[3] == 5:
            return 5

        else:
            if not valores[0] + 1 == valores[1]: return False 
            if not valores[1] + 1 == valores[2]: return False
            if not valores[2] + 1 == valores[3]: return False
            if not valores[3] + 1 == valores[4]: return False

        return valores[4]
    
    #Retorna a maior carta
    def cartaMaisAlta(self):
        valores = [carta.valor for carta in self.cartas]
        maiorCarta = None
        for carta in self.cartas:
            if maiorCarta is None:
                highcarta = carta
            elif maiorCarta.valor < carta.valor: 
                maiorCarta = carta

        return maiorCarta
         
    #Verifica se há uma quadrupla no deck
    def quadra(self):
        valores = [carta.valor for carta in self.cartas]
        for valor in valores:
            if valores.count(valor) == 4:
                return valor
        return False

    #Retorna os pares
    def pares(self):
        par = []
        valores = [carta.valor for carta in self.cartas]
        for valor in valores:
            if valores.count(valor) == 2 and valor not in par:
                par.append(valor)
        par.sort()
        return par
    
    #FullHouse é qnd tem 2 cartas com o msm valor e 3 tres com outro msm valor
    def fullHouse(self):
        dois = False
        tres = False
        val3 = 0

        valores = [carta.valor for carta in self.cartas]
        for valor in valores:
            if valores.count(valor) == 2:
                dois = True
            if valores.count(valor) == 3:
                tres = True
                val3 = valor
                
        if dois and tres: return val3
        else: return False

    def trinca(self):
        valores = [carta.valor for carta in self.cartas]
        for valor in valores:
            if valores.count(valor) == 3:
                return valor
        return False
    
    #Pontua a mão
    def pontua(self):
        pontos = 0 #incia com 0
        straight = self.straight()
        flush = self.flush()
        quadra = self.quadra()
        fullHouse = self.fullHouse()
        trinca = self.trinca()
        pares = self.pares()

        # Royal flush
        if straight and flush and straight == 14:
            pontos += 1000

        # Straight flush
        elif straight and flush:
            pontos += 900 + straight

        # Quadra
        elif quadra:
            pontos += 800 + quadra

        # Full House
        elif fullHouse:
            pontos += 700 + fullHouse

        # Flush
        elif flush:
            pontos += 600 + flush

        # Straight
        elif straight:
            pontos += 500 + straight 

        # Trinca
        elif trinca:
            pontos += 400 + trinca

        # 2 par
        elif len(pares) == 2:
            pontos += 300 + pares[1]

        # 1 par
        elif len(pares) > 0:
            pontos += 200 + pares[0]
            
        # Maior carta
        else:
            valores = [carta.valor for carta in self.cartas]
            for valor in valores:
                if valor > pontos:
                    pontos = valor
            pontos += 100
            
        return pontos

playstate = False
players = []

class Player(object):
    def __init__(self, nome):
        self.nome = nome
        self.cartas = []
        self.apostas = 0
        self.carteira = 1024
        self.deller = False
    
    #Dá uma carta ao player
    def addCard(self, card):
        self.cartas.append(card)
    
    def fazerAposta(self, valor):
        #Caso o valor utrapasse a quantidade na carteira
        if(valor > self.carteira): return False
        self.carteira -= valor
        self.apostas += valor
        
def serverInit(address, port):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #cria o primeiro Jogador
    name = input('Digite seu nome: ')
    jogador1 = Player(name)
    players.append(jogador1)
    
    try:
        server.bind((address, port))
        server.listen(10)
    except:
        return print('\nNão foi possível iniciar o jogo!\n')

    while True:
        client, addr = server.accept()
        messagesTreatment(client)

def messagesTreatment(client):
    #tenta receber o nome do jogador
    try:
        #receber o nome do jogador
        nome = client.recv(2048).decode('utf-8')
    except:
        return

    #Cria o jogador
    player = Player(nome)
    players.append(player)
        
    #inciajogo 
    JogoInit(client)    

def JogoInit(client):
    
    apostaInit = 1
    
    while True:
        print("\nInicio do jogo de poker\n")

            
        #Inicia e embaralha o baralho
        baralho = BaralhoInicial()
        baralho.embaralha()
        
        #Dá as cartas para os jogadores
        for player in players:
            for i in range(5):
                player.addCard(baralho.retira())
            for cartas in player.cartas:
                cartas.mostrar = True
                
        apostaInit = ConectBetting(client, apostaInit)
        
        apostaInit = betting(client, apostaInit)
        
        #Showdown
        
        msg = f"\n<{players[0].nome}> {players[0].cartas}\n"
        msg += f"<{players[1].nome}> {players[1].cartas}\n"
        
        print(msg)
        client.send(msg.encode('utf-8'))
        
        score1 = Pontuacao(players[0].cartas).pontua()
        score2 = Pontuacao(players[1].cartas).pontua()
        
        if score1 > score2 :
            msg = f"{players[0].nome} ganhou"
            players[0].carteira += players[0].apostas + players[1].apostas
        
        elif score1 < score2 :
            msg = f"{players[1].nome} ganhou"
            players[1].carteira += players[0].apostas + players[1].apostas
        
        else:
            msg = "Houve um Empate"
            players[1].carteira += players[1].apostas
            players[0].carteira += players[0].apostas
            
        print(f"\n\n{msg} \n")
        client.send(msg.encode('utf-8'))
            
        players[0].cartas = []
        players[1].cartas = []
    
def betting(client, apostaInit):
    
    print(players[0].cartas)
    print(f"Carteira: {players[0].carteira}")
    print(f"Suas apostas: {1024 - int(players[0].carteira)}")  
    print(f"\n1) Fazer uma aposta de ({apostaInit})")
    print("2) Dobrar a aposta")
    print("3) Sair\n\n")
    
    entrada = int(input("Digite uma resposta: "))
    while entrada < 1 or entrada > 3:
        entrada = int(input("Digite uma resposta valida: "))
    
    if(entrada == 1):
        client.send(f"<{players[1].nome}> apostou {apostaInit}\n".encode('utf-8'))
        players[1] #Tenta receber a msg
        try:
            msg = client.recv(2048).decode('utf-8')
        except:
            client.close()
            
        print(f"\n{msg} \n").fazerAposta(apostaInit)
        return apostaInit
    elif(entrada == 2):
        client.send(f"<{players[1].nome}> apostou {apostaInit * 2}\n".encode('utf-8'))
        players[1].fazerAposta(apostaInit*2)
        return apostaInit * 2
    else:
        client.send("fim de jogo".encode('utf-8'))
        fimdejogo(client)
             
def ConectBetting(client, apostaInit):
    #Manda uma string com as cartas
    msg = f"{players[1].cartas} \n"
    msg += f"Carteira: {players[1].carteira}\n"
    msg += f"Suas apostas: {1024 - int(players[0].carteira)}\n"
    msg += f"\n1) Fazer uma aposta de ({apostaInit})\n"
    msg += "2) Dobrar a aposta\n"
    msg += "3) Sair\n\n"
    
    #envia a resposta
    try:
        client.send(msg.encode('utf-8'))
    except:
        return
    
    #recebe a resposta
    try:
        resp = client.recv(2048).decode('utf-8')
    except:
        client.close()
    
    if(resp == "1"):
        print(f"<{players[0].nome}> apostou {apostaInit}\n")
        players[0].fazerAposta(int(apostaInit))
        return apostaInit
    
    elif(resp == "2"):
        print(f"<{players[0].nome}> apostou {apostaInit * 2}\n")
        players[0].fazerAposta(int(apostaInit*2))
        return apostaInit * 2
    
    else:
        fimdejogo(client)
        
#transforma um deck em string
def deckToStr(baralho):
    str = f"[{baralho[0]}"
    
    for a in baralho:
        if a != baralho[0]:
            str += f", {a}"
    str += "]"
    
    return str

def deleteClient(client, vetor):
    vetor.remove(client)

def fimdejogo(client):
    msg = f"\n<{players[0].nome}> terminou com {players[0].carteira}\n"
    msg += f"<{players[1].nome}> terminou com {players[1].carteira}\n"
    if(players[0].carteira > players[1].carteira):
        msg += f"{players[0].nome} ganhou\n"
    elif(players[0].carteira < players[1].carteira):
        msg += f"{players[1].nome} ganhou\n"
    else:
        msg += "Terminou empatado\n"
        
    print(f"\n\n{msg} \n")
    client.send(msg.encode('utf-8'))
    
    quit()

serverInit('localhost', 6013)