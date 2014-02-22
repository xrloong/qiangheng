package idv.xrloong.qiangheng.tools.provider;

import android.net.Uri;
import android.provider.BaseColumns;

public class StrokeTypeColumns implements BaseColumns {
	public static final String TABLE_NAME = "stroke_type";

	public static final String AUTHORITY = FindCommonComponentProvider.AUTHORITY;
	public static final Uri CONTENT_URI = Uri.parse("content://" + AUTHORITY + "/type");

	public static final String TYPE_NAME = "type_name";
}
