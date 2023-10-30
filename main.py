from FilaTandem import FilaTandem
from utils import calculaResultados, createSeeds, escreveResultados


config = {
        'fila_1_arrival_limits':[1,3],
        'fila_1_service_limits':[2,4],
        'fila_2_service_limits':[1,3],
        'seeds':[],
        'fila_1_servidores':2,
        'fila_1_capacidade':3,
        'fila_2_servidores':1,
        'fila_2_capacidade':5
}

seeds = [0.9921, 0.0004, 0.5534, 0.2761, 0.3398]

fila_1_simulados = []
fila_2_simulados = []
for seed in seeds:
    seeds = createSeeds(seed, 100000)
    config['seeds'] = seeds
    filaTandem = FilaTandem(config)
    estados1, estados2 = filaTandem.escalonador(2.5000)
    fila_1_simulados.append(estados1[3:])
    fila_2_simulados.append(estados2[3:])
    
resultados1 = calculaResultados(fila_1_simulados, config['fila_1_capacidade'])
resultados2 = calculaResultados(fila_2_simulados, config['fila_2_capacidade'])

escreveResultados([fila_1_simulados, fila_2_simulados], 'resultados_media.txt')
escreveResultados([resultados1, resultados2], 'estatisticas.txt')