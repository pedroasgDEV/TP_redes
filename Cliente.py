import threading
import socket


def clientInit(address, port):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((address, port))
    except:
        return print('\nNão foi possívvel se conectar ao servidor!\n')

    print('\nConectado')
    
    messagesTreatment(client)
    
def messagesTreatment(client):
    
    #Envia o nome do usuario
    username = input('Digite seu nome: ')
    try:
        client.send(f'{username}'.encode('utf-8'))
    except:
        return
    
    jogoInit(client)

def jogoInit(client):
    
    while True:
        print("\nInicio do jogo de poker\n")

        betting(client)
        ConectBetting(client)
        
        #retira cartas do baralho
        validInput = False
        while not validInput:
            inputStr = input("Quais Cartas você quer descartar? ( Ex. 1, 2, 3 ): ")

            try:
                #Transformamos em inteiros, depois dividimos cada número pela virgula.
                inputList = [int(inp.strip()) for inp in inputStr.split(",") if inp]
                
                #validamos caso ele escreva corretamente
                for inp in inputList:
                    if inp > 5:
                        continue 
                    if inp < 1:
                        continue 
                
                if len(inputList) > 5: continue 
                
                client.send(inputStr.encode('utf-8'))
                validInput = True
                
            except:
                #caso o usuário erre tudo
                print("Você colocou um número errado")
        
        betting(client)
        ConectBetting(client)
        
        #Tenta receber a msg
        try:
            msg = client.recv(2048).decode('utf-8')
        except:
            client.close()
            
        print(msg)
        
        #Tenta receber a msg
        try:
            msg = client.recv(2048).decode('utf-8')
        except:
            client.close()
            
        print(f"\n{msg} \n")
        
def betting(client):
    #Tenta receber a msg
    try:
        msg = client.recv(2048).decode('utf-8')
    except:
        client.close()
        
    print(msg)
        
    entrada = int(input("Digite uma resposta: "))
    while entrada < 1 or entrada > 3:
        entrada = int(input("Digite uma resposta valida: "))
    
    #envia a resposta
    try:
        client.send(f'{entrada}'.encode('utf-8'))
    except:
        return
    
    if(entrada == 3): fimdejogo(client)

def ConectBetting(client): 
    #Tenta receber a carteira+
    try:
        msg = client.recv(2048).decode('utf-8')
    except:
        client.close()
        
    if msg == "fim de jogo":
        fimdejogo(client)
    else:
        print(msg)

def fimdejogo(client):
    #Tenta receber a msg
    try:
        msg = client.recv(2048).decode('utf-8')
    except:
        client.close()
        
    print(f"\n{msg} \n")
    
    quit()

clientInit('localhost', 6715)