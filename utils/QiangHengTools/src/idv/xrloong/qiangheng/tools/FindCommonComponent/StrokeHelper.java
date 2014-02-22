package idv.xrloong.qiangheng.tools.FindCommonComponent;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import idv.xrloong.qiangheng.tools.model.AddendumRange;
import idv.xrloong.qiangheng.tools.model.CharacterAddendum;
import idv.xrloong.qiangheng.tools.model.DCCharacter;
import idv.xrloong.qiangheng.tools.model.DCData;
import idv.xrloong.qiangheng.tools.model.Geometry;
import idv.xrloong.qiangheng.tools.model.Stroke;
import idv.xrloong.qiangheng.tools.model.StrokeGroup;
import idv.xrloong.qiangheng.tools.model.StrokeGroupContent;
import idv.xrloong.qiangheng.tools.model.StrokeType;
import idv.xrloong.qiangheng.tools.model.StrokeTypeManager;
import idv.xrloong.qiangheng.tools.provider.AddendumColumns;
import idv.xrloong.qiangheng.tools.provider.CharacterAddendumColumns;
import idv.xrloong.qiangheng.tools.provider.CharacterColumns;
import idv.xrloong.qiangheng.tools.provider.StrokeColumns;
import idv.xrloong.qiangheng.tools.provider.StrokeGroupColumns;
import idv.xrloong.qiangheng.tools.provider.StrokeGroupContentColumns;
import idv.xrloong.qiangheng.tools.provider.StrokeTypeColumns;
import idv.xrloong.qiangheng.tools.util.Logger;
import android.content.ContentResolver;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.net.Uri;

public class StrokeHelper {
	private static final String LOG_TAG = Logger.getLogTag(StrokeHelper.class);
	private static final int ORDER_BASE = 1;

	public static List<StrokeType> queryAllStrokeTypes(Context context) {
		Logger.d(LOG_TAG, "queryAllStrokeTypes() +");

		Uri uri = Uri.parse("content://"+StrokeTypeColumns.AUTHORITY+"/type");

		List<StrokeType> resultNameList = new ArrayList<StrokeType>();
		Cursor cursor = context.getContentResolver().query(uri, null, null, null, null);
		if(cursor != null) {
			int indexTypeName = cursor.getColumnIndex(StrokeTypeColumns.TYPE_NAME);
			int indexId = cursor.getColumnIndex(StrokeTypeColumns._ID);

			cursor.moveToFirst();
			while(!cursor.isAfterLast()) {
				String typeName = cursor.getString(indexTypeName);
				long id = cursor.getLong(indexId);
				resultNameList.add(new StrokeType(typeName, id));

				cursor.moveToNext();
			}
			cursor.close();
		}

		Logger.d(LOG_TAG, "queryAllStrokeTypes() -");
		return resultNameList;
	}

	private static List<Stroke> queryAllStroke(Context context) {
		Logger.d(LOG_TAG, "queryAllStrokeTypes() +");

		Uri uri = Uri.parse("content://"+StrokeColumns.AUTHORITY+"/stroke");

		List<Stroke> resultNameList = new ArrayList<Stroke>();

		Cursor cursor = context.getContentResolver().query(uri, null, null, null, null);
		if(cursor != null) {
			cursor.moveToFirst();
			while(!cursor.isAfterLast()) {
				Stroke stroke = convertCursorToStroke(context, cursor);
				
				resultNameList.add(stroke);
				cursor.moveToNext();
			}
			cursor.close();
		}

		Logger.d(LOG_TAG, "queryAllStroke() -");
		return resultNameList;
	}

