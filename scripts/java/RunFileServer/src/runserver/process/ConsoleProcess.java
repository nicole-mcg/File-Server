package runserver.process;

import java.io.IOException;

import javax.swing.JOptionPane;

import runserver.gui.Console;

/**
 * 
 * @author c-mcg
 *
 */
public class ConsoleProcess extends Thread {
	
	/**
	 * The console this process should output to
	 */
	private Console console;
	
	/**
	 * ProcessBuilders used to create the processes
	 */
	private ProcessBuilder[] processBuilders;
	
	boolean closeConsoleWhenDone;
	
	/**
	 * When true, the process will shut down when possible
	 */
	private boolean shouldShutDown;
	
	/**
	 * When true, the process will restart when shut down
	 */
	private boolean shouldRestart;
	
	/**
	 * When true, the "Click okay to exit" popup won't show
	 * Currently only used for `shouldRestart`
	 */
	private boolean skipPopup;
	
	public ConsoleProcess(Console console, ProcessBuilder... processBuilders) {
		this(console, true, processBuilders);
	}
	
	public ConsoleProcess(Console console, boolean closeConsoleWhenDone, ProcessBuilder... processBuilders) {
		this.console = console;
		this.processBuilders = processBuilders;
		
		this.closeConsoleWhenDone = closeConsoleWhenDone;
		
		if (console != null) {
			console.setProcess(this);
		}
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
		restart(null);
	}
	
	public void restart(Console newConsole) {
		
		if (newConsole != null) {
			this.console = newConsole;
			newConsole.setProcess(this);
		}
		
		this.shouldRestart = true;
		this.shouldShutDown = true;
		this.skipPopup = true;
	}
	
	public void runProcess() {
		
		for (int i = 0; i < processBuilders.length; i++) {
			runProcess(i);
		}
		
		if (!skipPopup) {
			JOptionPane.showMessageDialog(console, "Press OK to exit.", "Alert", JOptionPane.INFORMATION_MESSAGE);
		}
		
		if (shouldRestart) {
			runProcess();
			return;
		}
		
		if (closeConsoleWhenDone) {
			console.close();
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
