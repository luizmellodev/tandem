import java.util.Arrays;

public class EventoProcessado extends Evento {
    private final double[] tempos;

    public EventoProcessado(Evento evento, double[] tempos) {
        super(evento.tipo, evento.tempo, evento.executed);
        this.tempos = tempos;
    }

    @Override
    public String toString() {
        return "EventoProcessado{" +
                "tipo=" + tipo +
                ", tempo=" + tempo +
                ", tempos=" + Arrays.toString(tempos) +
                '}';
    }
}
