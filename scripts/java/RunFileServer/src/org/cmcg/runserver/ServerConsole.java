package org.cmcg.runserver;

import javax.swing.JFrame;
import javax.swing.JScrollBar;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.ScrollPaneConstants;

@SuppressWarnings("serial")
public class ServerConsole extends JFrame {
	
	JTextArea textArea;
	JScrollBar scrollBar;

	public ServerConsole() {
		super("File Server");
		
		super.setSize(600, 400);
		
		this.textArea = new JTextArea(5, 20);
		this.textArea.setEditable(false);
		this.textArea.setLineWrap(true);
		this.textArea.setWrapStyleWord(true);
		
		JScrollPane scrollPane = new JScrollPane(textArea);
		scrollPane.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
		
		this.scrollBar = scrollPane.getVerticalScrollBar();
		
		super.add(scrollPane);
		
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
	
	@Override
	public void dispose() {
		RunServer.shouldShutDown = true;
	}
	
}
