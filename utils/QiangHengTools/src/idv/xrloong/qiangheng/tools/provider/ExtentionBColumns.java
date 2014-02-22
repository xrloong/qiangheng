package idv.xrloong.qiangheng.tools.provider;

import android.net.Uri;
import android.provider.BaseColumns;

public class ExtentionBColumns implements BaseColumns {
	public static final String TABLE_NAME = "character";

	public static final String AUTHORITY = ExtentionBProvider.AUTHORITY;
	public static final Uri CONTENT_URI = Uri.parse("content://" + AUTHORITY + "/character");

	public static final String CODE_POINT = "code_point";
	public static final String OPERATOR = "operator";
	public static final String OPERAND_COUNT = "operand_count";
	public static final String OPERAND_1 = "operand_1";
	public static final String OPERAND_2 = "operand_2";
	public static final String OPERAND_3 = "operand_3";
	public static final String OPERAND_4 = "operand_4";
}
