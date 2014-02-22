package idv.xrloong.qiangheng.tools.provider;

import android.net.Uri;
import android.provider.BaseColumns;

public class CharacterColumns implements BaseColumns {
	public static final String TABLE_NAME = "character";

	public static final String AUTHORITY = FindCommonComponentProvider.AUTHORITY;
	public static final Uri CONTENT_URI = Uri.parse("content://" + AUTHORITY + "/character");

	public static final String NAME = "name";
	public static final String COMMENT = "comment";
	public static final String GROUPING_ID = "grouping_id";
}
