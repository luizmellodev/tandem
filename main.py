from Fila import Fila
from Evento import Evento
from Fila import TipoFila
from LCG import LCG
from Fila import Controller
class Main:
    def __init__(self):
        self.filas = []
        self.numeros_aleatorios = []

    def execute(self):
        seeds = [0.9921, 0.0004, 0.5534, 0.2761, 0.3398]        
        a = 1664525
        c = 1013904223
        M = 2**32
        aleatorios = 10
        for seed in seeds:
            for fila in self.filas:
                lcg = LCG(seed, a, c, M)
                fila.aleatorios = [lcg.rand() for _ in range(aleatorios)]
                

    def criar_filas(self):
            fila1 = Fila(
                tipo=TipoFila.SIMPLES,
                tempo_chegada=[1, 3],
                tempo_saida=[2, 4],
                tempo_primeira_chegada=3,
                num_servidores=1,
                capacidade=5,
                eventos=[],
                servidores_ocupados=0,
                aleatorios=[]
            )
            self.filas.append(fila1)

            fila2 = Fila(
                tipo=TipoFila.TANDEM,
                tempo_chegada=[1,3],
                tempo_saida=[2, 4],
                tempo_primeira_chegada=3,
                num_servidores=2,
                capacidade=5,
                eventos=[],
                servidores_ocupados=0,
                aleatorios=[]
            )
            self.filas.append(fila2)

    def imprimir_filas(self):
        for i, fila in enumerate(self.filas, start=1):
            print(f"=== Fila {i} criada ===")
            fila.imprimir_valores()
            print()

# Exemplo de uso
if __name__ == "__main__":
    main = Main()
    main.criar_filas()
    main.execute()
    controller = Controller(main.filas, 3)