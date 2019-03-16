package wrappers;

import dandere2x.Utilities.DThread;
import dandere2x.Utilities.DandereUtils;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintStream;

import static java.io.File.separator;

//wrapper for dandere2xCpp in a thread / runnable version
public class Dandere2xCpp extends DThread {

    private Process dandere2xCppProc;
    private String runType;
    private int count;
    private String workspace;
    private PrintStream log;
    private String dandere2xCppDir;
    private int frameCount;
    private int blockSize;
    private int stepSize;
    private double psnrHigh;
    private double psnrLow;
    private double tolerance;

    public Dandere2xCpp(String workspace, String dandere2xCppDir, int frameCount, int blockSize, double tolerance, double psnrHigh, double psnrLow,
                        int stepSize, boolean isResume) {
        super(isResume);

        try {
            log = new PrintStream(new File(workspace + "logs" + separator + "dandere2xcpp_logfile.txt"));
        } catch (FileNotFoundException e) {
            System.out.println("Fatal Error: Could not create file at " + workspace + "logs" + separator + "dandere2xcpp_logfile.txt");
        }

        this.workspace = workspace;
        this.dandere2xCppDir = dandere2xCppDir;
        this.frameCount = frameCount;
        this.blockSize = blockSize;
        this.stepSize = stepSize;
        this.tolerance = tolerance;
        this.psnrHigh = psnrHigh;
        this.psnrLow = psnrLow;

        this.count = 0;

        if (isResume) {
            log.println("resuming dandere2xcpp session");
            resumeCondition();
        } else {
            log.println("new dandere2xcpp session");
            this.runType = "n";
        }
    }

    @Override
    public void run() {
        log.println("initiating shutdown hook");
        shutdownHook();

        ProcessBuilder dandere2xPB = getDandere2xPB();
        try {
            dandere2xCppProc = dandere2xPB.start();
        } catch (IOException e) {
            e.printStackTrace();
        }
        while (dandere2xCppProc.isAlive()) ;
    }

    @Override
    public void resumeCondition() {
        count = DandereUtils.getFileTypeInFolder(workspace + "pframe_data", ".txt").size();
        if (count != 0) {
            new File(workspace + "pframe_data" + separator + "pframe_" + count).delete();
            new File(workspace + "inversion_data" + separator + "inversion_" + count).delete();
            log.println("Resuming Dandere2x Session: " + count);
            this.runType = "r";
        }
    }

    //if program exits and dandere2xCppProc is still running, close that up
    private void shutdownHook() {
        Runtime.getRuntime().addShutdownHook(new Thread() {
            public void run() {
                if (dandere2xCppProc.isAlive()) {
                    System.out.println("Unexpected shutting down before dandere2xCppProc finished! Attempting to close");
                    log.println("Unexpected shutting down before dandere2xCppProc finished! Attempting to close");
                    dandere2xCppProc.destroyForcibly();
                    System.out.println("Exiting..");
                    log.println("Exiting..");
                }
            }
        });
    }

    /**
     * IF we're on linux, create the script for the user to run. The process builder command
     * to start waifu2x-cpp is also different than that of windows.
     */
    private ProcessBuilder getDandere2xPB() {

        ProcessBuilder dandere2xPB;

        if (DandereUtils.isLinux()) {
            log.println("using linux...");
            dandere2xPB = new ProcessBuilder(dandere2xCppDir,
                    workspace, frameCount + "", blockSize + "", tolerance + "", stepSize + "", runType, count + "");
        } else {
            log.println("using windows...");
            dandere2xPB = new ProcessBuilder("cmd.exe", "/C", "start", dandere2xCppDir,
                    workspace, frameCount + "", blockSize + "", tolerance + "", psnrHigh + "", psnrLow + "", stepSize + "", runType, count + "");
        }

        return dandere2xPB;
    }

}
