import yaml
from tabulate import tabulate

def carrega_yml(caminho_arquivo):
    
    file_path = caminho_arquivo

    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    parameters = data.get('parameters', {})
    arrivals = parameters.get('arrivals', {})
    queues = parameters.get('queues', {})
    network = parameters.get('network', [])
    rndnumbersPerSeed = parameters.get('rndnumbersPerSeed', None)

    return arrivals, queues, network, rndnumbersPerSeed

def imprimir_resultados(filas):
    for i, fila in enumerate(filas, start=1):
        print("#" * 60)
        print(f'Tabela de Resultados para Q{i}')

        info_table = [["G/G", f'{fila.num_servidores}/{fila.capacidade}'],
                      ["Intervalo de Chegada", fila.intervalo_chegada],
                      ["Intervalo de Saída", fila.intervalo_saida],
                      ["Probabilidades de Passagem", " ".join([f"Q{j+1}: {peso:.2f}" if j+1 != i else f"Saída: {peso:.2f}" for j, peso in enumerate(fila.pesos)])]
                      ]

        print(tabulate(info_table, headers='firstrow', tablefmt="grid"))
        print()

        estados_table = [["Estado", "Tempo", "Probabilidade"]] + [[j, fila.estados[j], f"{fila.estados[j]/sum(fila.estados):.2%}"] for j in range(len(fila.estados))]

        print(tabulate(estados_table, headers="firstrow", tablefmt="grid"))
        print()

