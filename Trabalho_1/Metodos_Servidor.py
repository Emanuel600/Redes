# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 10:22:18 2023

@author: Aluno
"""

import dados_servidor as cdg
import threading as thr

"""
  Após conectar com o cliente, recebe o código de acesso e a porta utilizada.
Também confirma o recebimento da mensagem do cliente
"""
def receive_host(con, cliente):
    print("Executing thread " + str(thr.current_thread()) + " of receive_host")
    print("Conectado: " + str(cliente))
    print("aguardando mensagem")
    recebe = ''
    while (recebe == ''): # Enquanto não recebe mensagem, não envia ACK
        recebe = con.recv(1024)
        
    con.send("ACK".encode()) # A ser modificada
        
    cod_pt = (recebe.decode()).strip().split('-')     # Recebe código e porta
    cod    = cod_pt[0]
    porta  = cod_pt[1]
    # dic é o dicionário "código : [nome, autorização]"
    dic = cdg.codigos[cod]
        
    nome = dic[0] # Nome associado ao código
    auto = dic[1] # Autorização associada ao código
        
    print("Usuário: " + nome)
    print("Nível de Autorização: " + auto)
    print("Acessando porta " + porta)
    if int(porta) <= int(auto):
        con.send("Entrada autorizada".encode())
    else:
        con.send("Entrada não autorizada".encode())
        if int(porta) > 5:
            con.send("Terminal falhou em enviar valor da porta".encode())

    con.close()
    return
"""
    Lê um arquivo de texto e cria um dicionário no arquivo
'dados_servidor.py'
"""
def receive_dados(FILEPATH):
    with open(FILEPATH, 'r') as f:
        lines = f.read_lines();
        f.close();
    return

"""
    Loga as tentativas de acesso em arquivo txt na forma:
    [data (dd/mm/aaaa) - hora(24h : min : seg), porta(str), código(str), autorização(y/n)]
"""
def log_att(FILEPATH):
    return