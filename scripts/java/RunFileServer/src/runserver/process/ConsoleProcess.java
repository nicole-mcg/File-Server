package runserver.process;

import java.io.IOException;

import javax.swing.JOptionPane;

import runserver.gui.Console;

public class ConsoleProcess extends Thread {
	
	private String name;
	private Console console;
	
	private ProcessBuilder[] processBuilders;
	
	private boolean shouldShutDown;
	private boolean shouldRestart;
	private boolean skipPopup;
	
	public ConsoleProcess(String name, ProcessBuilder... processBuilders) {
		this.name = name;
		this.processBuilders = processBuilders;
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
		console = new Console(name, this);
		
		for (int i = 0; i < processBuilders.length; i++) {
			runProcess(i);
		}
		
		if (!skipPopup) {
			JOptionPane.showMessageDialog(console, "Press OK to exit.", "Alert", JOptionPane.INFORMATION_MESSAGE);
		}
		
		console.close();
		
		if (shouldRestart) {
			runProcess();
		}
	}

	private void runProcess(int index) {
		if (index < 0 || index > processBuilders.length) {
			return;
		}
		
		ProcessBuilder processBuilder = processBuilders[index];
		
		processBuilder.redirectErrorStream(true);
		
		Process process;
		try {
			process = processBuilder.start();
		} catch (IOException e) {
			console.print("Unable to start process.");
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
		
	}
	
	@Override
	public void run() {
		runProcess();
	}
	
}