	private static Stroke convertCursorToStroke(Context context, Cursor cursor) {
		Stroke stroke = null;

		if(cursor != null) {
			int indexId = cursor.getColumnIndex(StrokeColumns._ID);
			int indexDbName = cursor.getColumnIndex(StrokeColumns.DB_NAME);
			int indexIsNormal = cursor.getColumnIndex(StrokeColumns.IS_NORMAL);
			int indexTypeId = cursor.getColumnIndex(StrokeColumns.STROKE_TYPE_ID);
			int indexExpression = cursor.getColumnIndex(StrokeColumns.EXPRESSION);
			int indexName = cursor.getColumnIndex(StrokeColumns.STROKE_NAME);
			int indexRange = cursor.getColumnIndex(StrokeColumns.RANGE);


			long id = cursor.getLong(indexId);
			String dbName = cursor.getString(indexDbName);
			String expression = cursor.getString(indexExpression);
			String name = cursor.getString(indexName);
			boolean isNormal = cursor.getInt(indexIsNormal) > 0;
			String rangeExpression = cursor.getString(indexRange);

			if(isNormal) {
				long typeId = cursor.getLong(indexTypeId);
				String strokeTypeName = StrokeTypeManager.getInstance().getTypeName(typeId-1);

				stroke = Stroke.generateNormal(name, expression, strokeTypeName);
			} else {
				stroke = Stroke.generateRef(name, expression);
			}
			stroke.setRange(rangeExpression);

			stroke.setDbId(id);
			stroke.setDbName(dbName);
		}

		return stroke;
	}

	public static StrokeGroup queryStrokeGroup(Context context, long groupId) {
		Logger.d(LOG_TAG, "queryStrokeGroup() +");

		Uri uri = Uri.parse("content://"+StrokeGroupColumns.AUTHORITY+"/stroke_group");
		uri = ContentUris.withAppendedId(uri, groupId);

		StrokeGroup strokeGroup = null;
		Cursor cursor = context.getContentResolver().query(uri, null, null, null, null);
		if(cursor != null) {
			cursor.moveToFirst();

			strokeGroup = convertCursorToStrokeGroup(cursor);

			cursor.close();
		}
		List<Stroke> strokeList = queryAllStrokeOfGroup(context, groupId);
		strokeGroup.setStrokeList(strokeList);

		Logger.d(LOG_TAG, "queryStrokeGroup() -");
		return strokeGroup;
	}

	private static List<StrokeGroup> queryAllStrokeGroup(Context context) {
		Logger.d(LOG_TAG, "queryAllStrokeGroup() +");

		Uri uri = Uri.parse("content://"+StrokeGroupColumns.AUTHORITY+"/stroke_group");

		List<StrokeGroup> strokeGroupList = new ArrayList<StrokeGroup>();
		Cursor cursor = context.getContentResolver().query(uri, null, null, null, null);
		if(cursor != null) {
			cursor.moveToFirst();
			while(!cursor.isAfterLast()) {
				StrokeGroup strokeGroup = convertCursorToStrokeGroup(cursor);
				if(strokeGroup != null) {
					strokeGroupList.add(strokeGroup);
				}
				cursor.moveToNext();
			}
			cursor.close();
		}

		Logger.d(LOG_TAG, "queryAllStrokeGroup() -");
		return strokeGroupList;
	}

	private static StrokeGroup convertCursorToStrokeGroup(Cursor cursor) {
		StrokeGroup strokeGroup = null;

		if(cursor != null) {
			int indexId = cursor.getColumnIndex(StrokeGroupColumns._ID);
			int indexDbName = cursor.getColumnIndex(StrokeGroupColumns.DB_NAME);
			int indexName = cursor.getColumnIndex(StrokeGroupColumns.NAME);

			long id = cursor.getLong(indexId);
			String dbName = cursor.getString(indexDbName);
			String name = cursor.getString(indexName);

			strokeGroup = new StrokeGroup(new ArrayList<Stroke>());
			strokeGroup.setDbId(id);
			strokeGroup.setDbName(dbName);
			strokeGroup.setName(name);
		}
		return strokeGroup;
	}

	private static List<DCCharacter> queryAllCharacter(Context context) {
		Logger.d(LOG_TAG, "queryAllCharacter() +");

		Uri uri = Uri.parse("content://"+CharacterColumns.AUTHORITY+"/character");

		List<DCCharacter> characterList = new ArrayList<DCCharacter>();
		Cursor cursor = context.getContentResolver().query(uri, null, null, null, null);
		if(cursor != null) {
			int indexId = cursor.getColumnIndex(CharacterColumns._ID);
			int indexName = cursor.getColumnIndex(CharacterColumns.NAME);
			int indexComment = cursor.getColumnIndex(CharacterColumns.COMMENT);
			int indexGroupId = cursor.getColumnIndex(CharacterColumns.GROUPING_ID);

			cursor.moveToFirst();
			while(!cursor.isAfterLast()) {
				long id = cursor.getLong(indexId);
				String name = cursor.getString(indexName);
				String comment = cursor.getString(indexComment);
				long groupingId = cursor.getLong(indexGroupId);

				DCCharacter character = new DCCharacter(name, comment);
				character.setDbId(id);
				character.setGroupingId(groupingId);

				characterList.add(character);
				cursor.moveToNext();
			}
			cursor.close();
		}

		Logger.d(LOG_TAG, "queryAllCharacter() -");
		return characterList;
	}

