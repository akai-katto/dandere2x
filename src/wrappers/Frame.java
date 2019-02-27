package wrappers;

import javax.imageio.IIOImage;
import javax.imageio.ImageIO;
import javax.imageio.ImageWriteParam;
import javax.imageio.ImageWriter;
import javax.imageio.plugins.jpeg.JPEGImageWriteParam;
import javax.imageio.stream.FileImageOutputStream;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;


public class Frame {

    private final static int opaque = new Color(0.0f, 0.0f, 0.0f, 0.0f).getRGB();
    public int height;
    public int width;
    public String imageURL;
    private BufferedImage image;
    private File f;


    /**
     * Loads an image via URL. Throws on failure to load.
     *
     * @param url
     */
    public Frame(String url) {
        try {
            image = ImageIO.read(new File(url));
        } catch (IOException e) {
            System.out.println(e);
            System.out.println("error trying to load url: " + url);
            throw new IllegalArgumentException("invalid url");
        } catch (NullPointerException e) {
            System.out.println(e);
            System.out.println("null ptr exception: " + url);
            throw new NullPointerException("null ptr");
        }
        this.imageURL = url;
        this.height = image.getHeight();
        this.width = image.getWidth();
    }


    /**
     * Directly load an image via a file. Optimization isn't an issue, unused at the moment.
     *
     * @param file
     */
    public Frame(File file) {
        try {
            image = ImageIO.read(file);
        } catch (IOException e) {
            System.out.println(e);
            throw new IllegalArgumentException("invalid file");
        }
        this.height = image.getHeight();
        this.width = image.getWidth();
        this.imageURL = file.getAbsolutePath();
    }


    /**
     * Manually create a blank image. Black is default. Used for constructing difference images
     *
     * @param height
     * @param width
     */
    public Frame(int width, int height) {
        if (height <= 0 || width <= 0)
            throw new IllegalArgumentException("height / width must be above zero and non neg");

        try {
            image = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
        } catch (NullPointerException e) {
            System.out.println(e);
            System.out.println("null ptr exception on custom image ");
            throw new NullPointerException("null ptr");
        }
        this.height = height;
        this.width = width;
    }


    /**
     * Replaces an RGB at a given x y point with an RGB represent in int form.
     *
     * @param x
     * @param y
     * @param rgb
     */
    public void setRGB(int x, int y, int rgb) {
        try {
            image.setRGB(x, y, rgb);
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("setrgb index out of bound");
            System.out.println("File " + imageURL);
            System.out.println("width max " + width);
            System.out.println("height max " + height);
            System.out.println("error: x" + x);
            System.out.println("error: y" + y);
            throw new IllegalArgumentException("invalid pixels");
        }
    }


    /**
     * Replaces the RGB at a given x y with a Color object.
     *
     * @param x
     * @param y
     * @param color
     */
    public void set(int x, int y, Color color) {
        int rgb = color.getRGB();

        try {
            image.setRGB(x, y, rgb);
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("setrgb index out of bound");
            System.out.println("File " + imageURL);
            System.out.println("width max " + width);
            System.out.println("height max " + height);
            System.out.println("error: x" + x);
            System.out.println("error: y" + y);
            throw new IllegalArgumentException("invalid pixels");
        }
    }


    /**
     * Used during experimental Dandere but not used anymore.
     *
     * @param x
     * @param y
     */
    public void setOpaque(int x, int y) {
        image.setRGB(x, y, opaque);
    }


    /**
     * Currently unused. Returns integer value of a pixel.
     *
     * @param x
     * @param y
     * @return
     */
    public int getRGB(int x, int y) {
        try {
            image.getRGB(x, y);
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("index out of bound");
            System.out.println("setrgb index out of bound");
            System.out.println("File " + imageURL);
            System.out.println("error: x" + x);
            System.out.println("error: y" + y);
            throw new IllegalArgumentException("invalid input");
        }
        return image.getRGB(x, y);
    }


    /**
     * Returns Color object of a pixel
     *
     * @param x
     * @param y
     * @return
     */
    public Color get(int x, int y) {
        try {
            return new Color(image.getRGB(x, y));
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("index out of bound");
            System.out.println("getrgb index out of bound");
            System.out.println("File " + imageURL);
            System.out.println("error: x" + x);
            System.out.println("error: y" + y);
            throw new IllegalArgumentException("invalid input");
        }
    }


    /**
     * Used when generating bleeds. Sometimes there's no area to bleed into, so we just fill in white
     * in the absence of information.
     *
     * @param x
     * @param y
     * @return
     */
    public Color getNoThrow(int x, int y) {
        try {
            return new Color(image.getRGB(x, y));
        } catch (ArrayIndexOutOfBoundsException e) {
            return Color.WHITE;
        }
    }

    /**
     * Saves image to JPEG using minimal compression. Credit to:
     * credit to stackoverflow.com/questions/17108234/setting-jpg-compression-level-with-imageio-in-java
     * <p>
     * for his elegant solution.
     * <p>
     * We don't save to PNG because PNG takes too long - 'merge' function will bottleneck if saving images in raw.
     *
     * @param output
     */
    public void saveFile(String output) {
        JPEGImageWriteParam jpegParams = new JPEGImageWriteParam(null);
        jpegParams.setCompressionMode(ImageWriteParam.MODE_EXPLICIT);
        jpegParams.setCompressionQuality(1f);
        final ImageWriter writer = ImageIO.getImageWritersByFormatName("jpg").next();
        try {
            writer.setOutput(new FileImageOutputStream(
                    new File(output)));
            writer.write(null, new IIOImage(image, null, null), jpegParams);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    /**
     * Unused function when Dandere was parallized. Leaving in for potential to parallize Dandere in future.
     *
     * @param output
     */
    public void saveFileThreaded(String output) {
        JPEGImageWriteParam jpegParams = new JPEGImageWriteParam(null);
        jpegParams.setCompressionMode(ImageWriteParam.MODE_EXPLICIT);
        jpegParams.setCompressionQuality(1f);
        Thread t = new Thread() {
            public void run() {
                JPEGImageWriteParam jpegParams = new JPEGImageWriteParam(null);
                jpegParams.setCompressionMode(ImageWriteParam.MODE_EXPLICIT);
                jpegParams.setCompressionQuality(1f);
                final ImageWriter writer = ImageIO.getImageWritersByFormatName("jpg").next(); // specifies where the jpg image has to be written
                try {
                    writer.setOutput(new FileImageOutputStream(
                            new File(output)));
                    writer.write(null, new IIOImage(image, null, null), jpegParams);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        };
        t.start();
    }

}
