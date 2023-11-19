import numpy as np
from tabulate import tabulate

def calculaResultados(lista, capacidade):
    
    np.set_printoptions(precision=4, suppress=True)
    data_array = np.array(lista)
    column_means = np.mean(data_array, axis=0)

    resultados = []
    for i in range(capacidade + 1):
        resultado = [i, column_means[i + 1], (column_means[i + 1] / column_means[0]) * 100]
        resultados.append(resultado)
    resultados.append(['TOTAL', column_means[0], 100])
    return resultados

def createSeeds(seed, n):
    seeds = []
    for i in range(n):
        seeds.append(seed)
        seed = (seed * 5) % 1
    return seeds

def calculaResultadosAux(lista, capacidade):
    resultados = []
    for i in range(capacidade + 1):
        resultado = [i, lista[-1][i + 1], (lista[-1][i + 1] / lista[-1][0]) * 100]
        resultados.append(resultado)
    resultados.append(['TOTAL', lista[-1][0], 100])
    return resultados

def escreveResultados(resultados, nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        for i, resultado in enumerate(resultados):
            arquivo.write('Fila ' + str(i + 1) + '\n')
            arquivo.write(str(tabulate(resultado)) + '\n')
        arquivo.write('\n')