	public static DCCharacter queryCharacter(Context context, int charDbId) {
		Logger.d(LOG_TAG, "queryCharacter() +");

		Uri uri = Uri.parse("content://"+CharacterColumns.AUTHORITY+"/character");
		Uri queryUri = ContentUris.withAppendedId(uri, charDbId);

		List<DCCharacter> characterList = new ArrayList<DCCharacter>();
		Cursor cursor = context.getContentResolver().query(queryUri, null, null, null, null);
		DCCharacter character = null;
		if(cursor != null) {
			int indexId = cursor.getColumnIndex(CharacterColumns._ID);
			int indexName = cursor.getColumnIndex(CharacterColumns.NAME);
			int indexComment = cursor.getColumnIndex(CharacterColumns.COMMENT);
			int indexGroupId = cursor.getColumnIndex(CharacterColumns.GROUPING_ID);

			cursor.moveToFirst();
			long id = cursor.getLong(indexId);
			String name = cursor.getString(indexName);
			String comment = cursor.getString(indexComment);
			long groupingId = cursor.getLong(indexGroupId);

			character = new DCCharacter(name, comment);
			character.setDbId(id);
			character.setGroupingId(groupingId);

			characterList.add(character);
			cursor.moveToNext();

			cursor.close();
		}

		Logger.d(LOG_TAG, "queryCharacter() -");
		return character;
	}

	private static class StrokeGroupContentInfo {
		private long mGroupId;
		private long mStrokeId;
		private int mOrder;
	}

	private static List<Stroke> queryAllStrokeOfGroup(Context context, long targetGroupId) {
		Logger.d(LOG_TAG, "queryAllStrokeGroupContentOfGroup() +");

//		Uri uri = Uri.parse("content://"+StrokeGroupContentColumns.AUTHORITY+"/stroke_group_content");
		Uri uri = Uri.parse("content://"+StrokeGroupContentColumns.AUTHORITY+"/stroke_of_group");
		uri = ContentUris.withAppendedId(uri, targetGroupId);

		List<Stroke> infoList = new ArrayList<Stroke>();

		Cursor cursor = context.getContentResolver().query(uri, null, null, null, null);
		if(cursor != null) {
			cursor.moveToFirst();
			while(!cursor.isAfterLast()) {
				Stroke stroke = convertCursorToStroke(context, cursor);

				infoList.add(stroke);

				cursor.moveToNext();
			}

			cursor.close();
		}

		Logger.d(LOG_TAG, "queryAllStrokeGroupContentOfGroup() -");
		return infoList;
	}

	private static List<StrokeGroupContentInfo> queryAllStrokeGroupContent(Context context) {
		Logger.d(LOG_TAG, "queryAllStrokeGroupContent() +");

		Uri uri = Uri.parse("content://"+StrokeGroupContentColumns.AUTHORITY+"/stroke_group_content");

		List<StrokeGroupContentInfo> infoList = new ArrayList<StrokeGroupContentInfo>();

		Cursor cursor = context.getContentResolver().query(uri, null, null, null, null);
		if(cursor != null) {
			int indexId = cursor.getColumnIndex(StrokeGroupContentColumns._ID);
			int indexGroupId = cursor.getColumnIndex(StrokeGroupContentColumns.REFERENCE_GROUP_ID);
			int indexStrokeOrder = cursor.getColumnIndex(StrokeGroupContentColumns.STROKE_ORDER);
			int indexStrokeId = cursor.getColumnIndex(StrokeGroupContentColumns.REFERENCE_STROKE_ID);

			cursor.moveToFirst();
			while(!cursor.isAfterLast()) {
				long groupId = cursor.getLong(indexGroupId);
				long strokeId = cursor.getLong(indexStrokeId);
				int strokeOrder = cursor.getInt(indexStrokeOrder);

				StrokeGroupContentInfo info = new StrokeGroupContentInfo();
				info.mGroupId = groupId;
				info.mStrokeId = strokeId;
				info.mOrder = strokeOrder;

				infoList.add(info);
				cursor.moveToNext();
			}
			cursor.close();
		}

		Logger.d(LOG_TAG, "queryAllStrokeGroupContent() -");
		return infoList;
	}

