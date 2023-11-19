from enum import Enum

class TipoEvento(Enum):
    CHEGADA = "CH1"
    SAIDA = "SA2"
    TRANSICAO = "P12"

class Evento:
    def __init__(self, tipo: TipoEvento, tempo, sorteio):
        self.tipo = tipo
        self.tempo = tempo
        self.sorteio = sorteio