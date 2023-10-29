import java.util.Random;

public class IntervaloTempo {
    private final int min;
    private final int max;
    private Random random;

    public IntervaloTempo(int min, int max, Random random) {
        this.max = max;
        this.min = min;
        this.random = random;
    }

    public double proximoTempo() {
        return (max - min) * random.nextDouble() + min;
    }

    public void setRandom(Random random) {
        this.random = random;
    }

    @Override
    public String toString() {
        return "IntervaloTempo{" +
                "min=" + min +
                ", max=" + max +
                '}';
    }
}
