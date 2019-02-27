package dandere2x.Utilities;

/**
 * Imagine we have an image like this
 * <p>
 * frame1:
 * <p>
 * 11111
 * 11111
 * 11122
 * 11111
 * <p>
 * and frame2 is like
 * <p>
 * <p>
 * 11111
 * 11122
 * 11111
 * 11111
 * <p>
 * our inversion displacement keeps track of the movement of 2's,
 * <p>
 * so the initial x and 3,3 and new x and new y is 2,3
 **/
public class VectorDisplacement implements java.io.Serializable {
    public int size;
    public int x;
    public int y;
    public int newX;
    public int newY;

    public VectorDisplacement(int x, int y, int newX, int newY) {
        this.x = x;
        this.y = y;
        this.newX = newX;
        this.newY = newY;
    }


    @Override
    public String toString() {
        return " x " + x + " y " + y + " newX " + newX + " newY " + newY;
    }

}
