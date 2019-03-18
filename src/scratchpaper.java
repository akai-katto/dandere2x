import dandere2x.Dandere2x;
import dandere2x.Utilities.ParseConfig;
import wrappers.Frame;
import wrappers.FrameOpaque;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintStream;


//3-2-19

//found a major design flaw. Todo , fix bleeding
//error. Bleeding is hard coded severeley for 2x. Figure it out!

public class scratchpaper {

    public static void main(String[] args) throws Exception {

        Frame frame1 = new Frame("C:\\Users\\windwoz\\Desktop\\workspace\\blindtest\\checkerlarge.png");
        Frame out = new Frame(3840, 2160);


        for(int x = 0; x < 3840; x++){
            for(int y = 0; y < 2160; y++){
                out.set(x,y,frame1.get(x + 2*(x/20), y + 2*(y/20)));
            }
        }

        out.saveFile("C:\\Users\\windwoz\\Desktop\\workspace\\blindtest\\uncheckeredlarge.png");

//        Frame f1 = new Frame("C:\\Users\\windwoz\\Desktop\\workspace\\blindtest\\inputs\\frame1.jpg");
//
//
//        FrameOpaque opaque = new FrameOpaque(1920 + 1920/10, 1080 + 1080 / 10);
//
//        for(int x = 0; x < opaque.width; x++){
//            for(int y = 0; y < opaque.height; y++){
//                opaque.setOpaque(x,y);
//            }
//        }
//
//
//        for(int x = 0; x < 1920; x++){
//            for(int y =0; y < 1080; y++){
//                opaque.set(x + x/10, y + y/ 10, f1.get(x,y));
//            }
//        }
//
//
//        opaque.saveTest("C:\\Users\\windwoz\\Desktop\\workspace\\blindtest\\savetest.png");
    }

}
