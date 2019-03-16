import dandere2x.Dandere2x;
import dandere2x.Utilities.ParseConfig;
import wrappers.Frame;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintStream;


//3-2-19

//found a major design flaw. Todo , fix bleeding
//error. Bleeding is hard coded severeley for 2x. Figure it out!

public class main {

    public static void main(String[] args) throws Exception {

        //create main log
        PrintStream log = null;
        File logFile = new File("log.txt");
        try {
            log = new PrintStream(logFile);
        } catch (FileNotFoundException e) {
            System.out.println("could not create log");
        }
        log.println("log created");


        //parse config.txt
        ParseConfig parse = new ParseConfig("config.txt");
        if (parse.logVerify(log)) {
            log.println("Valid config");
            Dandere2x sesh = new Dandere2x(parse);
            sesh.start();
        } else {
            log.println("Invalid config, check log.txt");
        }

    }
}
