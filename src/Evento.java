public class Evento {
    protected Tipo tipo;
    protected double tempo;
    protected boolean executed;

    public Evento(Tipo tipo, double tempo) {
        this.tipo = tipo;
        this.tempo = tempo;
        this.executed = false;
    }

    protected Evento(Tipo tipo, double tempo, boolean executado) {
        this.tempo = tempo;
        this.tipo = tipo;
        this.executed = executado;
    }

    public static Evento newSaida(double tempo) {
        return new Evento(Tipo.SAIDA, tempo);
    }

    public static Evento newPassagem(double tempo) {
        return new Evento(Tipo.PASSAGEM, tempo);
    }

    public static Evento newChegada(double tempo) {
        return new Evento(Tipo.CHEGADA, tempo);
    }

    public boolean isChegada() {
        return Tipo.CHEGADA.equals(tipo);
    }

    public boolean isPassagem() {
        return Tipo.PASSAGEM.equals(tipo);
    }

    public boolean isSaida() {
        return Tipo.SAIDA.equals(tipo);
    }

    public Tipo getTipo() {
        return tipo;
    }

    public double getTempo() {
        return tempo;
    }

    public boolean isExecuted() {
        return executed;
    }

    public void executado() {
        this.executed = true;
    }

    @Override
    public String toString() {
        return "Evento{" +
                "tipo=" + tipo +
                ", tempo=" + tempo +
                ", executed=" + executed +
                '}';
    }

    private enum Tipo {
        CHEGADA, SAIDA, PASSAGEM
    }
}
