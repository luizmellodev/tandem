from enum import Enum

class TipoEvento(Enum):
    CHEGADA = "CH1"
    SAIDA = "SA2"
    PASSAGEM = "P12"

class Evento:
    def __init__(self, tipo: TipoEvento, tempo, filaOrigem=None, filaDestino=None):
        self.tipo = tipo
        self.tempo = tempo
        self.filaOrigem = filaOrigem
        self.filaDestino = filaDestino