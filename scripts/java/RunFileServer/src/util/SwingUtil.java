package util;

import java.awt.Component;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.function.Consumer;

import javax.swing.JButton;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;

import runserver.gui.Console;

public class SwingUtil {
	
	/**
	 * Adds a button with the specified text to the panel
	 * Also adds the console as an action listener
	 * @param text The text (and action command) for the button
	 * @param panel The panel to add the button to
	 * @param console The console this panel will be attached to, used as an actionListener
	 */
	public static void addButton(String text, JPanel panel, Consumer<Console> onButtonClicked) {
		JButton button = new JButton(text);
		button.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				Console console = (Console) SwingUtilities.getRoot((Component) e.getSource());
				onButtonClicked.accept(console);
			}
		});
		panel.add(button);
	}

}
