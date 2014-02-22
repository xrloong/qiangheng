package idv.xrloong.qiangheng.tools.provider;

import android.net.Uri;
import android.provider.BaseColumns;

public class ExtrasColumns implements BaseColumns {
	public static final String AUTHORITY = NamingStrokeProvider.AUTHORITY;
	public static final Uri CONTENT_URI = Uri.parse("content://" + AUTHORITY + "/descriptions");

	public static final String NAME = "name";
	public static final String RANGE = "range";
}
