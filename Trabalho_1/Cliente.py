# Imports
import socket 
import time
import sys

#ip = input('digite o ip de conexao: ') 
ip = 'localhost' #localhost - endereço IP do meu próprio computador
porta = 7000 # porta aleatória

arg_list = sys.argv

if (len(arg_list) - 1): # 1 se o número da porta foi entrado no terminal
    pt = str(arg_list[1])
else: # Para testes
    pt = '5'

addr = ((ip,porta)) 
#criar o socket para o servidor passando a família do protocolo de transporte 
#socket.AF_INET define que é um protocolo para rede IP (AF_BLUETOOTH definiria comunicação bluetooth, por exemplo)
#socket.SOCK_STREAM para TCP
#socket.SOCK_DGRAM para UDP
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#define endereço e porta do servidor ao qual o cliente irá se comunicar
socket_cliente.connect(addr)

resposta = "NACK"

mensagem = input("Digite seu código de acesso: ")
mensagem = mensagem + "-" + pt
while (resposta != "ACK"):
    socket_cliente.send(mensagem.encode()) # Envia mensagem (codificada em bytes)
    resposta = socket_cliente.recv(1024).decode() # Recebe ACK

resposta = socket_cliente.recv(1024).decode() # Recebe autorização
print(resposta)
#resposta = socket_cliente.recv(1024)
time.sleep(0.1)
#print(resposta)

socket_cliente.close()