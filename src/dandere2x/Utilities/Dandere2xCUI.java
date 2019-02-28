package dandere2x.Utilities;

import java.io.File;
import java.text.DecimalFormat;
import java.util.ArrayList;

/**
 * A simple CUI class to give updates and status on execution.
 * <p>
 * Runs on it's own thread.
 */
public class Dandere2xCUI {

    private String mergedDir;
    private int totalFrames;
    private DecimalFormat numberFormat = new DecimalFormat("#.000");

    public Dandere2xCUI(String mergedDir, int totalFrames) {
        this.mergedDir = mergedDir;
        this.totalFrames = totalFrames;
    }

    public void run() {


        ArrayList<Double> times = new ArrayList<>();

        for (int x = 1; x < totalFrames - 1; x++) {
            if (times.size() == 10)
                times.remove(0);

            long startTime = System.nanoTime();
            while (!new File(mergedDir + "merged_" + x + ".jpg").exists()) {
                DandereUtils.threadSleep(50);
            }
            long endTime = System.nanoTime();

            double elapsed = (double) (endTime - startTime) / 1000000000;
            times.add(elapsed);

            double average = 0;

            for (double duration : times)
                average += duration;

            average /= times.size();

            System.out.print("Merged frame " + x + "       Average of Last " + times.size() + ": " + numberFormat.format(average) + " sec \\frame \r");
        }


    }
}
