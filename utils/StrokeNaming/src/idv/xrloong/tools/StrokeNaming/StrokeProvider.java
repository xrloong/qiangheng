package idv.xrloong.tools.StrokeNaming;

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
import android.util.Log;

public class StrokeProvider extends ContentProvider {
	public static final String AUTHORITY = "idv.xrloong.tools.StrokeNaming";

	private static final String TAG = "[StrokeProvider]";

	private static final String DATABASE_NAME = "strokes.db";
	private static final String TABLE_NAME_STROKES = "strokes";

	private static final int DATABASE_VERSION = 1;
    private DatabaseHelper mOpenHelper = null;

    private static final UriMatcher sUriMatcher;
	static {
		sUriMatcher = new UriMatcher(UriMatcher.NO_MATCH);
		/*
		sUriMatcher.addURI(StrokeColumns.AUTHORITY, "scene", CASE_SCENE);
		sUriMatcher.addURI(SceneProvider.AUTHORITY, "scene/#", CASE_SCENE_ID);
		sUriMatcher.addURI(FavoriteColumns.AUTHORITY, "favorite", CASE_FAVORITE);
		sUriMatcher.addURI(FavoriteColumns.AUTHORITY, "favorite/#",	CASE_FAVORITE_ID);
		sUriMatcher.addURI(SceneProviderStatusColumns.AUTHORITY, "status", CASE_STATUS);
		sUriMatcher.addURI(CurrentSceneColumns.AUTHORITY, "current_scene", CASE_CURRENT_SCENE);
		*/
	}

	@Override
	public int delete(Uri arg0, String arg1, String[] arg2) {
		// TODO Auto-generated method stub
		return 0;
	}

	@Override
	public String getType(Uri uri) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Uri insert(Uri uri, ContentValues values) {
		// TODO Auto-generated method stub

		SQLiteDatabase db = mOpenHelper.getWritableDatabase();
		long itemId = db.insert(TABLE_NAME_STROKES, null, values);

		return null;
	}

	public int bulkInsert(Uri uri, ContentValues[] values) {
		Log.i(TAG, "bulkInsert() +");
		SQLiteDatabase db = mOpenHelper.getWritableDatabase();
		int numInserted = 0;
		try {
			int numValues = values.length;
			db.beginTransaction();
			for (int i = 0; i < numValues; i++) {
				long rowId = db.insert(TABLE_NAME_STROKES, null, values[i]);

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
	public boolean onCreate() {
		// TODO Auto-generated method stub
		mOpenHelper = new DatabaseHelper(getContext());
		return true;
	}

	@Override
	public Cursor query(Uri uri, String[] projection, String selection,
			String[] selectionArgs, String sortOrder) {
		// TODO Auto-generated method stub
		Log.i(TAG, "query() +");
		Log.i(TAG, "query() uri: " + uri);

		SQLiteDatabase db = mOpenHelper.getReadableDatabase();

		String tableName = TABLE_NAME_STROKES;
        String sceneId = uri.getPathSegments().get(1);

        String where = generateWhereClauseWithID(StrokeColumns.ID, sceneId, selection);
        Cursor cursor = db.query(tableName, projection, where, selectionArgs, null, null, sortOrder);
		Log.i(TAG, "query() -");
		return cursor;
	}

	@Override
	public int update(Uri uri, ContentValues values, String selection, String[] selectionArgs) {
		// TODO Auto-generated method stub
		int numUpdated = 0;
		SQLiteDatabase db = null;
		try {
			db = mOpenHelper.getWritableDatabase();
		} catch (SQLiteException e) {
			Log.e(TAG, "update() uri: " + uri.toString() + ", exception : " + e);
			return numUpdated;
		}

        String strDataId = uri.getPathSegments().get(1);
		int dataId = Integer.parseInt(strDataId);
		numUpdated = db.update(TABLE_NAME_STROKES, values, generateWhereClauseWithID(StrokeColumns.ID, strDataId, selection), selectionArgs);

		return 0;
	}

	private String generateWhereClause(String where) {
		return (!TextUtils.isEmpty(where) ? " AND (" + where + ")" : "");
	}

	private String generateWhereClauseWithID(String mainCondition, String id,
			String where) {
		return mainCondition + "=" + id + generateWhereClause(where);
	}

	private static class DatabaseHelper extends SQLiteOpenHelper {
        private static final String TAG = "StrokeProvider.DatabaseHelper";
        public DatabaseHelper(Context context) {
                super(context, DATABASE_NAME, null, DATABASE_VERSION);
                Log.i(TAG, "DatabaseHelper(): name: "+DATABASE_NAME+", version: "+DATABASE_VERSION);
         }

        @Override
        public void onOpen(SQLiteDatabase db) {
                super.onOpen(db);

                // This is to support cascad delete
                if (!db.isReadOnly()) {
                        db.execSQL("PRAGMA foreign_keys=ON;");
                }
        }

        @Override
        public void onCreate(SQLiteDatabase db) {
        	Log.i(TAG, "onCreate() +");

			String sqlCommandToCreateTableScene = "CREATE TABLE "
					+ TABLE_NAME_STROKES
					+ " ("
					+ StrokeColumns.ID + " INTEGER PRIMARY KEY, "
					+ StrokeColumns.CHARACTER_NAME + " TEXT, "
					+ StrokeColumns.STROKE_NO + " INTEGER, "
					+ StrokeColumns.STROKE_DESCRIPTION + " TEXT, "
					+ StrokeColumns.STROKE_NAME + " TEXT "
					+ ");";

			Log.i(TAG, "create table: strokes");
			db.execSQL(sqlCommandToCreateTableScene);

			Log.i(TAG, "onCreate() -");
		}

		@Override
		public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
			// TODO Auto-generated method stub
            Log.i(TAG, "onUpdate() +");
            Log.i(TAG, "oldVersion: " + oldVersion + ", newVersion: " + newVersion);
            Log.i(TAG, "onUpdate() -");
		}
    }
}
