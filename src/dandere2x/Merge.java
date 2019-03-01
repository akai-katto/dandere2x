package dandere2x;

import dandere2x.Utilities.DandereUtils;
import dandere2x.Utilities.VectorDisplacement;
import wrappers.Frame;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.List;

import static java.io.File.separator;
import static java.lang.System.exit;

public class Merge implements Runnable {

    private int blockSize;
    private int bleed;
    private String workspace;
    private int frameCount;
    private int lexiConstant = 6;
    private PrintStream log;
    private int currentFrame;

    public Merge(int blockSize, int bleed, String workspace, int frameCount) {
        this.blockSize = blockSize;
        this.bleed = bleed;
        this.workspace = workspace;
        this.frameCount = frameCount;

        try {
            log = new PrintStream(new File(workspace + "logs" + separator + "merge_logfile.txt"));
        } catch (FileNotFoundException e) {
            System.out.println("Fatal Error: Could not create file at " + workspace + "logs" + separator + "merge_logfile.txt");
        }
    }


    /**
     * The first upscaled frame can be seen as a degenerate frame to an extent, it stands on it's own,
     * while all preceding frames are derived from previous frames.
     * <p>
     * To articulate, frame2, frame3, and frame4 may have pieces of frame1 in it. Furthermore, it's possible
     * for frame 1200 to have a piece of frame1 in it, so frame1 needs to be seen as different.
     * <p>
     * We wait for 'upscaled' differences to be outputed by waifu2x to be stitched over
     * the previous frame. We apply the neccecary predictive vectors to move parts of the image
     * around to create the image we want.
     * <p>
     * Once we construct an image out of upscaled differences and predictive vectors, this image becomes the base
     * for the preceding frame.
     */
    public void run() {

        setCurrentFrame(); //check if resuming or not
        //load genesis frame
        Frame base = DandereUtils.listenImage(log, workspace + "merged" + separator + "merged_" + currentFrame + ".jpg");

        for (int x = currentFrame; x < frameCount; x++) {
            log.println("Mering frame " + x);
            String inputName;

            if (DandereUtils.isLinux())
                inputName = workspace + "upscaled" + separator + "output_" + x + ".png";
            else
                inputName = workspace + "upscaled" + separator + "output_" + DandereUtils.getLexiconValue(lexiConstant, x) + ".png";


            //load the image 'upscaled differences', and using the data generated, create a new frame with it.
            Frame inversion = DandereUtils.listenImage(log, inputName);
            List<String> listPredictive = DandereUtils.listenText(log, workspace + "pframe_data" + separator + "pframe_" + x + ".txt");
            List<String> listInversion = DandereUtils.listenText(log, workspace + "inversion_data" + separator + "inversion_" + x + ".txt");

            //create and save the new frame using the predictive differences generated, then set the new frame as the new base
            base = createPredictive(x, inversion, base,
                    listPredictive, listInversion,
                    workspace + "merged" + separator + "merged_" + (x + 1) + ".jpg");

        }
    }


    /**
     * The protocol for resuming a dandere2x run is pretty similiar to that of starting a new one,
     * just change the 'current' frame so we don't have to start from scratch.
     *
     * Count how many images have been upscaled, and that's own new starting point.
     *
     * -1 in case previous image didnt save correctly.
     */
    public void setCurrentFrame(){

        int frameCount = DandereUtils.getFileTypeInFolder(workspace + "merged" + separator,".jpg").size();

        if(frameCount==0 || frameCount == 1){
            System.out.println("new merged session");
            this.currentFrame = 1;
        }else {
            System.out.println("resuming merged session");
            System.out.println(frameCount);
            this.currentFrame = frameCount;
        }
        return;
    }


