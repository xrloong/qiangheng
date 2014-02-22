package idv.xrloong.qiangheng.tools.provider;

import android.net.Uri;
import android.provider.BaseColumns;

public class CharacterExtraColumns implements BaseColumns {
	public static final String AUTHORITY = NamingStrokeProvider.AUTHORITY;
	public static final Uri CONTENT_URI = Uri.parse("content://" + AUTHORITY + "/descriptions");

	public static final String CHAR_ID = "char_id";
	public static final String EXTRA_ID = "extra_id";
}
