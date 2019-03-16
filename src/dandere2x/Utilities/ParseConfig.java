package dandere2x.Utilities;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.util.Enumeration;
import java.util.Properties;

import static java.io.File.separator;
import static java.lang.System.exit;

/**
 * A very disinteresting file checking the validity of a Dandere2x session.
 */
public class ParseConfig {


    private Properties prop;

    public ParseConfig(String input) {
        this.prop = new Properties();
        try {
            prop.load(new FileInputStream(input));
        } catch (IOException e) {
            System.out.println("config file not found");
            e.printStackTrace();
            exit(1);
        }

        String dir = null;
        try {
            dir = new File(".").getCanonicalPath() + separator;
        } catch (IOException e) {
            e.printStackTrace();
            exit(1);
        }

        Enumeration keys = prop.keys();
        while (keys.hasMoreElements()) {
            String key = (String) keys.nextElement();
            if (prop.getProperty(key).contains("[this]"))
                prop.setProperty(key, prop.getProperty(key).replace("[this]", dir));
        }
    }

    /**
     * Doesnt test if lua file is correct, just if it exists
     *
     * @param location
     * @return
     */
    public static boolean dandereLuaValid(String location) {

        if (location == null) {
            return false;
        }
        if (!new File(location).exists()) {
            return false;
        }

        return location.contains("dandere.lua");
    }

    /**
     * Verify workspace exists before continuing
     *
     * @param location
     * @return
     */
    public static boolean workspaceValid(String location) {
        if (location == null) {
            return false;
        }

        if (!new File(location).exists()) {
            new File(location).mkdir();
            return new File(location).exists();
        }
        return true;
    }
    //to do, need to parse blockSizes and what not

    public static boolean fileValid(String fileName) {


        if (fileName == null) {
            return false;
        }

        return new File(fileName).exists();
    }

    /**
     * Ensures a user inputs a valid ffmpeg time
     *
     * @param time
     * @return
     */
    public static boolean timeValid(String time) {

        if (time == null) {
            return false;
        }

        if (time.length() != 8) {
            return false;
        }

        if (time.charAt(2) != ':' && time.charAt(5) != ':') {
            return false;
        }

        for (int x = 0; x < time.length(); x++) {
            if (x == 2 || x == 5)
                continue;
            if (!Character.isDigit(time.charAt(x))) {
                return false;
            }
        }

        String[] splitTime = time.split(":");

        for (int x = 0; x < splitTime.length; x++) {
            if (Integer.parseInt(splitTime[x]) >= 60) {
                return false;
            }
        }
        return true;
    }

    /**
     * Ensures user inputs a valid audio track
     *
     * @param track
     * @return
     */
    public static boolean audioLayerValid(String track) {

        if (track == null) {
            return false;
        }

        if (track.length() != 3) {
            return false;
        }

        if (track.charAt(1) != ':') {
            return false;
        }
        for (int x = 0; x < track.length(); x++) {
            if (x == 1)
                continue;
            if (!Character.isDigit(track.charAt(x))) {
                return false;
            }
        }
        return true;
    }

    public static boolean blockSizeValid(int blocksize, int height, int width) {
        return height % blocksize == 0 && width % blocksize == 0;
    }

    //very config without logging
    public boolean verify() {
        PrintStream print = new PrintStream((System.out));
        return logVerify(print);
    }

    /**
     *
     */
    public boolean logVerify(PrintStream log) {

        boolean returnStatement = true;

        //file directories
        String dandereDir = prop.getProperty("dandereDir");
        String workspace = prop.getProperty("workspace");
        String fileDir = prop.getProperty("fileDir");
        String dandere2xCppDir = prop.getProperty("dandere2xCppDir");
        String waifu2xCaffeCUIDir = prop.getProperty("waifu2xCaffeCUIDir");
        String ffmpegDir = prop.getProperty("ffmpegDir");

        //session settings
        String timeFrame = prop.getProperty("timeFrame");
        String duration = prop.getProperty("duration");
        String audioLayer = prop.getProperty("audioLayer");
        int width = Integer.parseInt(prop.getProperty("width"));
        int height = Integer.parseInt(prop.getProperty("height"));

        //user settings //TODO
        int blockSize = Integer.parseInt(prop.getProperty("blockSize"));
        int stepSize = Integer.parseInt(prop.getProperty("stepSize"));
        double tolerance = Double.parseDouble(prop.getProperty("tolerance"));
        String noiseLevel = prop.getProperty("noiseLevel");
        String processType = prop.getProperty("processType");
        int frameRate = Integer.parseInt(prop.getProperty("frameRate"));
        int bleed = Integer.parseInt(prop.getProperty("bleed"));


        if (!ParseConfig.blockSizeValid(blockSize, height, width)) {
            System.out.println("--Invalid BlockSize--");
            System.out.println("Your input: " + blockSize);
            System.out.println("Valid blocksizes for your resolution are:");

            for (int x = 1; x < 250; x++) {
                if (height % x == 0 && width % x == 0) {
                    log.print(x + ", ");
                }
            }
             System.out.println();
            returnStatement = false;
        }

        if (DandereUtils.isLinux()) {
            if (!ParseConfig.dandereLuaValid(dandereDir)) {
                 System.out.println("--Invalid dandereDir--");
                 System.out.println("Your input: " + dandereDir);
                returnStatement = false;
            }
        }

        if (!ParseConfig.workspaceValid(workspace)) {
             System.out.println("--Invalid Workspace--");
             System.out.println("Your input: " + workspace);
            returnStatement = false;
        }

        if (!ParseConfig.fileValid(fileDir)) {
             System.out.println("--Invalid Filedir--");
             System.out.println("Your input: " + fileDir);
            returnStatement = false;
        }

        if (!ParseConfig.fileValid(dandere2xCppDir)) {
             System.out.println("--Invalid Dandere2xCPPDir--");
             System.out.println("Your input: " + dandere2xCppDir);
            returnStatement = false;
        }

        if (!DandereUtils.isLinux()) {
            if (!ParseConfig.fileValid(waifu2xCaffeCUIDir)) {
                 System.out.println("--Invalid waifu2xCaffeCUIDir--");
                 System.out.println("Your input: " + waifu2xCaffeCUIDir);
                returnStatement = false;
            }
        }

        if (!DandereUtils.isLinux()) {
            if (ffmpegDir.equals("ffmpeg")) {
                 System.out.println("Using default ffmpeg");
            } else if (!ParseConfig.fileValid(ffmpegDir)) {
                 System.out.println("--Invalid ffmpegDir--");
                 System.out.println("Your input: " + ffmpegDir);
                returnStatement = false;
            }
        }

        if (!ParseConfig.timeValid(timeFrame)) {
             System.out.println("--Invalid timeFrame--");
             System.out.println("Your input: " + timeFrame);
            returnStatement = false;
        }

        if (!ParseConfig.timeValid(duration)) {
             System.out.println("--Invalid Duration--");
             System.out.println("Your input: " + duration);
            returnStatement = false;
        }

        if (!ParseConfig.audioLayerValid(audioLayer)) {
             System.out.println("--Invalid audiolayer--");
             System.out.println("Your input: " + audioLayer);
            returnStatement = false;
        }

        return returnStatement;
    }

    public Properties getProp() {
        return prop;
    }


}
