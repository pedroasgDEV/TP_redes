characters = ["Sheldon", "Amy", "Leonard", "Penny", "Howard", "Bernadette", "Raj"]
cards = ["Pedra", "Papel", "Tesoura", "Lagarto", "Spock"]
class Player:
    def __init__(self, username, character):
        self.username = username
        self.character = character
        self.vidas = 0
        self.card = 0
        self.client = 0 #Recebe o cliente no servidor
        self.addr = 0 #Recebe o endereço do cliente no servidor
         