	private static List<AddendumRange> queryAllAddendum(Context context) {
		Logger.d(LOG_TAG, "queryAllAddendum() +");

		Uri uri = Uri.parse("content://"+CharacterColumns.AUTHORITY+"/addendum");

		List<AddendumRange> addendumRangeList = new ArrayList<AddendumRange>();
		Cursor cursor = context.getContentResolver().query(uri, null, null, null, null);
		if(cursor != null) {
			int indexId = cursor.getColumnIndex(AddendumColumns._ID);
			int indexName = cursor.getColumnIndex(AddendumColumns.NAME);
			int indexDbName = cursor.getColumnIndex(AddendumColumns.DB_NAME);
			int indexRangeExpression = cursor.getColumnIndex(AddendumColumns.RANGE_EXPRESSION);
			cursor.moveToFirst();
			while(!cursor.isAfterLast()) {
				long id = cursor.getLong(indexId);
				String name = cursor.getString(indexName);
				String dbName = cursor.getString(indexDbName);
				String rangeExpression = cursor.getString(indexRangeExpression);

				AddendumRange addendumRange = new AddendumRange(name);
				addendumRange.setGeometry(new Geometry(rangeExpression));
				addendumRange.setDbId(id);
				addendumRange.setDbName(dbName);

				addendumRangeList.add(addendumRange);
				cursor.moveToNext();
			}
			cursor.close();
		}

		Logger.d(LOG_TAG, "queryAllAddendum() -");
		return addendumRangeList;
	}

	private static class CharacterAddendumInfo {
		private long mCharacterId;
		private long mAddendumId;
	}

	private static List<CharacterAddendumInfo> queryAllCharacterAddendum(Context context) {
		Logger.d(LOG_TAG, "queryAllCharacterAddendum() +");

		Uri uri = Uri.parse("content://"+CharacterAddendumColumns.AUTHORITY+"/character_addendum");

		List<CharacterAddendumInfo> characterAddendumRangeList = new ArrayList<CharacterAddendumInfo>();
		Cursor cursor = context.getContentResolver().query(uri, null, null, null, null);
		if(cursor != null) {
			int indexCharacterId = cursor.getColumnIndex(CharacterAddendumColumns.REFERENCE_CHARACTER_ID);
			int indexAddendumId = cursor.getColumnIndex(CharacterAddendumColumns.REFERENCE_ADDENDUM_ID);
			cursor.moveToFirst();
			while(!cursor.isAfterLast()) {
				long characterId = cursor.getLong(indexCharacterId);
				long addendumId = cursor.getLong(indexAddendumId);

				CharacterAddendumInfo addendumRange = new CharacterAddendumInfo();
				addendumRange.mCharacterId = characterId;
				addendumRange.mAddendumId = addendumId;

				characterAddendumRangeList.add(addendumRange);
				cursor.moveToNext();
			}
			cursor.close();
		}

		Logger.d(LOG_TAG, "queryAllAddendum() -");
		return characterAddendumRangeList;
	}

