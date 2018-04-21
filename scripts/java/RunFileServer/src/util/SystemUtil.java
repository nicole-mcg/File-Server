package util;

public class SystemUtil {
	
	public static enum OperatingSystem {
		WINDOWS,
		LINUX,
		MAC,
		SOLARIS,
		UNKNOWN
	}

	public static OperatingSystem getOS() {
		
		String os = System.getProperty("os.name").toLowerCase();
		
		if (os.indexOf("win") >= 0) {
			return OperatingSystem.WINDOWS;
		}
		
		if (os.indexOf("mac") >= 0) {
			return OperatingSystem.MAC;
		}
		
		if (os.indexOf("sunos") >= 0) {
			return OperatingSystem.SOLARIS;
		}
		
		if (os.indexOf("nix") >= 0 || os.indexOf("nux") >= 0 || os.indexOf("aix") > 0 ) {
			return OperatingSystem.LINUX;
		}
		
		return OperatingSystem.UNKNOWN;
	}
	
}
