package org.cmcg.runserver;

import java.io.IOException;
import java.io.InputStream;
import java.nio.ByteBuffer;
import java.nio.channels.Channels;
import java.nio.channels.ReadableByteChannel;

public class ProcessOutputReader extends Thread {

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

			ByteBuffer buff = ByteBuffer.allocate(1);
			
			// Read input until stream is done
			while (!shouldShutDown && in.isOpen()) {

				buff.clear();

				in.read(buff);

				buff.flip();

				while (!shouldShutDown && buff.hasRemaining()) {
					console.print((char) buff.get());
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
