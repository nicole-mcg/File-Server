package org.cmcg.runserver;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

/**
 A simple java program to start the file server
// This is used to create cross-platform runnable commands in the root directory
 * 
 * @author Connor
 *
 */
public class RunServer {

    // In the future, this will also be used to run the file server using Jython.
    // Jython will run the file server in a safe cross-platform Java environment, as well as avoid the need to install Python.
    // (Java is more likely to be installed)

    public static void main(String... args) {

        // Get runtime handle
        Runtime runTime = Runtime.getRuntime();

        Process process;

        // Start execution of the python file server
        try {
            process = runTime.exec("python -m file_server.__init__ ../test_directories/serv_dir");
        } catch (IOException e) {
            System.out.println("Unable to start Python file-server.");
            System.out.println(e);
            return;
        }

        // Get reader for console output
        BufferedReader stdInput = new BufferedReader(
                new InputStreamReader(process.getInputStream()));

        // Get reader for error output
        BufferedReader stdError = new BufferedReader(
                new InputStreamReader(process.getErrorStream()));

        String line;

        try {

            // Read output from the command
            while ((line = stdInput.readLine()) != null) {
                System.out.println(line);
            }

        } catch (IOException e) {
            System.out.println("Error reading process output.");
            System.out.println(e);
        }

        try {

            // Read any errors from command
            while ((line = stdError.readLine()) != null) {
                System.out.println(line);
            }

        } catch (IOException e) {
            System.out.println("Error reading process output.");
            System.out.println(e);
        }

    }

}