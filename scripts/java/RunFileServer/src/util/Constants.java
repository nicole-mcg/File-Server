package util;

import java.io.File;
import java.util.Arrays;

public class Constants {

	public final static char P_SEP = File.separatorChar;
	
	public static Object[] sepArr(int numTimes) {
		Character[] s = new Character[numTimes];
		Arrays.fill(s, P_SEP);
		return (Object[]) s;
	}
	
}
