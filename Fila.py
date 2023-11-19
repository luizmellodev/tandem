from enum import Enum
import random
from Evento import Evento
from Evento import TipoEvento

class TipoFila(Enum):
    SIMPLES = "Fila Simples"
    TANDEM = "Fila em Tandem"
    ESPERA = "Fila de Espera"

class Fila:
    def __init__(self, tipo: TipoFila, tempo_chegada, tempo_saida, tempo_primeira_chegada, num_servidores, capacidade, eventos, servidores_ocupados, aleatorios):
        self.tipo = tipo
        self.tempo_chegada = tempo_chegada
        self.tempo_saida = tempo_saida
        self.tempo_primeira_chegada = tempo_primeira_chegada
        self.num_servidores = num_servidores
        self.capacidade = capacidade
        self.eventos = eventos
        self.servidores_ocupados = servidores_ocupados
        self.aleatorios = aleatorios

    def imprimir_valores(self):
        print(f"Tipo de Fila: {self.tipo}")
        print(f"Tempo de Chegada: {self.tempo_chegada}")
        print(f"Tempo de Saída: {self.tempo_saida}")
        print(f"Tempo da Primeira Chegada: {self.tempo_primeira_chegada}")
        print(f"Número de Servidores: {self.num_servidores}")
        print(f"Capacidade da Fila: {self.capacidade}")
        print(f"Eventos: {[e.__dict__ for e in self.eventos]}")
        print(f"Servidores Ocupados: {self.servidores_ocupados}")
        print(f"Números Aleatórios: {self.aleatorios}")


class Controller:
    def __init__(self, filas: Fila, tempo_inicial):
            self.filas = filas
            self.tempo_inicial = tempo_inicial
            self.tratamento(self.tempo_inicial)

    def tratamento(self, tempo_inicial):
        print("Tratando eventos...")
        eventos = []
        tempo = 0
        primeiro_evento = Evento(TipoEvento.CHEGADA, tempo_inicial, 0.0)
        eventos.append(primeiro_evento)
        
        fila1, fila2 = self.filas[0], self.filas[1]

        while fila1.aleatorios:
            eventos.sort(key=lambda x: x.tempo)
            evento = eventos.pop(0)
            tempo_anterior = tempo
            tempo = evento.tempo

            if evento.tipo == TipoEvento.CHEGADA:

                if fila1.servidores_ocupados < fila1.capacidade:
                    fila1.servidores_ocupados += 1

                    if fila1.servidores_ocupados <= fila1.num_servidores:
                        self.agendaP12(tempo, fila1, eventos)
                self.agendaCH1(tempo, fila1, eventos)

            elif evento.tipo == TipoEvento.SAIDA:
                fila2.servidores_ocupados -= 1

                if fila2.servidores_ocupados > 0:
                    self.agendaSA2(tempo, fila2, eventos)

            elif evento.tipo == TipoEvento.TRANSICAO:
                fila1.servidores_ocupados -= 1

                if fila1.servidores_ocupados >= fila1.num_servidores:
                    self.agendaP12(tempo, fila1, eventos)

                if fila2.servidores_ocupados < fila2.capacidade:
                    fila2.servidores_ocupados += 1

                    if fila2.servidores_ocupados <= fila2.num_servidores:
                        self.agendaSA2(tempo, fila2, eventos)
            else:
                print("Evento deu merda", evento.tipo)
                exit(1)
            
    def agendaCH1(self, tempo, fila, eventos):
        sorteio = self._sorteio(fila.tempo_chegada[0], fila.tempo_chegada[1])
        evento = Evento(TipoEvento.CHEGADA, tempo + sorteio, sorteio)
        eventos.append(evento)
        print(f"Chegada de um cliente na fila {fila.tipo} no tempo {tempo + sorteio}")
        fila.eventos.append(evento)
        
    def agendaSA2(self, tempo, fila, eventos):
        sorteio = self._sorteio(fila.tempo_saida[0], fila.tempo_saida[1])
        evento = Evento(TipoEvento.CHEGADA, tempo + sorteio, sorteio)
        eventos.append(evento)
        print(f"Saída de um cliente na fila {fila.tipo} no tempo {tempo + sorteio}")
        fila.eventos.append(evento)
        
    def agendaP12(self, tempo, fila, eventos):
        sorteio = self._sorteio(fila.tempo_saida[0], fila.tempo_saida[1])
        evento = Evento(TipoEvento.TRANSICAO, tempo + sorteio, sorteio)
        eventos.append(evento)
        print(f"Transição de um cliente da fila {fila.tipo} para a fila {fila.tipo} no tempo {tempo + sorteio}")
        fila.eventos.append(evento)

    def _sorteio(self, min, max):
        return random.uniform(min, max)
        
    
