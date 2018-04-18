package runserver.process;

import java.io.IOException;

import javax.swing.JOptionPane;

import runserver.Console;

public class ConsoleProcess extends Thread {
	
	private String name;
	private ProcessBuilder processBuilder;
	
	private boolean shouldShutDown;
	private boolean shouldRestart;
	private boolean skipPopup;
	
	public ConsoleProcess(String name, ProcessBuilder processBuilder) {
		this.name = name;
		this.processBuilder = processBuilder;
	}
	
	public void shutdown() {
		shutdown(false);
	}
	
	public void shutdown(boolean skipPopup) {
		this.shouldRestart = false;
		this.shouldShutDown = true;
		this.skipPopup = skipPopup;
	}
	
	public void restart() {
		this.shouldRestart = true;
		this.shouldShutDown = true;
		this.skipPopup = true;
	}

	public void runProcess() {
		Console console = new Console(name, this);
		
		processBuilder.redirectErrorStream(false);
		
		Process process;
		try {
			process = processBuilder.start();
		} catch (IOException e) {
			console.print("Unable to start Python file-server.");
			console.print(e);
			return;
		}
		
		ProcessOutputReader inReader = new ProcessOutputReader(console, "STDIN", process.getInputStream());
		ProcessOutputReader errReader = new ProcessOutputReader(console, "STDERR", process.getErrorStream());

		inReader.start();
		errReader.start();

		shouldShutDown = false;
		shouldRestart = false;
		skipPopup = false;

		while (!shouldShutDown && process.isAlive()) {
			try {
				Thread.sleep(500);
			} catch (InterruptedException e) {
			}
		}
		
		if (!shouldRestart) {
			console.print("Shutting down...");
		}

		errReader.shutDown();
		inReader.shutDown();

		process.destroyForcibly();
		
		if (!skipPopup) {
			JOptionPane.showMessageDialog(console, "Press OK to exit.", "Alert", JOptionPane.INFORMATION_MESSAGE);
		}
		
		console.close();
		
		if (shouldRestart) {
			runProcess();
		}
	}
	
	@Override
	public void run() {
		runProcess();
	}
	
}
