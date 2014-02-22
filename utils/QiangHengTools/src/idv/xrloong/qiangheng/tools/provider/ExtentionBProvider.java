package idv.xrloong.qiangheng.tools.provider;

import idv.xrloong.qiangheng.tools.util.Logger;
import android.content.ContentProvider;
import android.content.ContentValues;
import android.content.Context;
import android.content.UriMatcher;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteException;
import android.database.sqlite.SQLiteOpenHelper;
import android.net.Uri;
import android.text.TextUtils;

public class ExtentionBProvider extends ContentProvider {
	private static final String LOG_TAG = Logger.getLogTag(ExtentionBProvider.class);

	static final String AUTHORITY = "idv.xrloong.qiangheng.tools.DecomposingExtentionB";
	private static final UriMatcher sUriMatcher;

	private static final int CODE_CHARACTER = 1;
	private static final int CODE_CHARACTER_ID = 2;

	static {
		sUriMatcher = new UriMatcher(UriMatcher.NO_MATCH);
		sUriMatcher.addURI(AUTHORITY, "character/", CODE_CHARACTER);
		sUriMatcher.addURI(AUTHORITY, "character/#", CODE_CHARACTER_ID);
	}

	@Override
	public String getType(Uri uri) {
		return null;
	}

	@Override
	public Uri insert(Uri uri, ContentValues values) {
		return null;
	}

	@Override
	public int bulkInsert(Uri uri, ContentValues[] values) {
		Logger.d(LOG_TAG, "bulkInsert() +");

		String tableName = null;
        switch(sUriMatcher.match(uri)) {
    	case CODE_CHARACTER:
    		tableName = ExtentionBColumns.TABLE_NAME;
    		break;
    	case CODE_CHARACTER_ID:
    		Logger.w(LOG_TAG, "bulkInsert CODE_CHARACTER_ID is not supported");
    		break;
        }

        if(tableName == null) {
        	Logger.w(LOG_TAG, "bulkInser(): not avaiable tableName");
        	return 0;
        }

        SQLiteDatabase db = mOpenHelper.getWritableDatabase();
		int numInserted = 0;
		try {
			int numValues = values.length;
			db.beginTransaction();
			for (int i = 0; i < numValues; i++) {
Logger.e("AAAA", "XXXXXXXXXXXXXXXXXXXXXXXXXXX "+i +", "+values[i]);

				long rowId = db.insert(tableName, null, values[i]);
				db.yieldIfContendedSafely();
				if (rowId >= 0)
					numInserted++;
			}
			db.setTransactionSuccessful();
		} finally {
			db.endTransaction();
		}

		Logger.d(LOG_TAG, "bulkInsert() -");
		return numInserted;
	}

	@Override
	public Cursor query(Uri uri, String[] projection, String selection,
			String[] selectionArgs, String sortOrder) {
		Logger.i(LOG_TAG, "query() +");
		Logger.i(LOG_TAG, "query() uri: %s", uri);

		SQLiteDatabase db = mOpenHelper.getReadableDatabase();

		String tableName = null;
		String where = null;
        switch(sUriMatcher.match(uri)) {
    	case CODE_CHARACTER:
    		tableName = ExtentionBColumns.TABLE_NAME;
    		break;
    	case CODE_CHARACTER_ID:
    		tableName = ExtentionBColumns.TABLE_NAME;
            String codePoint = uri.getPathSegments().get(1);
            where = generateWhereClauseWithID(ExtentionBColumns.CODE_POINT, codePoint, selection);
    		break;
        }


        Cursor cursor = null;
        if(tableName != null) {
            cursor = db.query(tableName, projection, where, selectionArgs, null, null, sortOrder);
        }

        Logger.i(LOG_TAG, "query() -");
		return cursor;
	}

	private String generateWhereClause(String where) {
		return (!TextUtils.isEmpty(where) ? " AND (" + where + ")" : "");
	}

	private String generateWhereClauseWithID(String mainCondition, String id, String where) {
		return mainCondition + "=" + id + generateWhereClause(where);
	}

	@Override
	public int update(Uri uri, ContentValues values, String selection, String[] selectionArgs) {
		int numUpdated = 0;
		SQLiteDatabase db = null;
		try {
			db = mOpenHelper.getWritableDatabase();
		} catch (SQLiteException e) {
			Logger.e(LOG_TAG, "update() uri: " + uri.toString() + ", exception : " + e);
			return numUpdated;
		}

        String codePoint = uri.getPathSegments().get(1);
        String where = generateWhereClauseWithID(ExtentionBColumns.CODE_POINT, codePoint, selection);

		numUpdated = db.update(ExtentionBColumns.TABLE_NAME, values, where, selectionArgs);

		return 0;
	}

	@Override
	public int delete(Uri uri, String arg1, String[] arg2) {
		return 0;
	}

	private DatabaseHelper mOpenHelper = null;

	@Override
	public boolean onCreate() {
		mOpenHelper = new DatabaseHelper(getContext());
		return true;
	}

	private static final int DATABASE_VERSION = 1;

	private static class DatabaseHelper extends SQLiteOpenHelper {
        private static final String LOG_TAG = Logger.getLogTag(DatabaseHelper.class);
    	private static final String DATABASE_NAME = "DecomposeExtetionB.db";

    	private static String getDatabasePath(Context context) {
    		return context.getExternalFilesDir(null) + "/" + DATABASE_NAME;
    	}

    	public DatabaseHelper(Context context) {
                super(context, getDatabasePath(context), null, DATABASE_VERSION);
                Logger.i(LOG_TAG, "DatabaseHelper(): name: "+getDatabasePath(context)+", version: "+DATABASE_VERSION);
         }

        @Override
        public void onOpen(SQLiteDatabase db) {
                super.onOpen(db);

                if (!db.isReadOnly()) {
                		// This is to support cascade delete
                        db.execSQL("PRAGMA foreign_keys=ON;");
                }
        }

        @Override
        public void onCreate(SQLiteDatabase db) {
        	Logger.i(LOG_TAG, "onCreate() +");

			String sqlCommandToCreateTableStrokeType = "CREATE TABLE "
					+ ExtentionBColumns.TABLE_NAME
					+ " ("
					+ ExtentionBColumns._ID + " INTEGER PRIMARY KEY, "
					+ ExtentionBColumns.CODE_POINT + " INTEGER NOT NULL UNIQUE, "
					+ ExtentionBColumns.OPERATOR + " TEXT, "
					+ ExtentionBColumns.OPERAND_COUNT + " INTEGER NOT NULL, "
					+ ExtentionBColumns.OPERAND_1 + " TEXT, "
					+ ExtentionBColumns.OPERAND_2 + " TEXT, "
					+ ExtentionBColumns.OPERAND_3 + " TEXT, "
					+ ExtentionBColumns.OPERAND_4 + " TEXT "
					+ ");";
			Logger.i(LOG_TAG, "create table: stroke_type");
			db.execSQL(sqlCommandToCreateTableStrokeType);

			Logger.i(LOG_TAG, "onCreate() -");
		}

		@Override
		public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
			Logger.i(LOG_TAG, "onUpdate() +");
			Logger.i(LOG_TAG, "oldVersion: " + oldVersion + ", newVersion: " + newVersion);
			Logger.i(LOG_TAG, "onUpdate() -");
		}
    }
}
