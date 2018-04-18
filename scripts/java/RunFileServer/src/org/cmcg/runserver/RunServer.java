package org.cmcg.runserver;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.lang.ProcessBuilder.Redirect;
import java.nio.ByteBuffer;
import java.nio.channels.Channels;
import java.nio.channels.ReadableByteChannel;

import javax.swing.JDialog;
import javax.swing.JOptionPane;

/**
 * A simple java program to start the file server // This is used to create
 * cross-platform runnable commands in the root directory
 * 
 * @author Connor
 *
 */
public class RunServer {

	public static boolean shouldShutDown;
	public static Process pythonProcess;

	// In the future, this will also be used to run the file server using Jython.
	// Jython will run the file server in a safe cross-platform Java environment, as
	// well as avoid the need to install Python.
	// (Java is more likely to be installed)

	public static void main(String... args) {

		ServerConsole console = new ServerConsole();

		System.setProperty("user.dir", System.getProperty("user.dir") + "\\src");

		ProcessBuilder processBuilder = new ProcessBuilder("python", "-m", "file_server.__init__",
				"../test_directories/serv_dir");

		processBuilder.redirectErrorStream(false);
		processBuilder.directory(new File("src"));

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

		while (!shouldShutDown && pythonProcess.isAlive()) {
			try {
				Thread.sleep(500);
			} catch (InterruptedException e) {
			}
		}

		console.print("Shutting down.");

		errReader.shutDown();
		inReader.shutDown();

		pythonProcess.destroyForcibly();

		JOptionPane.showMessageDialog(console.getContentPane(), "Press OK to continue.", "Alert", JOptionPane.INFORMATION_MESSAGE);
		console.close();

	}

	private static class ProcessOutputReader extends Thread {

		ServerConsole console;
		String name;
		ReadableByteChannel in;

		private boolean shouldShutDown;

		ProcessOutputReader(ServerConsole console, String name, InputStream in) {
			this.console = console;
			this.name = name;
			this.in = Channels.newChannel(in);

			this.shouldShutDown = false;
		}

		void shutDown() {
			this.shouldShutDown = true;
		}

		@Override
		public void run() {
			try {

				// Read input until stream is done
				while (!shouldShutDown && in.isOpen()) {

					ByteBuffer buff = ByteBuffer.allocate(1);
					buff.clear();

					in.read(buff);

					buff.flip();

					while (!shouldShutDown && buff.hasRemaining()) {
						console.print(Character.toString((char) buff.get()), false);
					}

				}

			} catch (IOException e) {

				console.print(String.format("Error reading output from file server stream=%s", name));
				console.print(e);

			} finally {

				try {
					this.in.close();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}

			}

		}

	}

}