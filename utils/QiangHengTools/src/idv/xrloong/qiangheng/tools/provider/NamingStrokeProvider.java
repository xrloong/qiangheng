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

public class NamingStrokeProvider extends ContentProvider {
	private static final String LOG_TAG = Logger.getLogTag(NamingStrokeProvider.class);

	public static final String AUTHORITY = "idv.xrloong.qiangheng.tools.NamingStroke";

	private static final int DATABASE_VERSION = 1;

	private static final int CODE_STROKES= 1;
	private static final int CODE_STROKE_ID = 2;
    private static final UriMatcher sUriMatcher;
	static {
		sUriMatcher = new UriMatcher(UriMatcher.NO_MATCH);
		sUriMatcher.addURI(AUTHORITY, "descriptions/", CODE_STROKES);
		sUriMatcher.addURI(AUTHORITY, "descriptions/#", CODE_STROKE_ID);
	}

	private DatabaseHelper mOpenHelper = null;

	@Override
	public boolean onCreate() {
		mOpenHelper = new DatabaseHelper(getContext());
		return true;
	}

	@Override
	public String getType(Uri uri) {
		return null;
	}

	@Override
	public Cursor query(Uri uri, String[] projection, String selection, String[] selectionArgs, String sortOrder) {
		Logger.i(LOG_TAG, "query() +");
		Logger.i(LOG_TAG, "query() uri: " + uri);

		SQLiteDatabase db = mOpenHelper.getReadableDatabase();

		String tableName = StrokeActionColumns.TABLE_NAME;

        String where = null;
        int code = sUriMatcher.match(uri);
        switch(code) {
        	case CODE_STROKES:
        		break;
        	case CODE_STROKE_ID:
                String stroke = uri.getPathSegments().get(1);
                where = generateWhereClauseWithID(StrokeActionColumns._ID, stroke, selection);
        		break;
        }
        Cursor cursor = db.query(tableName, projection, where, selectionArgs, null, null, sortOrder);

        Logger.i(LOG_TAG, "query() -");
		return cursor;
	}

	@Override
	public Uri insert(Uri uri, ContentValues values) {
		SQLiteDatabase db = mOpenHelper.getWritableDatabase();
		long itemId = db.insert(StrokeActionColumns.TABLE_NAME, null, values);

		Uri.Builder builder = new Uri.Builder();
		builder.authority(AUTHORITY).appendPath(String.valueOf(itemId));
		Uri resultUri = builder.authority(AUTHORITY).appendPath(String.valueOf(itemId)).build();

		Logger.d(LOG_TAG, "insert(): %s", resultUri);
		return resultUri;
	}

	public int bulkInsert(Uri uri, ContentValues[] values) {
		Logger.i(LOG_TAG, "bulkInsert() +");
		SQLiteDatabase db = mOpenHelper.getWritableDatabase();
		int numInserted = 0;
		try {
			int numValues = values.length;
			db.beginTransaction();
			for (int i = 0; i < numValues; i++) {
				long rowId = db.insert(StrokeActionColumns.TABLE_NAME, null, values[i]);

				db.yieldIfContendedSafely();
				if (rowId >= 0)
					numInserted++;
			}
			db.setTransactionSuccessful();
		} finally {
			db.endTransaction();
		}

		return numInserted;
	}

	@Override
	public int delete(Uri arg0, String arg1, String[] arg2) {
		return 0;
	}

	@Override
	public int update(Uri uri, ContentValues values, String selection, String[] selectionArgs) {
		// TODO Auto-generated method stub
		int numUpdated = 0;
		SQLiteDatabase db = null;
		try {
			db = mOpenHelper.getWritableDatabase();
		} catch (SQLiteException e) {
			Logger.e(LOG_TAG, "update() uri: " + uri.toString() + ", exception : " + e);
			return numUpdated;
		}

        String strDataId = uri.getPathSegments().get(1);
//		int dataId = Integer.parseInt(strDataId);
		numUpdated = db.update(StrokeActionColumns.TABLE_NAME, values, generateWhereClauseWithID(StrokeActionColumns._ID, strDataId, selection), selectionArgs);

		return 0;
	}

	private String generateWhereClause(String where) {
		return (!TextUtils.isEmpty(where) ? " AND (" + where + ")" : "");
	}

	private String generateWhereClauseWithID(String mainCondition, String id, String where) {
		return mainCondition + "=" + id + generateWhereClause(where);
	}

	private static class DatabaseHelper extends SQLiteOpenHelper {
        private static final String LOG_TAG = Logger.getLogTag(DatabaseHelper.class);
    	private static final String DATABASE_NAME = "NamingStroke.db";

    	private static String getDatabasePath(Context context) {
//    		return DATABASE_NAME;
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

			String sqlCommandToCreateTableScene = "CREATE TABLE "
					+ StrokeActionColumns.TABLE_NAME
					+ " ("
					+ StrokeActionColumns._ID + " INTEGER PRIMARY KEY, "
					+ StrokeActionColumns.CHARACTER_NAME + " TEXT, "
					+ StrokeActionColumns.STROKE_NO + " INTEGER, "
					+ StrokeActionColumns.STROKE_DESCRIPTION + " TEXT, "
					+ StrokeActionColumns.STROKE_NAME + " TEXT "
					+ ");";

			Logger.i(LOG_TAG, "create table: strokes");
			db.execSQL(sqlCommandToCreateTableScene);

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
