package idv.xrloong.tools.StrokeNaming;

import android.net.Uri;
import android.provider.BaseColumns;

public class StrokeColumns implements BaseColumns {
	public static final String AUTHORITY = StrokeProvider.AUTHORITY;
	public static final Uri CONTENT_URI = Uri.parse("content://" + AUTHORITY + "/descriptions");

	public static final String ID = "_id";
	public static final String CHARACTER_NAME = "character_name";
	public static final String STROKE_NO = "stroke_no";
	public static final String STROKE_DESCRIPTION = "stroke_description";
	public static final String STROKE_NAME = "stroke_name";
}
