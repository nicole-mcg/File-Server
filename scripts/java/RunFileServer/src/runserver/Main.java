package runserver;

import java.io.File;
import java.util.ArrayList;

import runserver.process.ConsoleProcess;

/**
 * A simple java program to start the file server // This is used to create
 * cross-platform runnable commands in the root directory
 * 
 * @author Connor
 *
 */
public class Main {
	
	public static ArrayList<ConsoleProcess> clientProcesses;

	public static ConsoleProcess fileServerProcess;

	// In the future, this will also be used to run the file server using Jython.
	// Jython will run the file server in a safe cross-platform Java environment, as
	// well as avoid the need to install Python.
	// (Java is more likely to be installed)

	public static void main(String... args) {
		
		clientProcesses = new ArrayList<ConsoleProcess>();

		
		ProcessBuilder processBuilder = new ProcessBuilder("python", "-m", "file_server.__init__",
				"../test_directories/serv_dir");
		processBuilder.directory(new File("src"));
		
		new ConsoleProcess("File Server", processBuilder).runProcess();
	}

}