	public static DCData queryDCData(Context context) {
		List<StrokeGroup> strokeGroupList = queryAllStrokeGroup(context);
		List<DCCharacter> characterList = queryAllCharacter(context);

		List<StrokeGroup> strokeSet = new ArrayList<StrokeGroup>();
		List<StrokeGroup> radixSet = new ArrayList<StrokeGroup>();
		List<DCCharacter> characterSet = characterList;
		for(StrokeGroup strokeGroup : strokeGroupList) {
			String strokeGroupName = strokeGroup.getDbName();

			if(strokeGroupName.startsWith("字根集")) {
				radixSet.add(strokeGroup);
			} else if(strokeGroupName.startsWith("字符集")) {
			} else if(strokeGroupName.startsWith("筆劃集")) {
				strokeSet.add(strokeGroup);
			}
		}
		Map<Long, StrokeGroup> mapStrokeGroup = new HashMap<Long, StrokeGroup>();
		for(StrokeGroup strokeGroup : strokeGroupList) {
			mapStrokeGroup.put(strokeGroup.getDbId(), strokeGroup);
		}

		List<Stroke> strokeList= queryAllStroke(context);
		Map<Long, Stroke> mapStroke = new HashMap<Long, Stroke>();
		for(Stroke stroke : strokeList) {
			mapStroke.put(stroke.getDbId(), stroke);
		}

		List<StrokeGroupContentInfo> infoList = queryAllStrokeGroupContent(context);

		for(StrokeGroup strokeGroup : strokeGroupList) {
			long dbId = strokeGroup.getDbId();
			List<Stroke> tmpStrokeList = new ArrayList<Stroke>();
			for(StrokeGroupContentInfo info : infoList) {
				if(dbId == info.mGroupId) {
					Stroke stroke = mapStroke.get(info.mStrokeId);
					tmpStrokeList.add(stroke);
				}
			}
			strokeGroup.setStrokeList(tmpStrokeList);
		}

		for(DCCharacter character : characterSet) {
			long groupingId = character.getGroupingId();
			StrokeGroup strokeGroup = mapStrokeGroup.get(groupingId);
			character.setStrokeGroup(strokeGroup);
		}
		DCData dcData = new DCData(strokeSet, radixSet, characterSet);

		Map<Long, AddendumRange> mapAddendum = new HashMap<Long, AddendumRange>();
		List<AddendumRange> addendumList = queryAllAddendum(context);
		for(AddendumRange range : addendumList) {
			mapAddendum.put(range.getDbId(), range);
		}
		List<CharacterAddendumInfo> characterAddendumInfoList = queryAllCharacterAddendum(context);

		for(DCCharacter character : characterSet) {
			long characterId = character.getDbId();

			List<AddendumRange> rangeList = new ArrayList<AddendumRange>();
			for(CharacterAddendumInfo characterAddendumInfo : characterAddendumInfoList) {
				if(characterAddendumInfo.mCharacterId == characterId) {
					long rangeId = characterAddendumInfo.mAddendumId;
					AddendumRange range = mapAddendum.get(rangeId);
					rangeList.add(range);
				}
			}
			character.setAddonRangeList(rangeList);
		}
		return dcData;
	}

	public static void insertAllStrokeTypes(Context context) {
		Logger.d(LOG_TAG, "insertAllStrokeTypes() +");

		ContentResolver resolver = context.getContentResolver();

		List<String> strokeNameList = StrokeTypeManager.getInstance().getStrokeNameList();
		for(String name : strokeNameList) {
			Uri uri = Uri.parse("content://"+StrokeTypeColumns.AUTHORITY+"/type");
			ContentValues values = new ContentValues();
			values.put(StrokeTypeColumns.TYPE_NAME, name);
			resolver.insert(uri, values);
		}

		Logger.d(LOG_TAG, "insertAllStrokeTypes() +");
	}
/*
	private static void insertStroke(Context context, Stroke stroke) {
		Logger.d(LOG_TAG, "insertStroke() +");

		ContentResolver resolver = context.getContentResolver();
		Uri uri = Uri.parse("content://"+StrokeColumns.AUTHORITY+"/stroke");
		ContentValues values = convertStrokeToContentValues(stroke);

		resolver.insert(uri, values);

		Logger.d(LOG_TAG, "insertStroke() -");
	}
*/
	private static void insertStrokeList(Context context, List<Stroke> strokeList) {
		Logger.d(LOG_TAG, "insertStrokeList() +");

		ContentResolver resolver = context.getContentResolver();
		Uri uri = Uri.parse("content://"+StrokeColumns.AUTHORITY+"/stroke");

		int size = strokeList.size();
		ContentValues valuesArray[] = new ContentValues[size];
		for(int i = 0; i < size; i++) {
			Stroke stroke = strokeList.get(i);
			valuesArray[i] = convertStrokeToContentValues(stroke);
		}

		resolver.bulkInsert(uri, valuesArray);
		Logger.d(LOG_TAG, "insertStrokeList() -");
	}

