# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 10:22:18 2023

@author: Aluno
"""

#import dados_servidor as cdg
import threading as thr

import time

codigos = {}

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
    try:
        dic = codigos[cod]
    except:
        con.send("Desconhecido-n".encode())
        log_att("log.txt", porta, cod, "negado (código inexistente)")
        print("Usuário Inexistente!")
        print("Acessando porta " + porta)
        return
        
    nome = dic[0] # Nome associado ao código
    auto = dic[1] # Autorização associada ao código
    aut  = ''     # Resultado da Requesição de Acesso
        
    print("Usuário: " + nome)
    print("Nível de Autorização: " + auto)
    print("Acessando porta " + porta)
    if int(porta) <= int(auto):
        aut = 'y'
        log_att("log.txt", porta, cod, "autorizado")
    else:
        aut = 'n'
        log_att("log.txt", porta, cod, "negado")
    
    con.send((nome + '-' + aut).encode())

    con.close()
    return
"""
    Lê um arquivo de texto e cria um dicionário no formato
código(str) : [nome(str), nível_autorização(str)]
"""
def receive_dados(FILEPATH):
    f = open(FILEPATH, 'r')

    for line in f:    
        vals  = line.strip().split(',')
        codg  = vals[0] # Código de acesso
        nomes = vals[1] # Nome do usuário
        nivel = vals[2] # Nível de acesso
    
        codigos[codg] = [nomes, nivel]
        

"""
    Loga as tentativas de acesso em arquivo txt na forma:
    [data (dd/mm/aaaa) - hora(24h : min : seg), porta(str), código(str), autorização(str)]
"""
def log_att(FILEPATH, porta, cdg, aut):
    tim = time.localtime()
    log = str(tim.tm_mday) + '/' + str(tim.tm_mon) + '/' + str(tim.tm_year) + ' - '
    log = log + str(tim.tm_hour) + ':' + str(tim.tm_min) + ':' + str(tim.tm_sec)
    
    log  = log + ', p' + str(porta) + ', ' + cdg + ', ' + aut + '\n'
    
    with open(FILEPATH, 'a') as f:
        f.write(log)
    print("atividade logada")
    f.close()
    
    return