package idv.xrloong.qiangheng.tools.StrokeNaming;

import idv.xrloong.qiangheng.tools.provider.StrokeColumns;
import idv.xrloong.qiangheng.tools.util.Logger;

import java.util.ArrayList;
import java.util.List;

import android.content.ContentResolver;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.net.Uri;

public class StrokeActionHelper {
	private static final String LOG_TAG = Logger.getLogTag(StrokeActionHelper.class);
	public static List<StrokeItem> query(Context context)
	{
		Logger.d(LOG_TAG, "query() +");

		Uri strokeUri = StrokeColumns.CONTENT_URI;
		Uri queryUri = strokeUri;

		ContentResolver contentResolver = context.getContentResolver();
		Cursor cursor = contentResolver.query(queryUri, new String[]{}, null, null, null);

		List<StrokeItem> strokes = new ArrayList<StrokeItem>();
		StrokeItem strokeItem=null;
		if(cursor!=null){
			cursor.moveToFirst();
			while(!cursor.isAfterLast()) {
				int idxCharName = cursor.getColumnIndex(StrokeColumns.CHARACTER_NAME);
				int idxStrokeNo = cursor.getColumnIndex(StrokeColumns.STROKE_NO);
				int idxStrokeDescription = cursor.getColumnIndex(StrokeColumns.STROKE_DESCRIPTION);
				int idxStrokeName = cursor.getColumnIndex(StrokeColumns.STROKE_NAME);

				String charName=cursor.getString(idxCharName);
				int strokeNo=cursor.getInt(idxStrokeNo);
				String strokeDescription=cursor.getString(idxStrokeDescription);
				String strokeName=cursor.getString(idxStrokeName);
				strokeItem=new StrokeItem(charName, strokeNo, strokeDescription, strokeName);

				strokes.add(strokeItem);
				cursor.moveToNext();
			}
			cursor.close();
		}

		Logger.d(LOG_TAG, "query() -");
		return strokes;
	}

	public static StrokeItem query(Context context, long dataID)
	{
		Logger.d(LOG_TAG, "query() +");

		Uri strokeUri = StrokeColumns.CONTENT_URI;
		Uri queryUri = ContentUris.withAppendedId(strokeUri, dataID);

		ContentResolver contentResolver = context.getContentResolver();
		Cursor cursor = contentResolver.query(queryUri, new String[]{}, null, null, null);

		StrokeItem strokeItem=null;
		if(cursor!=null){
			if(cursor.moveToFirst())
			{
				int idxCharName = cursor.getColumnIndex(StrokeColumns.CHARACTER_NAME);
				int idxStrokeNo = cursor.getColumnIndex(StrokeColumns.STROKE_NO);
				int idxStrokeDescription = cursor.getColumnIndex(StrokeColumns.STROKE_DESCRIPTION);
				int idxStrokeName = cursor.getColumnIndex(StrokeColumns.STROKE_NAME);

				String charName=cursor.getString(idxCharName);
				int strokeNo=cursor.getInt(idxStrokeNo);
				String strokeDescription=cursor.getString(idxStrokeDescription);
				String strokeName=cursor.getString(idxStrokeName);
				strokeItem=new StrokeItem(charName, strokeNo, strokeDescription, strokeName);
			}
			cursor.close();
		}

		Logger.d(LOG_TAG, "query() -");
		return strokeItem;
	}

	static void insert(Context context, StrokeItem strokeItem) {
		Uri uri = StrokeColumns.CONTENT_URI;
		ContentResolver contentResolver = context.getContentResolver();

		ContentValues values = new ContentValues();
		values.put(StrokeColumns.CHARACTER_NAME, strokeItem.charName);
		values.put(StrokeColumns.STROKE_NO, strokeItem.strokeNo);
		values.put(StrokeColumns.STROKE_NAME, strokeItem.strokeName);
		values.put(StrokeColumns.STROKE_DESCRIPTION, strokeItem.strokeDescription);

		contentResolver.insert(uri, values);
	}

	public static void bulkInsert(Context context, List<StrokeItem> itemList)
	{
		Logger.d(LOG_TAG, "bulkInsert() +");

		Uri uri = StrokeColumns.CONTENT_URI;
		ContentResolver contentResolver = context.getContentResolver();

		List<ContentValues> valuesList = new ArrayList<ContentValues>();
		for(StrokeItem strokeItem:itemList)
		{
			ContentValues values = new ContentValues();
			values.put(StrokeColumns.CHARACTER_NAME, strokeItem.charName);
			values.put(StrokeColumns.STROKE_NO, strokeItem.strokeNo);
			values.put(StrokeColumns.STROKE_NAME, strokeItem.strokeName);
			values.put(StrokeColumns.STROKE_DESCRIPTION, strokeItem.strokeDescription);

			valuesList.add(values);
		}
		contentResolver.bulkInsert(uri, valuesList.toArray(new ContentValues[0]));

		Logger.d(LOG_TAG, "bulkInsert() -");
	}

	public static void update(Context context, long id, String strokeName)
	{
		Logger.d(LOG_TAG, "update() +");

		Uri strokeUri = StrokeColumns.CONTENT_URI;
		Uri updateUri = ContentUris.withAppendedId(strokeUri, id);

		ContentResolver contentResolver = context.getContentResolver();
		ContentValues values = new ContentValues();
		values.put(StrokeColumns.STROKE_NAME, strokeName);

		contentResolver.update(updateUri, values, null, null);
		Logger.d(LOG_TAG, "update() -");
	}
}