	private static ContentValues convertStrokeToContentValues(Stroke stroke) {
		Logger.d(LOG_TAG, "convertStrokeToContentValues() +");

		ContentValues values = new ContentValues();
		values.put(StrokeColumns.DB_NAME, stroke.getDbName());
		values.put(StrokeColumns.STROKE_NAME, stroke.getName());
		values.put(StrokeColumns.EXPRESSION, stroke.getExpression());
		values.put(StrokeColumns.RANGE, stroke.getRange());
		values.put(StrokeColumns.IS_NORMAL, stroke.isNormal());
		if(stroke.isNormal()) {
			values.put(StrokeColumns.STROKE_TYPE_ID, stroke.getTypeId());
		} else {
			values.putNull(StrokeColumns.STROKE_TYPE_ID);
//			values.putNull(StrokeColumns.STROKE_TYPE_ID);
		}

		Logger.d(LOG_TAG, "convertStrokeToContentValues() -");
		return values;
	}
/*
	private static void insertStrokeGroup(Context context, StrokeGroup strokeGroup) {
		Logger.d(LOG_TAG, "insertStrokeGroup() +");

		ContentResolver resolver = context.getContentResolver();
		Uri uri = Uri.parse("content://"+StrokeGroupColumns.AUTHORITY+"/stroke_group");

		ContentValues values = convertStrokeGroupToContentValues(strokeGroup);

		resolver.insert(uri, values);
		Logger.d(LOG_TAG, "insertStrokeGroup() -");
	}
*/
	private static void insertStrokeGroupList(Context context, List<StrokeGroup> strokeGroupList) {
		Logger.d(LOG_TAG, "insertStrokeGroupList() +");

		ContentResolver resolver = context.getContentResolver();
		Uri uri = Uri.parse("content://"+StrokeColumns.AUTHORITY+"/stroke_group");

		int size = strokeGroupList.size();
		ContentValues valuesArray[] = new ContentValues[size];
		for(int i = 0; i < size; i++) {
			StrokeGroup strokeGroup = strokeGroupList.get(i);
			valuesArray[i] = convertStrokeGroupToContentValues(strokeGroup);
		}

		resolver.bulkInsert(uri, valuesArray);
		Logger.d(LOG_TAG, "insertStrokeGroupList() -");
	}

	private static ContentValues convertStrokeGroupToContentValues(StrokeGroup strokeGroup) {
		Logger.d(LOG_TAG, "convertStrokeGroupToContentValues() +");

		ContentValues values = new ContentValues();
		values.put(StrokeGroupColumns.DB_NAME, strokeGroup.getDbName());
		values.put(StrokeGroupColumns.NAME, strokeGroup.getName());

		Logger.d(LOG_TAG, "convertStrokeGroupToContentValues() -");
		return values;
	}
/*
	private static Uri insertStrokeGroupContent(Context context, StrokeGroupContent strokeGroupContent) {
		Uri uri = Uri.parse("content://"+StrokeGroupContentColumns.AUTHORITY+"/stroke_group_content");

		ContentResolver resolver = context.getContentResolver();
		ContentValues values = convertStrokeGroupContentToContentValues(strokeGroupContent);

		Uri resultUri = resolver.insert(uri, values);

		return resultUri;
	}
*/
	private static void insertStrokeGroupContentList(Context context, List<StrokeGroupContent> strokeGroupContentList) {
		Logger.d(LOG_TAG, "insertStrokeGroupList() +");

		ContentResolver resolver = context.getContentResolver();
		Uri uri = Uri.parse("content://"+StrokeColumns.AUTHORITY+"/stroke_group_content");

		int size = strokeGroupContentList.size();
		ContentValues valuesArray[] = new ContentValues[size];
		for(int i = 0; i < size; i++) {
			StrokeGroupContent strokeGroupContent = strokeGroupContentList.get(i);
			valuesArray[i] = convertStrokeGroupContentToContentValues(strokeGroupContent);
		}

		resolver.bulkInsert(uri, valuesArray);
		Logger.d(LOG_TAG, "insertStrokeGroupList() -");
	}

	private static ContentValues convertStrokeGroupContentToContentValues(StrokeGroupContent strokeGroupContent) {
		Logger.d(LOG_TAG, "convertStrokeGroupContentToContentValues() +");

		ContentValues values = new ContentValues();
		values.put(StrokeGroupContentColumns.REFERENCE_GROUP_ID, strokeGroupContent.getStrokGroupDbId());
		values.put(StrokeGroupContentColumns.STROKE_ORDER, strokeGroupContent.getOrder());
		values.put(StrokeGroupContentColumns.REFERENCE_STROKE_ID, strokeGroupContent.getStrokDbId());
		Logger.d(LOG_TAG, "convertStrokeGroupContentToContentValues() -");
		return values;
	}

