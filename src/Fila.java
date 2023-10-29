import java.util.*;

public class Fila {
    private final int id;
    private final IntervaloTempo tempoEntrada;
    private final IntervaloTempo tempoSaida;
    private final double tempoPrimeiraChegada;
    private final int servidores;
    private final int capacidadeMaxima;
    private List<EventoProcessado> eventos;
    private List<Evento> eventosAgendados;
    private double[] temposOcupados;
    private int servidoresOcupados;
    private int capacidadeAtual;
    private double tempoAtual;

    public Fila(int id, IntervaloTempo tempoEntrada, IntervaloTempo tempoSaida, double tempoPrimeiraChegada,
                int servidores, int capacidadeMaxima) {
        this.id = id;
        this.tempoEntrada = tempoEntrada;
        this.tempoSaida = tempoSaida;
        this.tempoPrimeiraChegada = tempoPrimeiraChegada;
        this.eventos = new ArrayList<>();
        this.eventosAgendados = new ArrayList<>();
        this.capacidadeMaxima = capacidadeMaxima;
        this.servidores = servidores;
        temposOcupados = new double[capacidadeMaxima + 1];
    }

    public int getId() {
        return id;
    }

    public void executa(int lacos) {
        eventosAgendados.add(Evento.newChegada(tempoPrimeiraChegada));
        for (int i = 0; i < lacos; i++) {
            Evento evento = proxEvento();
            temposOcupados[capacidadeAtual] += (evento.getTempo() - tempoAtual);
            tempoAtual = evento.getTempo();
            evento.executado();
            eventos.add(new EventoProcessado(evento, Arrays.copyOf(temposOcupados, temposOcupados.length)));
            if (evento.isChegada()) {
                if (capacidadeAtual < capacidadeMaxima) {
                    capacidadeAtual++;
                    if (servidoresOcupados < servidores) {
                        servidoresOcupados++;
                        agendaSaida();
                    }
                }
                agendaChegada();
            } else if (evento.isSaida()) {
                capacidadeAtual--;
                servidoresOcupados--;
                if (capacidadeAtual > 0) {
                    int servidoresDisponiveis = servidores - servidoresOcupados;
                    int aguardandoNaFila = capacidadeAtual - servidoresOcupados;
                    for (int j = 0; j < aguardandoNaFila && j < servidoresDisponiveis; j++) {
                        servidoresOcupados++;
                        agendaSaida();
                    }
                }
            } else {
                throw new RuntimeException("Evento: " + evento.getTipo() + " Não conhecido");
            }
        }
    }

    private void agendaChegada() {
        double tempo = tempoEntrada.proximoTempo();
        tempo += tempoAtual;
        Evento chegada = Evento.newChegada(tempo);
        eventosAgendados.add(chegada);
    }

    private void agendaSaida() {
        double tempo = tempoSaida.proximoTempo();
        tempo += tempoAtual;
        Evento saida = Evento.newSaida(tempo);
        eventosAgendados.add(saida);
    }

    private Evento proxEvento() {
        return eventosAgendados.stream()
                .sorted(Comparator.comparingDouble(Evento::getTempo))
                .filter(it -> !it.isExecuted())
                .findFirst()
                .orElseThrow(() -> new RuntimeException("Nenhum proximo evento a ser processado."));
    }

    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder("Fila: " + id + "\n");
        builder.append("Tempos por posicao: \n");
        for (int i = 0; i < temposOcupados.length; i++)
            builder.append("\t Ocupacao: ").append(i).append(" -> Tempo: ").append(temposOcupados[i]).append("\n");

        builder.append("Eventos Processados:\n");
        for (int i = 0; i < eventos.size(); i++)
            writeEvent(i, eventos.get(i), builder);

        builder.append("Eventos Agendados:\n");
        for (int i = 0; i < eventosAgendados.size(); i++)
            writeEvent(i, eventosAgendados.get(i), builder);

        return builder.toString();
    }

    private void writeEvent(int i, Evento evento, StringBuilder builder) {
        builder.append("\t").append(i + 1).append(": ").append(evento.toString()).append("\n");
    }
}
