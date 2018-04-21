package runserver;

import java.awt.Desktop;
import java.awt.FlowLayout;
import java.io.File;
import java.net.URL;
import java.util.ArrayList;
import java.util.function.Supplier;

import javax.swing.JPanel;

import runserver.gui.Console;
import runserver.process.ConsoleProcess;

import util.SwingUtil;
import util.SystemUtil;
import util.SystemUtil.OperatingSystem;
import util.Constants;

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
		
		Console console = new Console("File Server");
		
		ProcessBuilder processBuilder = new ProcessBuilder("python", "-m", "file_server.__init__",
				"../test_directories/serv_dir");
		processBuilder.directory(new File("src"));
		
		ConsoleProcess process = new ConsoleProcess(console, processBuilder);
		
		Supplier<JPanel> createTopPanel = () -> {
		
			JPanel buttonPanel = new JPanel();
			buttonPanel.setLayout(new FlowLayout());
			
			SwingUtil.addButton("Open Web UI", buttonPanel, (Console c) -> {
				try {
			        Desktop.getDesktop().browse(new URL("http://127.0.0.1:8080").toURI());
			    } catch (Exception ex) {
			        ex.printStackTrace();
			    }
			});
			
			SwingUtil.addButton("Start Client", buttonPanel, (Console c) -> {
				ProcessBuilder pB = new ProcessBuilder("python", "-m", "file_server.__init__", String.format("..%ctest_directories%cclient_dir", Constants.sepArr(2)), "localhost", "test", "test");
				pB.directory(new File("src"));
				
				new ConsoleProcess(c.clone("File Client"), pB).start();
			});
			
			SwingUtil.addButton("Run Tests", buttonPanel, (Console c) -> {
				
				File rootDir = new File(System.getProperty("user.dir"));
				if (rootDir.getName() == "src") {
					rootDir = rootDir.getParentFile();
				}
				
				ProcessBuilder pyProcessBuilder, nodeProcessBuilder, cleanProcessBuilder;
				
				pyProcessBuilder = new ProcessBuilder("python", "-m", "pytest", "-x");
				pyProcessBuilder.directory(new File("src"));
				
				nodeProcessBuilder = new ProcessBuilder("npm", "test");
				nodeProcessBuilder.directory(new File("web"));
				
				String runTestsExt = SystemUtil.getOS() == OperatingSystem.WINDOWS ? ".bat" : ".sh";
				
				cleanProcessBuilder = new ProcessBuilder(String.format("cleanup_tests%s", runTestsExt));
				cleanProcessBuilder.directory(new File(String.format("%s%cscripts", rootDir.getAbsolutePath(), Constants.P_SEP)));
				
				new ConsoleProcess(c.clone("Running Tests"), pyProcessBuilder, nodeProcessBuilder, cleanProcessBuilder).start();
			});
			
			SwingUtil.addButton("Run Webpack", buttonPanel, (Console c) -> {
				ProcessBuilder pB = new ProcessBuilder(String.format(".%cnode_modules%c.bin%cwebpack", Constants.sepArr(3)),  "--watch");
				
				File currDir = new File(System.getProperty("user.dir"));
				if (currDir.getName() == "src") {
					currDir = currDir.getParentFile();
				}
				
				pB.directory(new File(String.format("%s%cweb", currDir.getAbsolutePath(), Constants.P_SEP)));
				new ConsoleProcess(c.clone("Webpack"), pB).start();
			});
			
			SwingUtil.addButton("Restart", buttonPanel, (Console c) -> {
				c.print("Restarting console");
				c.getProcess().restart();
			});
			
			SwingUtil.addButton("Shutdown", buttonPanel, (Console c) -> c.getProcess().shutdown());
			
			return buttonPanel;
		
		};
		
		console.initialize(createTopPanel);
		
		process.runProcess();
		
		console.close();
		
	}

}