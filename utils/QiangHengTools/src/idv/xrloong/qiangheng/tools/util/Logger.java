package idv.xrloong.qiangheng.tools.util;

import android.util.Log;

public class Logger {
//	private static final String LOG_TAG = getLogTag(Logger.class);
	private static final String LOG_PACKAGE = "QHTool";

	public static final String getLogTag(Class<?> clz) {
		return LOG_PACKAGE + clz.getSimpleName();
	}

	public static void e(String LogTag, String format, Object...  objects) {
		Log.e(LogTag, String.format(format, objects));
	}

	public static void e(String LogTag, String format, Throwable throwable, Object...  objects) {
		Log.e(LogTag, String.format(format, objects), throwable);
	}

	public static void w(String LogTag, String format, Object...  objects) {
		Log.e(LogTag, String.format(format, objects));
	}

	public static void w(String LogTag, String format, Throwable throwable, Object...  objects) {
		Log.e(LogTag, String.format(format, objects), throwable);
	}

	public static void i(String LogTag, String format, Object...  objects) {
		Log.v(LogTag, String.format(format, objects));
	}

	public static void i(String LogTag, String format, Throwable throwable, Object...  objects) {
		Log.e(LogTag, String.format(format, objects), throwable);
	}

	public static void v(String LogTag, String format, Object...  objects) {
		Log.v(LogTag, String.format(format, objects));
	}

	public static void v(String LogTag, String format, Throwable throwable, Object...  objects) {
		Log.e(LogTag, String.format(format, objects), throwable);
	}

	public static void d(String LogTag, String format, Object...  objects) {
		Log.d(LogTag, String.format(format, objects));
	}

	public static void d(String LogTag, String format, Throwable throwable, Object...  objects) {
		Log.e(LogTag, String.format(format, objects), throwable);
	}
}
