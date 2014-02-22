package idv.xrloong.qiangheng.tools.provider;

import android.net.Uri;
import android.provider.BaseColumns;

public class StrokeGroupContentColumns implements BaseColumns {
	public static final String TABLE_NAME = "stroke_group_content";

	public static final String AUTHORITY = FindCommonComponentProvider.AUTHORITY;
	public static final Uri CONTENT_URI = Uri.parse("content://" + AUTHORITY + "/stroke_group");

	public static final String REFERENCE_GROUP_ID = "group_id";
	public static final String STROKE_ORDER = "stroke_order";
	public static final String REFERENCE_STROKE_ID = "stroke_id";
}
