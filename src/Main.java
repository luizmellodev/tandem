import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;
import java.util.stream.IntStream;

public class Main {
    public static void main(String[] args) {
        boolean paralelo = true;
        int laco = 100;
        long[] seeds = {8106721679461579810L, 4749181526330897971L, 8772093917868148114L,
                7907799749336322280L, 6188031377265657066L};

        IntStream executions = IntStream.range(0, seeds.length);

        if (paralelo) {
            executions = executions.parallel();
        }
        executions.forEach(i -> execute(i, seeds, laco));
    }

    private static void execute(int i, long[] seeds, int laco) {
        System.out.println("Starting with index: " + i + " and seed: " + seeds[i]);
        Random random = new Random(seeds[i]);
        Fila[] filas = {
                new Fila(//G/G/1/5 -> tempoPrimeiraChegada: 3, chegada 1..3, saida 2..4
                        1, new IntervaloTempo(1, 3, random), new IntervaloTempo(2, 4, random),
                        3, 1, 5
                ),
                new Fila(//G/G/2/5 -> tempoPrimeiraChegada: 3, chegada 1..3, saida 2..4
                        2, new IntervaloTempo(1, 3, random), new IntervaloTempo(2, 4, random),
                        3, 2, 5
                )
        };
        for (Fila fila : filas) {
            System.out.println("Executing fila: " + fila.getId() + " execution: " + (i + 1));
            fila.executa(laco);
            save(fila, i + 1);
        }
    }

    private static void save(Fila fila, int i) {
        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter("fila_" + fila.getId() + "_exec_" + i + ".txt"));
            writer.write(fila.toString());
            writer.flush();
            writer.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}