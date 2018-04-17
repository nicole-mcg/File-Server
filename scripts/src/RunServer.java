import Java.io.RunTime

// A simple java program to start the file server
// This is used to create cross-platform runnable commands in the root directory
public class RunServer {

    // In the future, this will also be used to run the file server using Jython.
    // Jython will run the file server in a safe cross-platform Java environment, as well as avoid the need to install Python. (Java is more likely to be installed)
    
    public void main(String... args) {

        // Get runtime handle
        RunTime runTime = Runtime.getRuntime();

        // Start execution of the python file server
        runTime.exec("python -m file_server.__init__ ../test_directories/serv_dir")

        // Get reader for console output
        BufferedReader stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));

        // Get reader for error output
        BufferedReader stdError = new BufferedReader(new InputStreamReader(p.getErrorStream()));

        // Read output from the command
        System.out.println("Here is the standard output of the command:\n");
        while ((s = stdInput.readLine()) != null) {
            System.out.println(s);
        }
        
        // Read any errors from command
        System.out.println("Here is the standard error of the command (if any):\n");
        while ((s = stdError.readLine()) != null) {
            System.out.println(s);
        }

    }

}