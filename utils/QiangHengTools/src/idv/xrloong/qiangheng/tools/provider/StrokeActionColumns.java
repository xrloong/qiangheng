package idv.xrloong.qiangheng.tools.provider;

import android.net.Uri;
import android.provider.BaseColumns;

public class StrokeActionColumns implements BaseColumns {
	public static final String TABLE_NAME = "strokes";

	public static final String AUTHORITY = NamingStrokeProvider.AUTHORITY;
	public static final Uri CONTENT_URI = Uri.parse("content://" + AUTHORITY + "/descriptions");

	public static final String CHARACTER_NAME = "character_name";
	public static final String STROKE_NO = "stroke_no";
	public static final String STROKE_DESCRIPTION = "stroke_description";
	public static final String STROKE_NAME = "stroke_name";
}
