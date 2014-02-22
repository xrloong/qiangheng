package idv.xrloong.qiangheng.tools.provider;

import android.net.Uri;
import android.provider.BaseColumns;

public class StrokeColumns implements BaseColumns {
	public static final String TABLE_NAME = "stroke";

	public static final String AUTHORITY = FindCommonComponentProvider.AUTHORITY;
	public static final Uri CONTENT_URI = Uri.parse("content://" + AUTHORITY + "/stroke");

	public static final String DB_NAME = "db_name";
	public static final String STROKE_NAME = "stroke_name";
	public static final String RANGE = "range";
	public static final String IS_NORMAL = "is_normal";
	public static final String STROKE_TYPE_ID = "stroke_type_id";
	public static final String EXPRESSION = "expression";
}