	private static void insertCharacterList(Context context, List<DCCharacter> characterList) {
		Logger.d(LOG_TAG, "insertCharacterList() +");

		List<StrokeGroup> newStrokeGroupList = queryAllStrokeGroup(context);

		Map<String, Long> mapStrokeGroup = new HashMap<String, Long>();
		for(StrokeGroup strokeGroup : newStrokeGroupList) {
			mapStrokeGroup.put(strokeGroup.getDbName(), strokeGroup.getDbId());
		}

		for(DCCharacter character : characterList) {
			StrokeGroup strokeGroup = character.getStrokeGroup();
			long strokdGroupId = mapStrokeGroup.get(strokeGroup.getDbName());
			strokeGroup.setDbId(strokdGroupId);
		}


		ContentResolver resolver = context.getContentResolver();
		Uri uri = Uri.parse("content://"+CharacterColumns.AUTHORITY+"/character");

		int size = characterList.size();
		ContentValues valuesArray[] = new ContentValues[size];
		for(int i = 0; i < size; i++) {
			DCCharacter character = characterList.get(i);
			valuesArray[i] = convertCharacterValues(character);
		}

		resolver.bulkInsert(uri, valuesArray);



		Map<String, Long> mapCharacter = new HashMap<String, Long>();
		List<DCCharacter> newCharacterList = queryAllCharacter(context);
		for(DCCharacter character : newCharacterList) {
			long dbId = character.getDbId();
			String name = character.getName();
			mapCharacter.put(name, dbId);
		}

		Map<String, Long> mapAddendum = new HashMap<String, Long>();
		List<AddendumRange> addendumRangeList = queryAllAddendum(context);
		for(AddendumRange range : addendumRangeList) {
			long dbId = range.getDbId();
			String dbName = range.getDbName();
			mapAddendum.put(dbName, dbId);
		}

		for(DCCharacter character : characterList) {
			long characterDbId = mapCharacter.get(character.getName());
			character.setDbId(characterDbId);
			for(AddendumRange range : character.getAddendumRangeList()) {
				long rangeDbId = mapAddendum.get(range.getDbName());
				range.setDbId(rangeDbId);
			}
		}

		List<CharacterAddendum> characterAddendumList = new ArrayList<CharacterAddendum>();
		for(DCCharacter character : characterList) {
			for(AddendumRange range : character.getAddendumRangeList()) {
				CharacterAddendum characterAddendum = new CharacterAddendum(character, range);
				characterAddendumList.add(characterAddendum);
			}
		}

		Uri caUri = Uri.parse("content://"+CharacterColumns.AUTHORITY+"/character_addendum");

		int caSize = characterAddendumList.size();
		valuesArray = new ContentValues[caSize];
		for(int i = 0; i < caSize; i++) {
			CharacterAddendum characterAddendum = characterAddendumList.get(i);
			valuesArray[i] = convertCharacterAddendumRangeValues(characterAddendum);
		}

		resolver.bulkInsert(caUri, valuesArray);

		Logger.d(LOG_TAG, "insertCharacterList() -");
	}

	private static ContentValues convertCharacterAddendumRangeValues(CharacterAddendum characterAddendum) {
		Logger.d(LOG_TAG, "convertCharacterAddendumRangeValues() +");

		ContentValues values = new ContentValues();
		values.put(CharacterAddendumColumns.REFERENCE_CHARACTER_ID, characterAddendum.getCharacterId());
		values.put(CharacterAddendumColumns.REFERENCE_ADDENDUM_ID, characterAddendum.getAddendumRangeDbId());

		Logger.d(LOG_TAG, "convertCharacterAddendumRangeValues() -");
		return values;
	}

	private static ContentValues convertCharacterValues(DCCharacter character) {
		Logger.d(LOG_TAG, "convertCharacterValues() +");

		ContentValues values = new ContentValues();
		values.put(CharacterColumns.NAME, character.getName());
		values.put(CharacterColumns.COMMENT, character.getComment());
		values.put(CharacterColumns.GROUPING_ID, character.getStrokeGroup().getDbId());

		Logger.d(LOG_TAG, "convertCharacterValues() -");
		return values;
	}

