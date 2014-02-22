package idv.xrloong.qiangheng.tools.provider;

import idv.xrloong.qiangheng.tools.util.Logger;
import android.content.ContentProvider;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.Context;
import android.content.UriMatcher;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.net.Uri;
import android.text.TextUtils;

public class FindCommonComponentProvider extends ContentProvider {
	private static final String LOG_TAG = Logger.getLogTag(FindCommonComponentProvider.class);

	public static final String AUTHORITY = "idv.xrloong.qiangheng.tools.FindCommonComponent";

	private static final int DATABASE_VERSION = 1;

	private static final int CODE_STROKE_TYPE= 1;
	private static final int CODE_STROKE_TYPE_ID = 2;
	private static final int CODE_STROKE= 3;
	private static final int CODE_STROKE_ID = 4;
	private static final int CODE_STROKE_GROUP= 5;
	private static final int CODE_STROKE_GROUP_ID = 6;
	private static final int CODE_STROKE_GROUP_CONTENT = 7;
	private static final int CODE_STROKE_GROUP_CONTENT_ID = 8;
	private static final int CODE_CHARACTER= 9;
	private static final int CODE_CHARACTER_ID = 10;
	private static final int CODE_ADDENDUM= 11;
	private static final int CODE_ADDENDUM_ID = 12;
	private static final int CODE_CHARACTER_ADDENDUM = 13;
	private static final int CODE_CHARACTER_ADDENDUM_ID = 14;

	private static final int CODE_STROKE_OF_GROUP = 101;
	private static final int CODE_STROKE_GROUP_BY_NAME = 102;