    /**
     * @param frame          framenumber is essentially unused, just here for debuggign
     * @param inversion      image containing the missing parts
     * @param base           the previous frame in which we draw over
     * @param listPredictive vectors of predictive /interpolated frames
     * @param listInversion  vectors needed to piece inversion back into the larger image
     * @param outLocation
     * @returns a image craeted from the base, modifies the pixels based on predictive, and draws the inversion frames over the respective location.
     */
    private Frame createPredictive(int frame, Frame inversion, Frame base, List<String> listPredictive, List<String> listInversion, String outLocation) {
        Frame out = new Frame(base.width, base.height);

        ArrayList<VectorDisplacement> vectorDisplacements = new ArrayList<>();
        ArrayList<VectorDisplacement> inversionDisplacements = new ArrayList<>();


        //read every predictive vector and put it into an arraylist
        for (int x = 0; x < listPredictive.size() / 4; x++) {
            vectorDisplacements.add(
                    new VectorDisplacement(Integer.parseInt(listPredictive.get(x * 4)), Integer.parseInt(listPredictive.get(x * 4 + 1)),
                            Integer.parseInt(listPredictive.get(x * 4 + 2)),
                            Integer.parseInt(listPredictive.get(x * 4 + 3))));
        }

        //read every inversion vector and put it into an arraylist
        for (int x = 0; x < listInversion.size() / 4; x++) {
            inversionDisplacements.add(
                    new VectorDisplacement(Integer.parseInt(listInversion.get(x * 4)), Integer.parseInt(listInversion.get(x * 4 + 1)),
                            Integer.parseInt(listInversion.get(x * 4 + 2)),
                            Integer.parseInt(listInversion.get(x * 4 + 3))));
        }


        //if it is the case that both lists are empty, then the upscaled image is the new frame.
        //This is because if we have no predictive vectors, then the image we're looking at
        //right now has nothing to do with the previous frame
        if (inversionDisplacements.isEmpty() && vectorDisplacements.isEmpty()) {
            log.println("frame is a brand new frame, saving frame");
            out = inversion;
            out.saveFile(outLocation);
            return out;
        }

        //if it is a pFrame but we don't have any inversion items, then simply copy the previous frame.
        //In other words, if there is no inversionDisplacements, the last scene is identical. (inversion Displacements
        //are generated when two frames are non identical.
        if (inversionDisplacements.isEmpty() && !vectorDisplacements.isEmpty()) {
            log.println("frame is identical to previous frame");
            base.saveFile(outLocation);
            return base;
        }

        try {
            //piece together the image using predictive information
            for (int outer = 0; outer < vectorDisplacements.size(); outer++) {
                for (int x = 0; x < blockSize * 2; x++) {
                    for (int y = 0; y < blockSize * 2; y++) {
                        out.set(x + 2 * vectorDisplacements.get(outer).x, y + 2 * vectorDisplacements.get(outer).y,
                                base.getNoThrow(x + 2 * vectorDisplacements.get(outer).newX, y + 2 * vectorDisplacements.get(outer).newY));
                    }
                }
            }

            //put inversion (the missing) information into the image
            for (int outer = 0; outer < inversionDisplacements.size(); outer++) {
                for (int x = 0; x < (blockSize * 2); x++) {
                    for (int y = 0; y < (blockSize * 2); y++) {
                        out.set(inversionDisplacements.get(outer).x * 2 + x, inversionDisplacements.get(outer).y * 2 + y,
                                inversion.get(inversionDisplacements.get(outer).newX * (2 * (blockSize + bleed)) + x + bleed, inversionDisplacements.get(outer).newY * (2 * (blockSize + bleed)) + y + bleed));

                    }
                }
            }
        } catch (ArrayIndexOutOfBoundsException e) {
            log.println("Critical Error: Frame " + frame + " caused an unexpected out of bounds exception");
            log.println(e.toString());
            log.println("Program will terminate");
            exit(1);
        }

        log.println("Saving frame " + frame);
        //save the new predictive frame
        out.saveFile(outLocation);

        //reduce time needed at runtime by returning the new image as to not have to load it again
        return out;
    }


}
