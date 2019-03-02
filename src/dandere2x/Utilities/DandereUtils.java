package dandere2x.Utilities;

import wrappers.Frame;

import java.io.File;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class DandereUtils {

    //https://stackoverflow.com/questions/14288185/detecting-windows-or-linux
    public static boolean isLinux() {
        String OS = System.getProperty("os.name").toLowerCase();
        return (OS.contains("nix") || OS.contains("nux") || OS.contains("aix"));
    }

    public static List<String> readListInFile(String fileName) {

        List<String> lines = Collections.emptyList();
        try {
            lines =
                    Files.readAllLines(Paths.get(fileName), StandardCharsets.UTF_8);
        } catch (IOException e) {

            // do something
            e.printStackTrace();
        }
        return lines;
    }

    public static void threadSleep(int n) {
        try {

            Thread.sleep(n);
        } catch (InterruptedException e) {
        }
    }


    public static ArrayList<String> getFileTypeInFolder(String path, String type) {
        File folder = new File(path);
        File[] listOfFiles = folder.listFiles();
        ArrayList<String> fileList = new ArrayList<String>();

        for (File x : listOfFiles) {
            if (x.toString().contains(type))
                fileList.add(x.toString());
        }
        Collections.sort(fileList);
        return fileList;
    }


    /**
     * Listens in to see if a file is valid or not.
     * Continue to cycle within a time limit. Currently time limit is 10000 * 100 = 100 seconds.
     * Returns image when it is loaded. If not, keep waiting.
     *
     * @param baseName absolute URL to file
     * @return baseImage if successfully load image.
     */
    public static Frame listenImage(PrintStream log, String baseName) {

        boolean dneErrorShown = false;
        Frame frameLoad = null;
        int timeLimit = 100000;

        for (long x = 0; x < timeLimit; x++) {
            if (!new File(baseName).exists()) {
                if (!dneErrorShown) {
                    log.println("Could not find file " + baseName + ".. waiting...");
                    dneErrorShown = true;
                }
                threadSleep(100);
                continue;
            }

            try {
                frameLoad = new Frame(baseName);
            } catch (NullPointerException e) {
                log.println("null pointer exception in image");
                threadSleep(100);
                continue;
            } catch (IllegalArgumentException e) {
                log.println("error reading png on image, waiting - ");
                threadSleep(100);
                continue;
            } catch (IndexOutOfBoundsException e) {
                log.println("out of bounds reading png on image, waiting - ");
                threadSleep(100);
                continue;
            }

            if (frameLoad != null)
                break;
        }

        if (frameLoad == null) {
            log.print("Could not find " + baseName + " within 1000 seconds, execution halted");
            throw new IllegalArgumentException("Could not find " + baseName + " within 1000 seconds, execution halted");
        }
        return frameLoad;
    }


    //this isnt working on linux

    /**
     * Listens in to see if a file is valid or not.
     * Continue to cycle within a time limit. Currently time limit is 10000 * 100 = 100 seconds.
     * Returns image when it is loaded. If not, keep waiting.
     * <p>
     * There's a very odd error / work around I have working here. There were a few cases
     * in which the listenText function would begin to read the textfile before the dandere2xcpp file
     * began finish writing to the text file...
     * <p>
     * to mitigate this, we read it twice at two different times. If the lengths of the files difer,
     * do it again.
     *
     * @return baseImage if successfully load image.
     */
    public static List listenText(PrintStream log, String input) {

        boolean dneErrorShown = false;
        List initial;
        int timeLimit = 10000;

        for (long x = 0; x < timeLimit; x++) {
            if (!new File(input).exists()) {
                if (!dneErrorShown) {
                    log.println("Could not find file " + input + ".. waiting...");
                    dneErrorShown = true;
                }
                threadSleep(100);
                continue;
            } else {
                initial = readListInFile(input);
                if (readListInFile(input).size() != initial.size()) {
                    log.println("LIST NOT THE SAME SIZE!! CAUGHT THE FUCKER");
                    continue;
                } else
                    break;
            }

        }

        return readListInFile(input);
    }

    //00:26:49
    //given a valid duration string, return how many seconds will pass
    public static int getSecondsFromDuration(String duration) {
        String[] splitted = duration.split(":");

        int hours_in_seconds = (Integer.parseInt(splitted[0])) * 3600;
        int minutes_in_seconds = (Integer.parseInt(splitted[1])) * 60;
        int seconds = (Integer.parseInt(splitted[2]));
        return hours_in_seconds + minutes_in_seconds + seconds;
    }

    public static String getLexiconValue(int digits, int x) {
        String input = x + "";

        while (input.length() < digits) {
            input = "0" + input;
        }

        return input;
    }


}
