import javafx.application.Platform;
import javafx.scene.control.CheckBox;
import javafx.scene.control.CustomMenuItem;

import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;

public class ProgramRunner extends Thread {

    private String url;
    private Consumer<String> callBack; // Signals the javafx thread to do stuff
    private int programsIndex;
    private String args;
    private String os;
    private String fileName;


    // Use this constructor if you are trying to run one of the trading analysis programs such as the spread grouper
    // program.
    public ProgramRunner(String webUrl, Consumer<String> callBack)
    {
        this.callBack = callBack;
        url = webUrl;
        programsIndex = 0;
        os = System.getProperty("os.name");
        args = "";
        fileName = url.split("/")[4];
    }

    public void setArgs(String newArgs)
    {
        synchronized (args) {
            args = newArgs;
        }
    }

    public void run()
    {
        ProcessBuilder program;

        // should consider adding this code to the constructor
        File workingDur = new File(System.getProperty("user.dir"));
        String parDur = workingDur.getParent();



        // signal GUI to put waiting screen up
        callBack.accept("Wait");

        if (os.contains("Mac"))
            program = new ProcessBuilder("python3", "letterboxd_scraper.py", url);
        else
            program = new ProcessBuilder("python", "letterboxd_scraper.py", url);

        program.directory(new File(parDur));
        program.inheritIO(); // <-- passes IO from forked process.
        try {
            Process p = program.start(); // <-- forkAndExec on Unix
            p.waitFor(); // <-- waits for the forked process to complete.
        } catch (Exception exception) {
            exception.printStackTrace();
        }


        if (os.contains("Mac"))
            program = new ProcessBuilder("python3", "analyzer_1.4.py", fileName+".json");
        else
            program = new ProcessBuilder("python", "analyzer_1.4.py", fileName+".json");

//        program.directory(new File(parDur + "/sentiment_analysis_model"));
        program.directory(new File(parDur));
        program.inheritIO(); // <-- passes IO from forked process.
        try {
            Process p = program.start(); // <-- forkAndExec on Unix
            p.waitFor(); // <-- waits for the forked process to complete.
        } catch (Exception exception) {
            exception.printStackTrace();
        }

        callBack.accept("Results");
    }
}
