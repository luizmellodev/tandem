import random
from Fila import Fila
from auxiliares import carrega_yml
from Evento import Evento
from Evento import TipoEvento
from Aleatorio import Aleatorio

class Simulador:
    def __init__(self, caminhoArquivoConfiguracao, semente):
        self.escalonador = []
        self.tempoGlobal = 0.0
        self.a = 1664525
        self.c = 1013904223
        self.M = 2**32
        self.semente = semente
        self.iniciaRedeFilas(caminhoArquivoConfiguracao)
        self.aleatorio = Aleatorio(self.semente, self.a, self.c, self.M)
        
    def executar(self):
        self.chegada(self.filas[0], self.primeiraChegada)
        
        while self.iteracoes > 0:
            self.escalonador.sort( key=lambda x: x.tempo )
            proximo_evento = self.escalonador.pop(0)

            if proximo_evento.tipo == TipoEvento.CHEGADA:
                self.chegada(self.filas[0], proximo_evento.tempo)

            elif proximo_evento.tipo == TipoEvento.PASSAGEM:
                self.passagem(proximo_evento)

            else:
                self.saida(proximo_evento)

        for fila in self.filas:
            fila.estados = [round(tempo, 4) for tempo in fila.estados]
        
        return self.filas
    
    def sorteio(self, min, max):
        self.iteracoes -= 1
        return (max - min) * self.aleatorio.proximo() + min
    
    def atualizar_tempo_filas(self, tempo):
        for fila in self.filas:
            fila.estados[fila.populacao] += (tempo - self.tempoGlobal)
        self.tempoGlobal = tempo

    def agenda_saida(self, indice_fila_origem):
        evento_saida = Evento(
            TipoEvento.SAIDA, 
            self.tempoGlobal + self.sorteio(self.filas[indice_fila_origem].intervalo_saida[0], self.filas[indice_fila_origem].intervalo_saida[1]),
            filaOrigem=indice_fila_origem
            )
        self.escalonador.append(evento_saida)
    
    def saida(self, evento):
        self.atualizar_tempo_filas(evento.tempo)
        fila_origem = self.filas[evento.filaOrigem]

        fila_origem.populacao -= 1
        if fila_origem.populacao >= fila_origem.num_servidores:
            indice_fila_destino = self.filas.index(random.choices(self.filas, fila_origem.pesos)[0])

            if evento.filaOrigem == indice_fila_destino:
                self.agenda_saida(evento.filaOrigem)
            else:
                self.agenda_passagem(evento.filaOrigem, indice_fila_destino)

    def agenda_chegada(self):
        evento_chegada = Evento(
            TipoEvento.CHEGADA,
            self.tempoGlobal + self.sorteio(self.filas[0].intervalo_chegada[0], self.filas[0].intervalo_chegada[1])
            )
        self.escalonador.append(evento_chegada)

    def chegada(self, fila, tempo):
        self.atualizar_tempo_filas(tempo)

        if fila.infinita and (fila.populacao == fila.capacidade):
            fila.estados.append(0)
            fila.capacidade += 1

        if fila.populacao < fila.capacidade:
            fila.populacao += 1

            if fila.populacao <= fila.num_servidores:
                indice_fila_origem = self.filas.index(fila)
                indice_fila_destino = self.filas.index(random.choices(self.filas, fila.pesos)[0])
                self.agenda_passagem(indice_fila_origem, indice_fila_destino)
        else:
            fila.perdas += 1
        self.agenda_chegada()

    def agenda_passagem(self, indice_fila_origem, indice_fila_destino):
        evento_passagem = Evento(
            TipoEvento.PASSAGEM,
            self.tempoGlobal + self.sorteio(self.filas[indice_fila_origem].intervalo_saida[0], self.filas[indice_fila_origem].intervalo_saida[1]),
            filaOrigem=indice_fila_origem,
            filaDestino=indice_fila_destino)
        self.escalonador.append(evento_passagem)
    
    def passagem(self, event):
        self.atualizar_tempo_filas(event.tempo)
        fila_origem = self.filas[event.filaOrigem]
        fila_destino = self.filas[event.filaDestino]

        fila_origem.populacao -= 1

        if fila_origem.populacao >= fila_origem.num_servidores:
            indice_fila_origem = self.filas.index(fila_origem)
            indice_fila_destino = self.filas.index(random.choices(self.filas, fila_origem.pesos)[0])

            if indice_fila_origem == indice_fila_destino:
                self.agenda_saida(indice_fila_origem)
            else:
                self.agenda_passagem(indice_fila_origem, indice_fila_destino)

        if fila_destino.populacao >= fila_destino.capacidade and fila_destino.infinita:
            fila_destino.estados.append(0)
            fila_destino.capacidade += 1
        
        if fila_destino.populacao < fila_destino.capacidade:
            fila_destino.populacao += 1

            if fila_destino.populacao <= fila_destino.num_servidores:
                indice_fila_origem = self.filas.index(fila_destino)
                indice_fila_destino = self.filas.index(random.choices(self.filas, fila_destino.pesos)[0])

                if indice_fila_origem == indice_fila_destino:
                    self.agenda_saida(indice_fila_origem)
                else:
                    self.agenda_passagem(indice_fila_origem, indice_fila_destino)
        else:
            fila_destino.perdas += 1

    def iniciaRedeFilas(self, caminhoArquivoConfiguracao):
        chegadas, filas, rede, rndnumbersPerSeed = carrega_yml(caminhoArquivoConfiguracao)
        self.iteracoes = rndnumbersPerSeed
        self.primeiraChegada = chegadas['Q1']
        
        num_filas = len(filas)
        matriz_pesos = [[0] * num_filas for _ in range(num_filas)]
        
        nome_filas = list(filas.keys())
        filas = list(filas.values())

        for coneccao in rede:
            indice_origem = nome_filas.index(coneccao['source'])
            indice_alvo = nome_filas.index(coneccao['target'])
            matriz_pesos[indice_origem][indice_alvo] = coneccao['probability']

        for i in range(num_filas):
            soma_linha = sum(matriz_pesos[i])
            matriz_pesos[i][i] = 1 - soma_linha

        self.filas = [Fila() for _ in  range(len(filas))]
        
        for i in range(num_filas):
            self.filas[i].intervalo_chegada = [filas[i].get('minArrival', 0.0), filas[i].get('maxArrival', 0.0)]
            self.filas[i].intervalo_saida = [filas[i]['minService'], filas[i]['maxService']]
            self.filas[i].capacidade = filas[i].get('capacity', 0)
            self.filas[i].infinita = self.filas[i].capacidade == 0
            self.filas[i].num_servidores = filas[i]['servers']
            self.filas[i].estados = [0.0] * (self.filas[i].capacidade + 1)
            self.filas[i].pesos = matriz_pesos[i]
            
