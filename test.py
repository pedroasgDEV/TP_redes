import random

# Define os principais atributos das cartas
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

class Player(object):
    def __init__(self):
        self.cards = []
    
    #Um contador das suas cartas
    def addCard(self, card):
        self.cards.append(card)
    #uma função de dar a carta ao jogador

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
      
#Para se iniciar o Jogo, precisa utilizar no seu emulador o interpreterVideoPoker()
def interpreterVideoPoker():
  player = Player()

  # Intial Amount
  points = 100

  # Cost per hand
  handCost = 10

  end = False
  while not end:
    #print( "You have {0} points".format(points) )
    #print()

    points-=10

    #utilizado para assim que iniciar o jogo, voce recebe um deck, e ele recebe uma misturada.
    #Hand Loop
    deck = BaralhoInicial()
    deck.embaralha()
      
    # Deal Out
    #para entregar ao jogador 5 cartas
    for i in range(5):
      player.addCard(deck.retira())

    #para carta nas mãos deste jogador para este jogador ele verá suas cartas
    # Make them visible
    for card in player.cards:
      card.mostrar = True
    print(player.cards)

    validInput = False
    while not validInput:
      print("Quais Cartas você quer descartar? ( Ex. 1, 2, 3 )")
      print("Aperte Enter para segurar e escreva exit para sair do jogo ")
      inputStr = input()

      if inputStr == "exit":
        end=True
        break

        #um try para começo da verificação

      try:
        #Transformamos em inteiros, depois dividimos cada número pela virgula.
        inputList = [int(inp.strip()) for inp in inputStr.split(",") if inp]
        
        #validamos caso ele escreva corretamente
        for inp in inputList:
          if inp > 5:
            continue 
          if inp < 1:
            continue 
          
        #nesta lista, nós entregamos novas cartas e as mostramos para as pessoas
        for inp in inputList:
          player.cards[inp-1] = deck.retira()
          player.cards[inp-1].mostrar = True
          
        validInput = True
        
      except:
        #caso o usuário erre tudo
        print("Você colocou um número errado")

    #Score
    #Seu cálculo é feito a partir dos pontos que você ganha com cada poder da mão.
    score = Pontuacao(player.cards)
    
    if score.pontua() == 1000:
      print(player.cards)
    
    player.cards=[]
  
interpreterVideoPoker()