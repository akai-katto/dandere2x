package dandere2x.Utilities;


//"Dandere Thread"


/**
 * In order to reduce confusion / increase cohesion, this abstract class exists to express the need
 * for a few core functions that exist within
 */

/**
 * Forces resumeCondition to be set upon instantiating.
 */
public abstract class DThread implements Runnable {


    boolean isResume;
    public DThread(boolean isResume){
        this.isResume = isResume;
    }

    abstract public void run();
    abstract public void resumeCondition();
}
