from enum import Enum
import random
from Evento import Evento
from Evento import TipoEvento

class Fila:
    def __init__(self, intervalo_chegada=[], intervalo_saida=[], num_servidores=0, capacidade=0, infinita=True):
        self.intervalo_chegada = intervalo_chegada
        self.intervalo_saida = intervalo_saida
        self.num_servidores = num_servidores
        self.capacidade = capacidade
        self.infinita = infinita
        self.estados = []
        self.pesos = None
        self.perdas = 0
        self.populacao = 0

