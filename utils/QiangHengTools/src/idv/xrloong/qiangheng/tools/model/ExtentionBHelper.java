package idv.xrloong.qiangheng.tools.model;

import java.util.ArrayList;
import java.util.List;

import idv.xrloong.qiangheng.tools.provider.ExtentionBColumns;
import idv.xrloong.qiangheng.tools.util.Logger;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.net.Uri;

public class ExtentionBHelper {

	public static void initExtB(Context context, int codePointStart, int codePointEnd) {
		List<ContentValues> valuesList = new ArrayList<ContentValues>();
		for(int codePoint = codePointStart; codePoint <= codePointEnd; codePoint++) {
			ContentValues values = new ContentValues();
			values.put(ExtentionBColumns.CODE_POINT, codePoint);
			values.put(ExtentionBColumns.OPERATOR, "XXXX");
			values.put(ExtentionBColumns.OPERAND_1, "XXXX");
			values.put(ExtentionBColumns.OPERAND_2, "XXXX");
			valuesList.add(values);
		}

		ContentValues[] arrays = new ContentValues[valuesList.size()];
		for(int index = 0, codePoint = codePointStart; codePoint <= codePointEnd; index++, codePoint++) {
			arrays[index] = valuesList.get(index);
		}

		Uri uri = Uri.parse("content://"+ExtentionBColumns.AUTHORITY+"/"+"character");
		context.getContentResolver().bulkInsert(uri, arrays);
	}

	public static void insertList(Context context, List<CharacterDecomposition> characterDecompositionList) {

		int size = characterDecompositionList.size();
		ContentValues[] arrays = new ContentValues[size];
		for(int index = 0; index < size; index ++) {
			CharacterDecomposition characterDecomposition = characterDecompositionList.get(index);
			ContentValues values = new ContentValues();
			values.put(ExtentionBColumns.CODE_POINT, characterDecomposition.getCodePoint());
			values.put(ExtentionBColumns.OPERATOR, characterDecomposition.getOperator());
			values.put(ExtentionBColumns.OPERAND_COUNT, characterDecomposition.getOperandCount());

			int operandCount = characterDecomposition.getOperandCount();
			if(operandCount >= 1) {
				values.put(ExtentionBColumns.OPERAND_1, characterDecomposition.getOperand1());
			}
			if(operandCount >= 2) {
				values.put(ExtentionBColumns.OPERAND_2, characterDecomposition.getOperand2());
			}
			if(operandCount >= 3) {
				values.put(ExtentionBColumns.OPERAND_3, characterDecomposition.getOperand3());
			}
			if(operandCount >= 4) {
				values.put(ExtentionBColumns.OPERAND_4, characterDecomposition.getOperand4());
			}

			arrays[index] = values;
		}

		Uri uri = Uri.parse("content://"+ExtentionBColumns.AUTHORITY+"/"+"character");
		context.getContentResolver().bulkInsert(uri, arrays);
	}

	public static CharacterDecomposition query(Context context, int codePoint) {
		Uri uri = Uri.parse("content://"+ExtentionBColumns.AUTHORITY+"/"+"character");
		uri = ContentUris.withAppendedId(uri, codePoint);
		Cursor cursor = context.getContentResolver().query(uri, null, null, null, null);

		cursor.moveToFirst();
		CharacterDecomposition characterDecomposition = convertCursorToCharacterDecomposition(cursor);
		cursor.close();

		return characterDecomposition;
	}

	public static List<CharacterDecomposition> queryAll(Context context) {
		Uri uri = Uri.parse("content://"+ExtentionBColumns.AUTHORITY+"/character");
		Cursor cursor = context.getContentResolver().query(uri, null, null, null, null);

		int indexCodePoint = cursor.getColumnIndex(ExtentionBColumns.CODE_POINT);
		int indexOperator = cursor.getColumnIndex(ExtentionBColumns.OPERATOR);
		int indexOperand1 = cursor.getColumnIndex(ExtentionBColumns.OPERAND_1);
		int indexOperand2 = cursor.getColumnIndex(ExtentionBColumns.OPERAND_2);

		List<CharacterDecomposition> characterDecompositionList = new ArrayList<CharacterDecomposition>();
		cursor.moveToFirst();
		while(!cursor.isAfterLast()) {
			CharacterDecomposition characterDecomposition = convertCursorToCharacterDecomposition(cursor);

			characterDecompositionList.add(characterDecomposition);

			cursor.moveToNext();
		}
		cursor.close();

		return characterDecompositionList;
	}

	private static CharacterDecomposition convertCursorToCharacterDecomposition(Cursor cursor) {
		int indexCodePoint = cursor.getColumnIndex(ExtentionBColumns.CODE_POINT);
		int indexOperandCount = cursor.getColumnIndex(ExtentionBColumns.OPERAND_COUNT);
		int indexOperator = cursor.getColumnIndex(ExtentionBColumns.OPERATOR);
		int indexOperand1 = cursor.getColumnIndex(ExtentionBColumns.OPERAND_1);
		int indexOperand2 = cursor.getColumnIndex(ExtentionBColumns.OPERAND_2);
		int indexOperand3 = cursor.getColumnIndex(ExtentionBColumns.OPERAND_3);
		int indexOperand4 = cursor.getColumnIndex(ExtentionBColumns.OPERAND_4);

		int codePoint = cursor.getInt(indexCodePoint);
		int operandCount = cursor.getInt(indexOperandCount);
		String operator = cursor.getString(indexOperator);
		String operand1 = cursor.getString(indexOperand1);
		String operand2 = cursor.getString(indexOperand2);
		String operand3 = cursor.getString(indexOperand3);
		String operand4 = cursor.getString(indexOperand4);

		CharacterDecomposition characterDecomposition = null;
		switch(operandCount) {
		case 0:
			characterDecomposition = new CharacterDecomposition(codePoint, operator);
			break;
		case 1:
			characterDecomposition = new CharacterDecomposition(codePoint, operator, operand1);
			break;
		case 2:
			characterDecomposition = new CharacterDecomposition(codePoint, operator, operand1, operand2);
			break;
		case 3:
			characterDecomposition = new CharacterDecomposition(codePoint, operator, operand1, operand2, operand3);
			break;
		case 4:
			characterDecomposition = new CharacterDecomposition(codePoint, operator, operand1, operand2, operand3, operand4);
			break;
		}

		return characterDecomposition;
	}

	public static void updateCodePoint(Context context, CharacterDecomposition characterDecomposition) {
		int codePoint = characterDecomposition.getCodePoint();
		int operandCount = characterDecomposition.getOperandCount();

		ContentValues values = new ContentValues();
		values.put(ExtentionBColumns.CODE_POINT, codePoint);
		values.put(ExtentionBColumns.OPERAND_COUNT, operandCount);
		values.put(ExtentionBColumns.OPERATOR, characterDecomposition.getOperator());
		if(operandCount >= 1) {
			values.put(ExtentionBColumns.OPERAND_1, characterDecomposition.getOperand1());
		}
		if(operandCount >= 2) {
			values.put(ExtentionBColumns.OPERAND_2, characterDecomposition.getOperand2());
		}
		if(operandCount >= 3) {
			values.put(ExtentionBColumns.OPERAND_3, characterDecomposition.getOperand3());
		}
		if(operandCount >= 4) {
			values.put(ExtentionBColumns.OPERAND_4, characterDecomposition.getOperand4());
		}

		Uri uri = Uri.parse("content://"+ExtentionBColumns.AUTHORITY+"/"+"character");
		uri = ContentUris.withAppendedId(uri, codePoint);
		context.getContentResolver().update(uri, values, null, null);
	}
}
