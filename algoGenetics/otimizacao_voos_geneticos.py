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
    for i in range(len(solucao) // 2):
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
    print("pesquisa randomca")
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


def simulated_anneling(dominio, funcao_custo, temperatura=10000, resfriamento=0.95, passo=1):
    print("simulated_anneling")
    solucao = pesquisa_randomica(dominio, funcao_custo)
    while temperatura > 0.1:
        i = random.randint(0, len(dominio)-1)
        direcao = random.randint(-passo, passo)
        solucaoTemp = solucao[:]
        solucaoTemp[i] += direcao

        if(solucaoTemp[i] < dominio[i][0]):
            solucaoTemp[i] = dominio[i][0]
        elif solucaoTemp[i] > dominio[i][1]:
            solucaoTemp[i] = dominio[i][1]

        custo_solucao = funcao_custo(solucao)
        custo_solucao_temp = funcao_custo(solucaoTemp)
        probabilit = pow(math.e, (-custo_solucao_temp -
                                  custo_solucao) / temperatura)

        if(custo_solucao_temp < custo_solucao or random.random() < probabilit):
            solucao = solucaoTemp

        temperatura = temperatura*resfriamento
        print(".")

    return solucao


def mutacao(dominio, passo, solucao):
    i = random.randint(0, len(dominio) - 1)
    mutante = solucao

    if random.random() < 0.5:
        if solucao[i] != dominio[i][0]:
            mutante = solucao[0:i] + [solucao[i] - passo] + solucao[i + 1:]
    else:
        if solucao[i] != dominio[i][1]:
            mutante = solucao[0:i] + [solucao[i] + passo] + solucao[i + 1:]

    return mutante


def cruzamento(dominio, solucao1, solucao2):
    i = random.randint(1, len(dominio) - 2)
    return solucao1[0:i] + solucao2[i:]


def genetico(dominio, funcao_custo, tamanho_populacao=200, passo=1,
             probabilidade_mutacao=0.2, elitismo=0.2, numero_geracoes=10000):

    populacao = []
    for i in range(tamanho_populacao):
        solucao = [random.randint(dominio[i][0], dominio[i][1])
                   for i in range(len(dominio))]

        populacao.append(solucao)
    numero_elitismo = int(elitismo * tamanho_populacao)

    for i in range(numero_geracoes):
        custos = [(funcao_custo(individuo), individuo)
                  for individuo in populacao]

        custos.sort()
        individuos_ordenados = [individuo for (custo, individuo) in custos]

        populacao = individuos_ordenados[0:numero_elitismo]

        while len(populacao) < tamanho_populacao:
            if random.random() < probabilidade_mutacao:
                m = random.randint(0, numero_elitismo)
                populacao.append(
                    mutacao(dominio, passo, individuos_ordenados[m]))
            else:
                c1 = random.randint(0, numero_elitismo)
                c2 = random.randint(0, numero_elitismo)
                populacao.append(cruzamento(dominio, individuos_ordenados[c1],
                                            individuos_ordenados[c2]))

    return custos[0][1]


dominio = [(0, 9)] * (len(pessoas)*2)

solucao_genetico = genetico(dominio, funcao_custo)
print(solucao_genetico)
custo_genetico = funcao_custo(solucao_genetico)
imprimir_agenda(solucao_genetico)
print(custo_genetico)
