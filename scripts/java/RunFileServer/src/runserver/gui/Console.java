package runserver.gui;

import java.awt.BorderLayout;
import java.util.function.Supplier;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JScrollBar;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.ScrollPaneConstants;

import runserver.process.ConsoleProcess;

@SuppressWarnings("serial")
public class Console extends JFrame {

	private Supplier<JPanel> createTopPanel;
	private Supplier<JPanel> createBottomPanel;

	private JTextArea textArea;
	private JScrollBar scrollBar;

	private ConsoleProcess process;

	public Console(String title) {
		super(title);

		super.setSize(625, 400);
		super.setResizable(false);
		super.setDefaultCloseOperation(DISPOSE_ON_CLOSE);
	}

	public void initialize() {
		initialize(null, null);
	}

	public void initialize(Supplier<JPanel> createTopPanel) {
		initialize(createTopPanel, null);
	}

	public void initialize(Supplier<JPanel> createTopPanel, Supplier<JPanel> createBottomPanel) {
		this.createTopPanel = createTopPanel;
		this.createBottomPanel = createBottomPanel;

		this.textArea = new JTextArea();
		this.textArea.setEditable(false);
		this.textArea.setLineWrap(true);
		this.textArea.setWrapStyleWord(true);

		if (createTopPanel != null) {
			super.getContentPane().add(createTopPanel.get(), BorderLayout.NORTH);
		}
		if (createBottomPanel != null) {
			super.getContentPane().add(createBottomPanel.get(), BorderLayout.SOUTH);
		}

		// Dimension d = new Dimension(150, 5);
		// Filler box = new Filler(d, d, d);
		// buttonPanel.add(box);

		JScrollPane scrollPane = new JScrollPane(textArea);
		scrollPane.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
		this.scrollBar = scrollPane.getVerticalScrollBar();
		super.getContentPane().add(scrollPane, BorderLayout.CENTER);

		super.setVisible(true);
	}

	public void setProcess(ConsoleProcess process) {
		this.process = process;
	}
	
	public ConsoleProcess getProcess() {
		return process;
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
	
	public Console clone() {
		return clone(this.getTitle());
	}
	
	public Console clone(String title) {
		Console console = new Console(title);
		console.initialize(createTopPanel, createBottomPanel);
		return console;
	}

	public void close() {
		super.setVisible(false);
		super.dispose();
	}

	@Override
	public void dispose() {
		if (process != null) {
			process.shutdown(true);
		}
	}

}
