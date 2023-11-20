from Simulador import Simulador
from auxiliares import imprimir_resultados

if __name__ == '__main__':
    
    simulador = Simulador('config.yml', 42)
    filas = simulador.executar()
    imprimir_resultados(filas)
