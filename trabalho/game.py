characters = ["Sheldon", "Amy", "Leonard", "Penny", "Howard", "Bernadette", "Raj"]
cards = ["Pedra", "Papel", "Tesoura", "Lagarto", "Spock"]

default_port = 4007
salas_id = 0
class Player:
    def __init__(self, username, character, client = 0):
        self.username = username
        self.character = character
        self.client = client #Recebe o cliente no servidor
        self.vidas = 0
        self.card = 0


class Room:
    def __init__(self, nome, player, senha = '1234'):
        self.nome = nome
        self.senha = senha
        self.players = [player]
        self.isFull = False
        self.sala_id = salas_id