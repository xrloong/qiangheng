package idv.xrloong.qiangheng.tools.provider;

import android.net.Uri;
import android.provider.BaseColumns;

public class CharacterAddendumColumns implements BaseColumns {
	public static final String TABLE_NAME = "character_addendum";

	public static final String AUTHORITY = FindCommonComponentProvider.AUTHORITY;
	public static final Uri CONTENT_URI = Uri.parse("content://" + AUTHORITY + "/character_addendum");

	public static final String REFERENCE_CHARACTER_ID = "character_id";
	public static final String REFERENCE_ADDENDUM_ID = "addendum_id";
}
