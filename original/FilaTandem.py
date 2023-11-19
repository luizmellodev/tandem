class FilaTandem:

    def __init__(self, config) -> None:
        self.FILA1 = 0
        self.FILA2 = 0
        self.tempo = 0.0
        self.fila_1_arrival_limits = config['fila_1_arrival_limits']
        self.fila_1_service_limits = config['fila_1_service_limits']
        self.fila_2_service_limits = config['fila_2_service_limits']
        self.seeds = config['seeds']
        self.seed = 0
        self.fila_1_capacidade = config['fila_1_capacidade']
        self.fila_2_capacidade = config['fila_2_capacidade']
        self.fila_1_servidores = config['fila_1_servidores']
        self.fila_2_servidores = config['fila_2_servidores']

    def escalonador(self, tempo_inicial):
        self.escalonador_eventos = []
        self.tabela_estados_fila1 = []
        self.tabela_estados_fila2 = []
        
        # cria um vetor estado inicial com tamanho 3 + (capacidade + 1)
        fila_1_estado = [0.0] * (4 + (self.fila_1_capacidade + 1))
        fila_1_estado[0] = None
        fila_1_estado[1] = self.FILA1
        fila_1_estado[2] = self.FILA2
        fila_1_estado[3] = self.tempo
        self.tabela_estados_fila1.append(fila_1_estado)
        
        fila_2_estado = [0.0] * (4 + (self.fila_2_capacidade + 1))
        fila_2_estado[0] = None
        fila_2_estado[1] = self.FILA1
        fila_2_estado[2] = self.FILA2
        fila_2_estado[3] = self.tempo
        self.tabela_estados_fila2.append(fila_2_estado)
        
        # novo evento sem sorteio
        evento = ['CH1', tempo_inicial, 0.0]
        self.escalonador_eventos.append(evento)
        while self.seed < len(self.seeds):
            self.escalonador_eventos.sort( key=lambda x: x[1] )
            evento = self.escalonador_eventos.pop(0) 
            tempo_anterior = self.tempo
            self.tempo = evento[1]
            if evento[0] == 'CH1':
                if self.FILA1 < self.fila_1_capacidade:
                    self.FILA1 += 1
                    if self.FILA1 <= self.fila_1_servidores:
                        self.agendaP12(self.tempo)
                self.agendaCH1(self.tempo)
            elif evento[0] == 'SA2':
                self.FILA2 -= 1
                if self.FILA2 > 0:
                    self.agendaSA2(self.tempo)
            elif evento[0] == 'P12':
                self.FILA1 -= 1
                if self.FILA1 >= self.fila_1_servidores:
                    self.agendaP12(self.tempo)
                if self.FILA2 < self.fila_2_capacidade:
                    self.FILA2 += 1
                    if self.FILA2 <= self.fila_2_servidores:
                        self.agendaSA2(self.tempo)       
            
            self.calculaEstado(evento, tempo_anterior)
        return self.tabela_estados_fila1[-1], self.tabela_estados_fila2[-1]

    def calculaEstado(self, evento, tempo_anterior):
        fila_1_ultimo_estado = self.tabela_estados_fila1[-1]
        fila_2_ultimo_estado = self.tabela_estados_fila2[-1]
        fila_1_ultima_fila = fila_1_ultimo_estado[1]
        fila_2_ultima_fila = fila_2_ultimo_estado[2]
    
        fila_1_novo_estado = fila_1_ultimo_estado.copy()
        fila_2_novo_estado = fila_2_ultimo_estado.copy()
        
        fila_1_novo_estado[0] = evento[0]
        fila_1_novo_estado[1] = self.FILA1
        fila_1_novo_estado[2] = self.FILA2
        fila_1_novo_estado[3] = self.tempo
        fila_2_novo_estado[0] = evento[0]
        fila_2_novo_estado[1] = self.FILA1
        fila_2_novo_estado[2] = self.FILA2
        fila_2_novo_estado[3] = self.tempo        
        # diferenca entre tempo atual e o anterior
        diferenca = self.tempo - tempo_anterior
        
        # atualiza quanto tempo a fila ficou com a quantidade de pessoas anterior
        # diferenca + tempo anterior da fila com a quantidade de pessoas anterior
        fila_1_novo_estado[4 + fila_1_ultima_fila] = diferenca + fila_1_ultimo_estado[4 + fila_1_ultima_fila]
        fila_2_novo_estado[4 + fila_2_ultima_fila] = diferenca + fila_2_ultimo_estado[4 + fila_2_ultima_fila]
        
        self.tabela_estados_fila1.append(fila_1_novo_estado)
        self.tabela_estados_fila2.append(fila_2_novo_estado)

    def _sorteio(self, min_max):
        if self.seed == len(self.seeds):
            return 0
        self.seed += 1
        return (min_max[1] - min_max[0]) * self.seeds[self.seed - 1] + min_max[0]
    
    def agendaCH1(self, tempo):
        sorteio = self._sorteio(self.fila_1_arrival_limits)
        evento = ['CH1', tempo + sorteio, sorteio]
        self.escalonador_eventos.append(evento)
        
    def agendaSA2(self, tempo):
        sorteio = self._sorteio(self.fila_2_service_limits)
        evento = ['SA2', tempo + sorteio, sorteio]
        self.escalonador_eventos.append(evento)
        
    def agendaP12(self, tempo):
        sorteio = self._sorteio(self.fila_1_service_limits)
        evento = ['P12', tempo + sorteio, sorteio]
        self.escalonador_eventos.append(evento)