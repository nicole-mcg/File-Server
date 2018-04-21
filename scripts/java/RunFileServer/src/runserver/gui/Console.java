package runserver.gui;

import java.awt.BorderLayout;
import java.awt.Desktop;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.net.URL;
import java.util.Arrays;
import java.util.HashMap;
import java.util.function.Function;
import java.util.function.Predicate;

import javax.swing.Box.Filler;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JScrollBar;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.ScrollPaneConstants;

import runserver.Main;
import runserver.process.ConsoleProcess;

@SuppressWarnings("serial")
public class Console extends JFrame implements ActionListener {
	
	public final static char P_SEP = File.separatorChar;
	
	public static Object[] sepArr(int numTimes) {
		Character[] s = new Character[numTimes];
		Arrays.fill(s, P_SEP);
		return (Object[]) s;
	}
	
	private boolean isMainConsole;
	private ConsoleProcess process;

	private HashMap<String, Runnable> buttonHandlers;
	private JPanel buttonPanel;
	
	private JTextArea textArea;
	private JScrollBar scrollBar;
	
	public Console(String title, ConsoleProcess process) {
		this(title, process, false);
	}

	public Console(String title, ConsoleProcess process, boolean isMainConsole) {
		super(title);
		
		this.process = process;
		this.isMainConsole = isMainConsole;
		
		this.buttonHandlers = new HashMap<String, Runnable>();

		super.setSize(625, 400);
		super.setResizable(false);

		this.textArea = new JTextArea();
		this.textArea.setEditable(false);
		this.textArea.setLineWrap(true);
		this.textArea.setWrapStyleWord(true);

		buttonPanel = new JPanel();
		buttonPanel.setLayout(new FlowLayout());
		super.getContentPane().add(buttonPanel, BorderLayout.NORTH);
		
		addButton("Open Web UI", () -> {
			try {
		        Desktop.getDesktop().browse(new URL("http://127.0.0.1:8080").toURI());
		    } catch (Exception ex) {
		        ex.printStackTrace();
		    }
		}, buttonPanel);
		
		addButton("Start Client", () -> {
			ProcessBuilder processBuilder = new ProcessBuilder("python", "-m", "file_server.__init__", String.format("..%ctest_directories%cclient_dir", sepArr(2)), "localhost", "test", "test");
			processBuilder.directory(new File("src"));
			
			new ConsoleProcess("File Client", processBuilder).start();
		}, buttonPanel);
		
		addButton("Run Tests", () -> {
			
			File rootDir = new File(System.getProperty("user.dir"));
			if (rootDir.getName() == "src") {
				rootDir = rootDir.getParentFile();
			}
			
			ProcessBuilder pyProcessBuilder, nodeProcessBuilder, cleanProcessBuilder;
			
			pyProcessBuilder = new ProcessBuilder("python", "-m", "pytest", "-x");
			pyProcessBuilder.directory(new File("src"));
			
			nodeProcessBuilder = new ProcessBuilder("npm", "test");
			nodeProcessBuilder.directory(new File("web"));
			
			cleanProcessBuilder = new ProcessBuilder("cleanup_tests");
			cleanProcessBuilder.directory(new File(String.format("%s%cscripts", rootDir.getAbsolutePath(), P_SEP)));
			
			new ConsoleProcess("Running tests", pyProcessBuilder, nodeProcessBuilder, cleanProcessBuilder).start();
		}, buttonPanel);
		
		addButton("Run Webpack", () -> {
			ProcessBuilder processBuilder = new ProcessBuilder(String.format(".%cnode_modules%c.bin%cwebpack", sepArr(3)),  "--watch");
			
			File currDir = new File(System.getProperty("user.dir"));
			if (currDir.getName() == "src") {
				currDir = currDir.getParentFile();
			}
			
			processBuilder.directory(new File(String.format("%s%cweb", currDir.getAbsolutePath(), P_SEP)));
			new ConsoleProcess("Webpack", processBuilder).start();
		}, buttonPanel);
		
		addButton("Restart", () -> {
			print("Restarting console");
			process.restart();
		}, buttonPanel);
		
		addButton("Shutdown", () -> process.shutdown(), buttonPanel);
		
		//Dimension d = new Dimension(150, 5);
		//Filler box = new Filler(d, d, d);
		//buttonPanel.add(box);

		JScrollPane scrollPane = new JScrollPane(textArea);
		scrollPane.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
		this.scrollBar = scrollPane.getVerticalScrollBar();
		super.getContentPane().add(scrollPane, BorderLayout.CENTER);

		super.setDefaultCloseOperation(DISPOSE_ON_CLOSE);
		super.setVisible(true);
	}

	public void print(char c) {
		print(Character.toString(c), false);
	}

	public void print(int i) {
		print(Integer.toString(i));
	}

	public void print(Object object) {
		print(object.toString());
	}

	public void print(String message) {
		print(message, true);
	}

	public void print(String message, boolean newLine) {
		System.out.print(message + (newLine ? "\n" : ""));
		this.textArea.append(message + (newLine ? "\n" : ""));
		this.textArea.repaint();
		scrollBar.setValue(scrollBar.getMaximum());
	}

	public void close() {
		super.setVisible(false);
		super.dispose();
	}
	
	private void addButton(String text, Runnable onButtonClicked, JPanel panel) {
		
		JButton button = new JButton(text);
		button.addActionListener(this);
		panel.add(button);
		
		buttonHandlers.put(text, onButtonClicked);
	}

	@Override
	public void dispose() {
		if (isMainConsole) {
			Main.fileServerProcess.shutdown(true);
		} else {
			process.shutdown(true);
		}
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		String command = e.getActionCommand();
		
		if (buttonHandlers.containsKey(command)) {
			buttonHandlers.get(command).run();
		}
	}

}