	private static final UriMatcher sUriMatcher;
	static {
		sUriMatcher = new UriMatcher(UriMatcher.NO_MATCH);
		sUriMatcher.addURI(AUTHORITY, "type/", CODE_STROKE_TYPE);
		sUriMatcher.addURI(AUTHORITY, "type/#", CODE_STROKE_TYPE_ID);

		sUriMatcher.addURI(AUTHORITY, "stroke/", CODE_STROKE);
		sUriMatcher.addURI(AUTHORITY, "stroke/#", CODE_STROKE_ID);

		sUriMatcher.addURI(AUTHORITY, "stroke_group/", CODE_STROKE_GROUP);
		sUriMatcher.addURI(AUTHORITY, "stroke_group/#", CODE_STROKE_GROUP_ID);

		sUriMatcher.addURI(AUTHORITY, "stroke_group_content/", CODE_STROKE_GROUP_CONTENT);
		sUriMatcher.addURI(AUTHORITY, "stroke_group_content/#", CODE_STROKE_GROUP_CONTENT_ID);

		sUriMatcher.addURI(AUTHORITY, "character/", CODE_CHARACTER);
		sUriMatcher.addURI(AUTHORITY, "character/#", CODE_CHARACTER_ID);

		sUriMatcher.addURI(AUTHORITY, "addendum/", CODE_ADDENDUM);
		sUriMatcher.addURI(AUTHORITY, "addendum/#", CODE_ADDENDUM_ID);

		sUriMatcher.addURI(AUTHORITY, "character_addendum/", CODE_CHARACTER_ADDENDUM);
		sUriMatcher.addURI(AUTHORITY, "character_addendum/#", CODE_CHARACTER_ADDENDUM_ID);

		sUriMatcher.addURI(AUTHORITY, "stroke_group/stroke/byid/#", CODE_STROKE_OF_GROUP);
		sUriMatcher.addURI(AUTHORITY, "stroke_group/stroke/byname/*", CODE_STROKE_OF_GROUP);
		sUriMatcher.addURI(AUTHORITY, "stroke_group/byname/*", CODE_STROKE_GROUP_BY_NAME);
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
		Logger.i(LOG_TAG, "query() uri: %s", uri);

		SQLiteDatabase db = mOpenHelper.getReadableDatabase();

		String tableName = null;

        String where = null;
        int code = sUriMatcher.match(uri);
        switch(code) {
        	case CODE_STROKE_TYPE:
        		tableName = StrokeTypeColumns.TABLE_NAME;
        		break;
        	case CODE_STROKE_TYPE_ID:
        		tableName = StrokeTypeColumns.TABLE_NAME;
                String strokeType = uri.getPathSegments().get(1);
                where = generateWhereClauseWithID(StrokeTypeColumns._ID, strokeType, selection);
        		break;
        	case CODE_STROKE:
        		tableName = StrokeColumns.TABLE_NAME;
        		break;
        	case CODE_STROKE_ID:
        		tableName = StrokeColumns.TABLE_NAME;
                String stroke = uri.getPathSegments().get(1);
                where = generateWhereClauseWithID(StrokeColumns._ID, stroke, selection);
        		break;
        	case CODE_STROKE_GROUP:
        		tableName = StrokeGroupColumns.TABLE_NAME;
        		break;
        	case CODE_STROKE_GROUP_ID:
        		tableName = StrokeGroupColumns.TABLE_NAME;
                String strokeGroup = uri.getPathSegments().get(1);
                where = generateWhereClauseWithID(StrokeGroupColumns._ID, strokeGroup, selection);
        		break;
        	case CODE_STROKE_GROUP_CONTENT:
        		tableName = StrokeGroupContentColumns.TABLE_NAME;
        		break;
        	case CODE_STROKE_GROUP_CONTENT_ID:
        		tableName = StrokeGroupContentColumns.TABLE_NAME;
                String strokeGroupContent = uri.getPathSegments().get(1);
                where = generateWhereClauseWithID(StrokeGroupContentColumns._ID, strokeGroupContent, selection);
        		break;
        	case CODE_CHARACTER:
        		tableName = CharacterColumns.TABLE_NAME;
        		break;
        	case CODE_CHARACTER_ID:
        		tableName = CharacterColumns.TABLE_NAME;
                String character = uri.getPathSegments().get(1);
                where = generateWhereClauseWithID(CharacterColumns._ID, character, selection);
        		break;
        	case CODE_ADDENDUM:
        		tableName = AddendumColumns.TABLE_NAME;
        		break;
        	case CODE_ADDENDUM_ID:
        		tableName = AddendumColumns.TABLE_NAME;
                String addendumId = uri.getPathSegments().get(1);
                where = generateWhereClauseWithID(AddendumColumns._ID, addendumId, selection);
        		break;
        	case CODE_CHARACTER_ADDENDUM:
        		tableName = CharacterAddendumColumns.TABLE_NAME;
        		break;
        	case CODE_CHARACTER_ADDENDUM_ID:
        		tableName = CharacterAddendumColumns.TABLE_NAME;
                String characterAddendumId = uri.getPathSegments().get(1);
                where = generateWhereClauseWithID(CharacterAddendumColumns._ID, characterAddendumId, selection);
        		break;
        	case CODE_STROKE_OF_GROUP:
        		tableName = CharacterColumns.TABLE_NAME;

        		String byMethod = uri.getPathSegments().get(2);
        		if("byid".equals(byMethod)) {
	                String strokeGroupId = uri.getPathSegments().get(3);
	        		String commandFormant = "SELECT * from %1$s JOIN %2$s On %1$s.%3$s=%2$s.%4$s AND %1$s.%5$s=%6$s";
	        		String command = String.format(commandFormant, StrokeGroupContentColumns.TABLE_NAME, StrokeColumns.TABLE_NAME, StrokeGroupContentColumns.REFERENCE_STROKE_ID,
	        				StrokeColumns._ID, StrokeGroupContentColumns.REFERENCE_GROUP_ID, strokeGroupId);
	        		return db.rawQuery(command, null);
        		} else if("byname".equals(byMethod)) {
        			String strokeGroupName = uri.getPathSegments().get(3);
//        			Cursor cursor = db.query(StrokeGroupColumns.TABLE_NAME, projection, StrokeGroupColumns.NAME+"=="+strokeGroupName, selectionArgs, null, null, sortOrder);
//        			Cursor cursor = db.query(StrokeGroupColumns.TABLE_NAME, projection, StrokeGroupColumns.NAME+"=?", new String[] {strokeGroupName}, null, null, sortOrder);
        			Cursor cursor = db.query(StrokeGroupColumns.TABLE_NAME, projection, where, selectionArgs, null, null, sortOrder);

					int indexId = cursor.getColumnIndex(StrokeGroupColumns._ID);
					int indexName = cursor.getColumnIndex(StrokeGroupColumns.NAME);
					long strokeGroupId = 0;
					cursor.moveToFirst();
					while(!cursor.isAfterLast()) {
						String name = cursor.getString(indexName);
						if(strokeGroupName.equals(name)) {
							strokeGroupId = cursor.getLong(indexId);
						}
						cursor.moveToNext();
					}
					cursor.close();
					/*
        			cursor.moveToFirst();
        			int indexId = cursor.getColumnIndex(StrokeGroupColumns._ID);
        			long strokeGroupId = cursor.getLong(indexId);
        			cursor.close();
        			*/
	        		String commandFormant = "SELECT * from %1$s JOIN %2$s On %1$s.%3$s=%2$s.%4$s AND %1$s.%5$s=%6$d";
	        		String command = String.format(commandFormant, StrokeGroupContentColumns.TABLE_NAME, StrokeColumns.TABLE_NAME, StrokeGroupContentColumns.REFERENCE_STROKE_ID,
	        				StrokeColumns._ID, StrokeGroupContentColumns.REFERENCE_GROUP_ID, strokeGroupId);
	        		return db.rawQuery(command, null);
        		}
        	case CODE_STROKE_GROUP_BY_NAME:
        		tableName = StrokeGroupColumns.TABLE_NAME;
//        		String byMethod = uri.getPathSegments().get(1);
        		String strokeGroupName = uri.getPathSegments().get(2);
        		where = StrokeGroupColumns.NAME + " LIKE '%%"+strokeGroupName+"%%'";
Logger.e(LOG_TAG, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX %s, %s", strokeGroupName, where);
        		break;
        }

        Cursor cursor = null;
        if(tableName != null) {
            cursor = db.query(tableName, projection, where, selectionArgs, null, null, sortOrder);
        }

        Logger.i(LOG_TAG, "query() -");
		return cursor;
	}

	@Override
	public Uri insert(Uri uri, ContentValues values) {
		SQLiteDatabase db = mOpenHelper.getWritableDatabase();
		long itemId = -1;
        Uri availableUri = null;
        switch(sUriMatcher.match(uri)) {
    	case CODE_STROKE_TYPE:
    		itemId = db.insert(StrokeTypeColumns.TABLE_NAME, null, values);
    		availableUri = uri;
    		break;
    	case CODE_STROKE_TYPE_ID:
    		Logger.w(LOG_TAG, "insert CODE_STROKE_TYPE_ID is not supported");
    		break;
    	case CODE_STROKE:
    		itemId = db.insert(StrokeColumns.TABLE_NAME, null, values);
    		availableUri = uri;
    		break;
    	case CODE_STROKE_ID:
    		Logger.w(LOG_TAG, "insert CODE_STROKE_ID is not supported");
    		break;
    	case CODE_STROKE_GROUP:
    		itemId = db.insert(StrokeGroupColumns.TABLE_NAME, null, values);
    		availableUri = uri;
    		break;
    	case CODE_STROKE_GROUP_ID:
    		Logger.w(LOG_TAG, "insert CODE_STROKE_GROUP_ID is not supported");
    		break;
    	case CODE_STROKE_GROUP_CONTENT:
    		itemId = db.insert(StrokeGroupContentColumns.TABLE_NAME, null, values);
    		availableUri = uri;
    		break;
    	case CODE_STROKE_GROUP_CONTENT_ID:
    		Logger.w(LOG_TAG, "insert CODE_STROKE_GROUP_CONTENT_ID is not supported");
    		break;
    	case CODE_ADDENDUM:
    		itemId = db.insert(AddendumColumns.TABLE_NAME, null, values);
    		availableUri = uri;
    		break;
    	case CODE_ADDENDUM_ID:
    		Logger.w(LOG_TAG, "insert CODE_ADDENDUM_ID is not supported");
    		break;
    	case CODE_CHARACTER_ADDENDUM:
    		itemId = db.insert(CharacterAddendumColumns.TABLE_NAME, null, values);
    		availableUri = uri;
    		break;
    	case CODE_CHARACTER_ADDENDUM_ID:
    		Logger.w(LOG_TAG, "insert CODE_CHARACTER_ADDENDUM_ID is not supported");
    		break;
        }

        Uri resultUri = null;
        if(itemId != -1) {
        	resultUri = ContentUris.withAppendedId(availableUri, itemId);
        }

		Logger.d(LOG_TAG, "insert(): %s", resultUri);
		return resultUri;
	}

	@Override
	public int bulkInsert(Uri uri, ContentValues[] values) {
		Logger.d(LOG_TAG, "bulkInsert() +");

		String tableName = null;
        switch(sUriMatcher.match(uri)) {
    	case CODE_STROKE_TYPE:
    		tableName = StrokeTypeColumns.TABLE_NAME;
    		break;
    	case CODE_STROKE_TYPE_ID:
    		Logger.w(LOG_TAG, "insert CODE_STROKE_TYPE_ID is not supported");
    		break;
    	case CODE_STROKE:
    		tableName = StrokeColumns.TABLE_NAME;
    		break;
    	case CODE_STROKE_ID:
    		Logger.w(LOG_TAG, "bulkInsert CODE_STROKE_ID is not supported");
    		break;
    	case CODE_STROKE_GROUP:
    		tableName = StrokeGroupColumns.TABLE_NAME;
    		break;
    	case CODE_STROKE_GROUP_ID:
    		Logger.w(LOG_TAG, "bulkInsert CODE_STROKE_GROUP_ID is not supported");
    		break;
    	case CODE_STROKE_GROUP_CONTENT:
    		tableName = StrokeGroupContentColumns.TABLE_NAME;
    		break;
    	case CODE_STROKE_GROUP_CONTENT_ID:
    		Logger.w(LOG_TAG, "bulkInsert CODE_STROKE_GROUP_CONTENT_ID is not supported");
    		break;
    	case CODE_CHARACTER:
    		tableName = CharacterColumns.TABLE_NAME;
    		break;
    	case CODE_CHARACTER_ID:
    		Logger.w(LOG_TAG, "bulkInsert CODE_CHARACTER_ID is not supported");
    		break;
    	case CODE_ADDENDUM:
    		tableName = AddendumColumns.TABLE_NAME;
    		break;
    	case CODE_ADDENDUM_ID:
    		Logger.w(LOG_TAG, "bulkInsert CODE_ADDENDUM_ID is not supported");
    		break;
    	case CODE_CHARACTER_ADDENDUM:
    		tableName = CharacterAddendumColumns.TABLE_NAME;
    		break;
    	case CODE_CHARACTER_ADDENDUM_ID:
    		Logger.w(LOG_TAG, "insert CODE_CHARACTER_ADDENDUM_ID is not supported");
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
	public int delete(Uri arg0, String arg1, String[] arg2) {
		return 0;
	}

	@Override
	public int update(Uri uri, ContentValues values, String selection, String[] selectionArgs) {
/*
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
		numUpdated = db.update(StrokeTypeColumns.TABLE_NAME, values, generateWhereClauseWithID(StrokeTypeColumns._ID, strDataId, selection), selectionArgs);
*/
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
    	private static final String DATABASE_NAME = "FindCommonComponent.db";

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

			String sqlCommandToCreateTableStrokeType = "CREATE TABLE "
					+ StrokeTypeColumns.TABLE_NAME
					+ " ("
					+ StrokeTypeColumns._ID + " INTEGER PRIMARY KEY, "
					+ StrokeTypeColumns.TYPE_NAME + " TEXT NOT NULL UNIQUE"
					+ ");";
			Logger.i(LOG_TAG, "create table: stroke_type");
			db.execSQL(sqlCommandToCreateTableStrokeType);

			String sqlCommandToCreateTableStroke = "CREATE TABLE "
					+ StrokeColumns.TABLE_NAME
					+ " ("
					+ StrokeColumns._ID + " INTEGER PRIMARY KEY, "
					+ StrokeColumns.DB_NAME + " TEXT NOT NULL UNIQUE, "
					+ StrokeColumns.STROKE_NAME + " TEXT, "
					+ StrokeColumns.RANGE + " TEXT, "
					+ StrokeColumns.IS_NORMAL + " BOOLEAN, "
					+ StrokeColumns.STROKE_TYPE_ID + " INTEGER references " +StrokeTypeColumns.TABLE_NAME + "(" +StrokeTypeColumns._ID  +"), "
					+ StrokeColumns.EXPRESSION + " TEXT"
					+ ");";
			Logger.i(LOG_TAG, "create table: stroke");
			db.execSQL(sqlCommandToCreateTableStroke);

			String sqlCommandToCreateTableStrokeGroup = "CREATE TABLE "
					+ StrokeGroupColumns.TABLE_NAME
					+ " ("
					+ StrokeGroupColumns._ID + " INTEGER PRIMARY KEY, "
					+ StrokeGroupColumns.DB_NAME + " TEXT NOT NULL UNIQUE, "
					+ StrokeGroupColumns.NAME + " TEXT,"
					+ StrokeGroupColumns.RANGE + " TEXT"
					+ ");";
			Logger.i(LOG_TAG, "create table: stroke_groups");
			db.execSQL(sqlCommandToCreateTableStrokeGroup);

			String sqlCommandToCreateTableStrokeGroupContent = "CREATE TABLE "
					+ StrokeGroupContentColumns.TABLE_NAME
					+ " ("
					+ StrokeGroupContentColumns._ID + " INTEGER PRIMARY KEY, "
					+ StrokeGroupContentColumns.REFERENCE_GROUP_ID + " INTEGER references " + StrokeGroupColumns.TABLE_NAME + "(" +StrokeGroupColumns._ID  +"), "
					+ StrokeGroupContentColumns.STROKE_ORDER + " INTEGER, "
					+ StrokeGroupContentColumns.REFERENCE_STROKE_ID + " INTEGER references " + StrokeColumns.TABLE_NAME + "(" +StrokeColumns._ID  +") "
					+ ");";
			Logger.i(LOG_TAG, "create table: stroke_groups_content");
			db.execSQL(sqlCommandToCreateTableStrokeGroupContent);

			String sqlCommandToCreateTableCharacter = "CREATE TABLE "
					+ CharacterColumns.TABLE_NAME
					+ " ("
					+ CharacterColumns._ID + " INTEGER PRIMARY KEY, "
					+ CharacterColumns.NAME + " TEXT, "
					+ CharacterColumns.COMMENT + " TEXT, "
					+ CharacterColumns.GROUPING_ID + " INTEGER references " + StrokeGroupColumns.TABLE_NAME + "(" +StrokeGroupColumns._ID  +")"
					+ ");";
			Logger.i(LOG_TAG, "create table: character");
			db.execSQL(sqlCommandToCreateTableCharacter);

			String sqlCommandToCreateTableAddendumRange = "CREATE TABLE "
					+ AddendumColumns.TABLE_NAME
					+ " ("
					+ AddendumColumns._ID + " INTEGER PRIMARY KEY, "
					+ AddendumColumns.NAME + " TEXT, "
					+ AddendumColumns.DB_NAME + " TEXT, "
					+ AddendumColumns.RANGE_EXPRESSION + " TEXT "
					+ ");";
			Logger.i(LOG_TAG, "create table: addendum_range");
			db.execSQL(sqlCommandToCreateTableAddendumRange);

			String sqlCommandToCreateTableCharacterAddendumRange = "CREATE TABLE "
					+ CharacterAddendumColumns.TABLE_NAME
					+ " ("
					+ CharacterAddendumColumns._ID + " INTEGER PRIMARY KEY, "
					+ CharacterAddendumColumns.REFERENCE_CHARACTER_ID + " INTEGER references " + CharacterColumns.TABLE_NAME + "(" +CharacterColumns._ID  +"), "
					+ CharacterAddendumColumns.REFERENCE_ADDENDUM_ID + " INTEGER references " + CharacterAddendumColumns.TABLE_NAME + "(" +CharacterAddendumColumns._ID  +") "
					+ ");";
			Logger.i(LOG_TAG, "create table: addendum_range");
			db.execSQL(sqlCommandToCreateTableCharacterAddendumRange);

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