	private static void insertStrokeSet(Context context, List<StrokeGroup> strokeGroupList) {
		List<StrokeGroup> allStrokeGroupList = strokeGroupList;
		List<Stroke> allStrokeList = new ArrayList<Stroke>();
		for(StrokeGroup strokeGroup : strokeGroupList) {
			allStrokeList.addAll(strokeGroup.getStrokeList());
		}

		insertStrokeGroupList(context, allStrokeGroupList);
		insertStrokeList(context, allStrokeList);

		List<Stroke> newStrokeList = queryAllStroke(context);
		List<StrokeGroup> newStrokeGroupList = queryAllStrokeGroup(context);

		Map<String, Long> mapStroke = new HashMap<String, Long>();
		for(Stroke stroke : newStrokeList) {
			mapStroke.put(stroke.getDbName(), stroke.getDbId());
		}

		Map<String, Long> mapStrokeGroup = new HashMap<String, Long>();
		for(StrokeGroup strokeGroup : newStrokeGroupList) {
			mapStrokeGroup.put(strokeGroup.getDbName(), strokeGroup.getDbId());
		}

		List<StrokeGroupContent> strokeGroupContentList = new ArrayList<StrokeGroupContent>();

		for(StrokeGroup strokeGroup : strokeGroupList) {
			strokeGroup.setDbId(mapStrokeGroup.get(strokeGroup.getDbName()));
			int order = ORDER_BASE;
			for(Stroke stroke : strokeGroup.getStrokeList()) {
				stroke.setDbId(mapStroke.get(stroke.getDbName()));
				StrokeGroupContent strokeGroupContent = new StrokeGroupContent(strokeGroup, order, stroke);
				strokeGroupContentList.add(strokeGroupContent);
				order ++;
			}
		}
		insertStrokeGroupContentList(context, strokeGroupContentList);
	}


	private static void insertAddendumRangeList(Context context, List<AddendumRange> addendumRangeList) {
		Logger.d(LOG_TAG, "insertAddendumRangeList() +");

		ContentResolver resolver = context.getContentResolver();
		Uri uri = Uri.parse("content://"+AddendumColumns.AUTHORITY+"/addendum");

		int size = addendumRangeList.size();
		ContentValues valuesArray[] = new ContentValues[size];
		for(int i = 0; i < size; i++) {
			AddendumRange addendumRange = addendumRangeList.get(i);
			valuesArray[i] = convertAddendumRangeValues(addendumRange);
		}

		resolver.bulkInsert(uri, valuesArray);
		Logger.d(LOG_TAG, "insertAddendumRangeList() -");
	}

	private static ContentValues convertAddendumRangeValues(AddendumRange addendumRange) {
		Logger.d(LOG_TAG, "convertCharacterValues() +");

		ContentValues values = new ContentValues();
		values.put(AddendumColumns.NAME, addendumRange.getName());
		values.put(AddendumColumns.DB_NAME, addendumRange.getDbName());
		values.put(AddendumColumns.RANGE_EXPRESSION, addendumRange.getExpression());

		Logger.d(LOG_TAG, "convertAddendumRangeValues() -");
		return values;
	}

	public static void insertDCData(Context context, DCData dcData) {
		List<StrokeGroup> strokeSetStrokeGroupList = dcData.getStrokeSet();
		List<StrokeGroup> radixSetStrokeGroupList = dcData.getRadixSet();
		List<DCCharacter> characterList = dcData.getCharacterSet();
		List<AddendumRange> rangeList = dcData.getAddendumRangeList();

		insertStrokeSet(context, strokeSetStrokeGroupList);
		insertStrokeSet(context, radixSetStrokeGroupList);

		List<StrokeGroup> strokeGroupList = new ArrayList<StrokeGroup>();
		for(DCCharacter character : characterList) {
			StrokeGroup strokeGroup = character.getStrokeGroup();

			strokeGroupList.add(strokeGroup);
		}
		insertStrokeSet(context, strokeGroupList);
		insertAddendumRangeList(context, rangeList);

		insertCharacterList(context, characterList);
	}
}
