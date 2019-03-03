package wrappers;

import dandere2x.Utilities.DandereUtils;

import java.io.File;
import java.io.IOException;
import java.io.PrintStream;

import static java.io.File.separator;

public class FFMpeg {

    /**
     * Extracts audio in the same regard as 'extract frames' would function.
     * For windows, ffmpeg is included by default, so one needs to manually
     * download it and set it's path, or just set the exectutables location as the 'ffMpeg' string
     *
     * @param workspace
     * @param timeFrame
     * @param fileName
     * @param audioLayer
     * @param duration
     */
    public static void extractAudio(PrintStream log, String ffmpegDir, String workspace, String timeFrame, String duration, String fileName, String audioLayer) {

        Process proc = null;
        Runtime run = Runtime.getRuntime();
        String command;

        if (DandereUtils.isLinux()) {
            log.println("extracting audio on linux..");
            command = "ffmpeg  -ss " + timeFrame + " -i " + fileName +
                    " -t " + duration + " -map " + audioLayer + " " + workspace + "audio.mp3";
        } else {
            log.println("extracting frames on windows...");
            command = "cmd.exe /C start " + ffmpegDir + " -ss " + timeFrame + " -i " + fileName +
                    " -t " + duration + " -map " + audioLayer + " " + workspace + "audio.mp3";
        }
        log.println("audio extraction command ..." + command);


        try {
            log.println("running command " + command);
            proc = run.exec(command);
        } catch (IOException e) {
            e.printStackTrace();
            log.println("fatal error: Could not execute extract audio! Running will continue");
            log.print(e.toString());
            System.out.println("fatal error: Could not execute extract audio! Running will continue");
        }

        synchronized (proc) {
            while (proc.isAlive()) {
                try {
                    log.println("proc is alive");
                    proc.wait(250);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
        synchronized (proc) {
            try {
                proc.wait(1000);
            } catch (InterruptedException e) {

            }
        }
    }


    public static void extractFrames(PrintStream log, String ffmpegDir, String workspace, String timeFrame,
                                     String fileName, String duration, int frameRate) {

        log.println("Extracting frames at " + workspace);
        new File(workspace + "inputs").mkdir();

        Process process = null;
        Runtime run = Runtime.getRuntime();

        String command;

        if (DandereUtils.isLinux()) {
            log.println("extracting frames on linux...");
            command = "ffmpeg  -ss " + timeFrame + " -i " + fileName + " -r " + frameRate + " -qscale:v 2 " +
                    " -t " + duration + " " + workspace + "inputs" + separator + "frame%01d.jpg";
        } else {
            log.println("extracting frames on windows..");
            command = "cmd.exe /C start " + ffmpegDir + " -ss " + timeFrame + " -i " + fileName + " -r "
                    + frameRate + " -qscale:v 2 " + " -t " + duration + " " + workspace + "inputs" + separator + "frame%01d.jpg";
        }

        log.println("command for frame extraction: " + command);


        try {
            log.println("running command " + command);
            process = run.exec(command);
        } catch (IOException e) {
            e.printStackTrace();
            log.println("fatal error: Could not execute extract frames!");
            log.print(e.toString());
            System.out.println("fatal error: Could not execute extract frames!");
        }

        try {
            process = run.exec(command);
        } catch (IOException e) {
            e.printStackTrace();
        }

        synchronized (process) {
            while (process.isAlive()) {
                try {
                    log.println("waiting for process to extract frames");
                    process.wait(250);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }

        log.println("extracted frames");
    }
}
