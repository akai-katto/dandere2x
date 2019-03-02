package dandere2x;

import dandere2x.Utilities.DThread;
import dandere2x.Utilities.DandereUtils;
import dandere2x.Utilities.VectorDisplacement;
import wrappers.Frame;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.List;

import static java.io.File.separator;

public class Difference extends DThread implements Runnable {

    private int blockSize;
    private int bleed;
    private String workspace;
    private int imageCount;
    private int lexiConstant = 6;
    private PrintStream log;
    private int currentFrame = 1; // allow this to be modifiable in event of resume

    public Difference(int blockSize, int bleed, String workspace, int imageCount, boolean isResume) {
        super(isResume);
        try {
            log = new PrintStream(new File(workspace + "logs" + separator + "difference_logfile.txt"));
        } catch (FileNotFoundException e) {
            System.out.println("Fatal Error: Could not create file at " + workspace + "merge_logfile.txt");
        }

        new File(workspace + "outputs" + separator + "metadata" + separator).mkdir();


        this.blockSize = blockSize;
        this.bleed = bleed;
        this.workspace = workspace;
        this.imageCount = imageCount;

        if(isResume)
            resumeCondition();


    }


    @Override
    public void resumeCondition(){
        setCurrentFrame();
    }

    /**
     * The protocol for resuming a dandere2x run is pretty similiar to that of starting a new one,
     * just change the 'current' frame so we don't have to start from scratch.
     *
     * Count how many images have been upscaled, and that's own new starting point
     *
     *
     * -1 in case previous image didnt save correctly.
     */
    public void setCurrentFrame(){

        int frameCount = DandereUtils.getFileTypeInFolder(workspace + "outputs" + separator + "metadata" + separator,".txt").size();

        if(frameCount==0 || frameCount == 1){
            log.println("new session");
            this.currentFrame = 1;
        }else {
            log.println("resuming session: " + (frameCount-1+""));
            this.currentFrame = frameCount-1;
        }
        return;
    }

    @Override
    /**
     * Wait for the predictive data and inversion data to exist, then create the 'differences' image
     * that will be upscaled later by waifu2x.
     * <p>
     * We do this by using the raw frames outputed from the video.
     */
    public void run() {

        for (int x = currentFrame; x < imageCount; x++) {
            log.println("Frame " + x);
            Frame im2 = DandereUtils.listenImage(log, workspace + "inputs" + separator + "frame" + (x + 1) + ".jpg");
            List<String> listPredictive = DandereUtils.listenText(log, workspace + "pframe_data" + separator + "pframe_" + x + ".txt");
            List<String> listInversion = DandereUtils.listenText(log, workspace + "inversion_data" + separator + "inversion_" + x + ".txt");

            saveInversion(x, im2, listPredictive,
                    listInversion,
                    workspace + "outputs" + separator + "output_" + DandereUtils.getLexiconValue(lexiConstant, x) + ".jpg");

            try {
                new File(workspace + "outputs" + separator + "metadata" + separator + "file" + x +".txt").createNewFile();
            } catch (IOException e) {
                e.printStackTrace();
            }

            saveDebug(x, im2, workspace + "debug" + separator + "debug_" + DandereUtils.getLexiconValue(lexiConstant, x) + ".jpg");
        }
    }





    /**
     * @param frameNumber
     * @param inputFile     the smaller image
     * @param listInversion we actually don't need predictive, it exists here to only let us know if we need to
     *                      completely redraw a frame or not.
     * @param listInversion we load the inversions from a textfile to create a list of vectors to recreate the missing parts of an image
     * @param outLocation   the output location
     * @return
     */
    private boolean saveInversion(int frameNumber, Frame inputFile, List<String> listPredictive, List<String> listInversion, String outLocation) {
        ArrayList<VectorDisplacement> inversionVectors = new ArrayList<>();

        //the size of the image needed is the square root (rougly) im dimensions. Might go over
        //sometimes, so we add + 1
        int size = (int) (Math.sqrt(listInversion.size() / 4) + 1) * (blockSize + bleed);
        Frame out = new Frame(size, size);


        //in the case where inversionVectors is empty but it is a predictive wrappers.Frame, then
        //simply output an irrelevent image, as the entire wrappers.Frame is to be copied .
        if (listInversion.isEmpty() && !listPredictive.isEmpty()) {
            Frame no = new Frame(1, 1);
            no.saveFile(outLocation);
            return true;
        }

        //in the case where both lists are empty, then we are upscaling a brand new wrappers.Frame, in which case,
        //otuput the entire image
        if (listInversion.isEmpty() && listPredictive.isEmpty()) {
            inputFile.saveFile(outLocation);
            return true;
        }
        //for every item in the listInversion, create vector displacements out of them in the same order they were saved
        for (int x = 0; x < listInversion.size() / 4; x++) {
            inversionVectors.add(
                    new VectorDisplacement(Integer.parseInt(listInversion.get(x * 4)), Integer.parseInt(listInversion.get(x * 4 + 1)),
                            Integer.parseInt(listInversion.get(x * 4 + 2)),
                            Integer.parseInt(listInversion.get(x * 4 + 3))));
        }


        //Use the vectors read to create a 'differences' image.
        for (int outer = 0; outer < inversionVectors.size(); outer++) {
            for (int x = 0; x < (blockSize + bleed); x++) {
                for (int y = 0; y < (blockSize + bleed); y++) {

                    out.set(
                            inversionVectors.get(outer).newX * (blockSize + bleed) + x,
                            inversionVectors.get(outer).newY * (blockSize + bleed) + y,
                            inputFile.getNoThrow(inversionVectors.get(outer).x + x - bleed / 2,
                                    inversionVectors.get(outer).y + y - bleed / 2));

                }
            }
        }


        //if none of the two cases above, we are working with a simple P wrappers.Frame.
        out.saveFile(outLocation);
        return true;
    }


    /**
     * This function exists mostly to see what Dandere2x is seeing.
     *
     * @param ImageNumber
     * @param Frame1
     * @param outLocation
     * @return
     */
    private boolean saveDebug(int ImageNumber, Frame Frame1, String outLocation) {
        List<String> listPredictive = DandereUtils.listenText(log, workspace + separator + "pframe_data" + separator
                + "pframe_" + ImageNumber + ".txt");

        int xBounds = Frame1.width;
        int yBounds = Frame1.height;

        Frame PDImage = new Frame(xBounds, yBounds);

        ArrayList<VectorDisplacement> blocks = new ArrayList<>();


        //read every predictive vector and put it into an arraylist
        for (int x = 0; x < listPredictive.size() / 4; x++) {
            blocks.add(
                    new VectorDisplacement(Integer.parseInt(listPredictive.get(x * 4)), Integer.parseInt(listPredictive.get(x * 4 + 1)),
                            Integer.parseInt(listPredictive.get(x * 4 + 2)),
                            Integer.parseInt(listPredictive.get(x * 4 + 3))));
        }


        for (int outer = 0; outer < blocks.size(); outer++) {
            for (int x = 0; x < blockSize; x++) {
                for (int y = 0; y < blockSize; y++) {
                    PDImage.set(x + blocks.get(outer).x, y + blocks.get(outer).y,
                            Frame1.getNoThrow(x + blocks.get(outer).newX, y + blocks.get(outer).newY));
                }
            }
        }

        PDImage.saveFile(outLocation);

        return true;
    }

}
