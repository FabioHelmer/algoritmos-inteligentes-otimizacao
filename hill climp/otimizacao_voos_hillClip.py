import time
import random
import math

pessoas = [('Amanada', 'CWB'),
           ('Pedro', 'GIG'),
           ('Marcos', 'POA'),
           ('Priscila', 'FLN'),
           ('Jessica', 'CNF'),
           ('Paulo', 'GYN')]

destino = 'GRU'
voos = {}

for linha in open('voos.txt'):
    _origin, _destino, _saida, _chegada, _preco = linha.split(',')
    voos.setdefault((_origin, _destino), [])
    voos[(_origin, _destino)].append((_saida, _chegada, int(_preco)))


def imprimir_agenda(agenda):
    id_voo = -1
    for i in range(len(agenda)//2):
        nome = pessoas[i][0]
        origem = pessoas[i][1]
        id_voo += 1
        ida = voos[(origem, destino)][agenda[id_voo]]
        id_voo += 1
        volta = voos[(destino, origem)][agenda[id_voo]]
        print('%10s%10s %5s-%5s R$%3s %5s-%5s R$%3s' % (nome, origem,
                                                        ida[0], ida[1], ida[2], volta[0], volta[1], volta[2]))


def getMinutos(hora):
    x = time.strptime(hora, '%H:%M')
    minutos = x[3] * 60 + x[4]
    return minutos


def funcao_custo(solucao):
    preco_total = 0
    ultima_chegada = 0
    primeira_partida = 1439

    id_voo = -1
    for i in range(len(solucao)//2):
        origem = pessoas[i][1]
        id_voo += 1
        ida = voos[(origem, destino)][solucao[id_voo]]
        id_voo += 1
        volta = voos[(destino, origem)][solucao[id_voo]]

        preco_total += ida[2]
        preco_total += volta[2]
        if ultima_chegada < getMinutos(ida[1]):
            ultima_chegada = getMinutos(ida[1])

        if primeira_partida > getMinutos(volta[0]):
            primeira_partida = getMinutos(volta[0])

    total_espera = 0
    id_voo = -1
    for i in range(len(solucao)//2):
        origem = pessoas[i][1]
        id_voo += 1
        ida = voos[(origem, destino)][solucao[id_voo]]
        id_voo += 1
        volta = voos[(destino, origem)][solucao[id_voo]]

        total_espera += ultima_chegada - getMinutos(ida[1])
        total_espera += getMinutos(volta[0]) - primeira_partida

    if ultima_chegada > primeira_partida:
        preco_total += 50

    return preco_total + total_espera


# agenda = [1, 4, 3, 2, 7, 3, 6, 3, 2, 4, 5, 3]


def pesquisa_randomica(dominio, funcao_custo):
    melhor_custo = 999999999
    for i in range(0, 10000):
        solucao = [random.randint(dominio[i][0], dominio[i][1])
                   for i in range(len(dominio))]
        custo = funcao_custo(solucao)
        if custo < melhor_custo:
            print('.')
            melhor_custo = custo
            melhor_solucao = solucao
    return melhor_solucao


def hill_clip(dominio, funcao_custo):
    solucao = pesquisa_randomica(dominio, funcao_custo)

    while True:
        vizinhos = []

        for i in range(len(dominio)):
            if solucao[i] > dominio[i][0]:
                if solucao[i] != dominio[i][1]:
                    vizinhos.append(solucao[0:i]+[solucao[i]+1]+solucao[i+1:])
            if solucao[i] < dominio[i][1]:
                if solucao[i] != dominio[i][0]:
                    vizinhos.append(
                        solucao[0:i] + [solucao[i]-1] + solucao[i+1:])

        atual = funcao_custo(solucao)
        melhor = atual
        for i in range(len(vizinhos)):
            custo = funcao_custo(vizinhos[i])
            if custo < melhor:
                melhor = custo
                solucao = vizinhos[i]
        if melhor == atual:
            break
    return solucao


dominio = [(0, 9)] * (len(pessoas)*2)

hill_clip = hill_clip(dominio, funcao_custo)
print(hill_clip)
imprimir_agenda(hill_clip)
print(funcao_custo(hill_clip))
