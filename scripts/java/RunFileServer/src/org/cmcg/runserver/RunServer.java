package org.cmcg.runserver;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.ProcessBuilder.Redirect;

/**
 * A simple java program to start the file server // This is used to create
 * cross-platform runnable commands in the root directory
 * 
 * @author Connor
 *
 */
public class RunServer {

	public static boolean shouldShutDown;

	// In the future, this will also be used to run the file server using Jython.
	// Jython will run the file server in a safe cross-platform Java environment, as
	// well as avoid the need to install Python.
	// (Java is more likely to be installed)

	public static void main(String... args) {
		
		//System.setProperty("user.dir", System.getProperty("user.dir") + "\\src");

		ServerConsole console = new ServerConsole();
		
		ProcessBuilder processBuilder = new ProcessBuilder("python", "-m", "file_server.__init__", "../test_directories/serv_dir");
		processBuilder.directory(new File("src"));
		
		processBuilder.redirectErrorStream(true);
		processBuilder.redirectOutput(Redirect.PIPE);
		
		console.print("Starting file server");

		// Start execution of the python file server
		Process pythonProcess;
		try {
			pythonProcess = processBuilder.start();
		} catch (IOException e) {
			console.print("Unable to start Python file-server.");
			console.print(e);
			return;
		}

		ProcessOutputReader inReader = new ProcessOutputReader(console, "STDIN", pythonProcess.getInputStream());
		ProcessOutputReader errReader = new ProcessOutputReader(console, "STDERR", pythonProcess.getErrorStream());

		inReader.start();
		errReader.start();
		
		shouldShutDown = false;

		while (!shouldShutDown) {
			try {
				Thread.sleep(500);
			} catch (InterruptedException e) {
			}
		}
		
		inReader.shutDown();
		errReader.shutDown();
		
		pythonProcess.destroyForcibly();

		int exit = pythonProcess.exitValue();
		console.print("Exited with code " + exit);

		console.close();

	}

	private static class ProcessOutputReader extends Thread {

		ServerConsole console;
		String name;
		BufferedReader in;

		private boolean shouldShutDown;

		ProcessOutputReader(ServerConsole console, String name, InputStream in) {
			this.console = console;
			this.name = name;
			this.in = new BufferedReader(new InputStreamReader(in));

			this.shouldShutDown = false;
		}
		
		void shutDown() {
			this.shouldShutDown = true;
			super.interrupt();
		}

		@Override
		public void run() {
			try {

				String line;

				// Read input until stream is done
				while (!shouldShutDown && (line = in.readLine()) != null) {
					console.print(line, false);
				}

			} catch (IOException e) {
				console.print(String.format("Error reading output from file server stream=%s", name));
				console.print(e);
			} finally {
				try {
					in.close();
				} catch (IOException e) {
					console.print(String.format("Failed to close output from file server stream=%s", name));
				}
			}

		}

	}

}