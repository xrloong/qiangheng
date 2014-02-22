package idv.xrloong.qiangheng.tools.model;

import idv.xrloong.qiangheng.tools.util.Logger;

import java.util.ArrayList;
import java.util.List;

public class DCData {
	private static final String LOG_TAG = Logger.getLogTag(DCData.class);

	private List<StrokeGroup> mStrokeSetStrokeGrouList = new ArrayList<StrokeGroup>();
	private List<StrokeGroup> mRadixSetStrokeGrouList = new ArrayList<StrokeGroup>();
	private List<DCCharacter> mCharacterList = new ArrayList<DCCharacter>();

	private String SOURCE_TYPE_STROKE_SET = "筆劃集";
	private String SOURCE_TYPE_RADIX_SET = "字根集";
	private String SOURCE_TYPE_CHARACTER_SET = "字符集";

	private String FORMAT_UNIQUE_STROKE_GROUP_NAME = "%s:%s:%s";
	private String FORMAT_UNIQUE_STROKE_NAME = "%s:%s:%s:%s";
	private String FORMAT_UNIQUE_ADDENDUM_NAME = "%s:%s:%s";

	public DCData(List<StrokeGroup> strokeSet, List<StrokeGroup> radixSet, List<DCCharacter> characterList) {
		setStrokeSet(strokeSet);
		setRadixSet(radixSet);
		setCharacterSet(characterList);
	}

	private void  setStrokeSet(List<StrokeGroup> strokeSet) {
		mStrokeSetStrokeGrouList = strokeSet;

		for(StrokeGroup strokeGroup : mStrokeSetStrokeGrouList) {
			String newStrokeGroupName = computeUniqueStrokeGroupName(SOURCE_TYPE_STROKE_SET, "", strokeGroup.getName());
			strokeGroup.setDbName(newStrokeGroupName);

			for(Stroke stroke : strokeGroup.getStrokeList()) {
				String newStrokeName = computeUniqueStrokeName(SOURCE_TYPE_STROKE_SET, "", strokeGroup.getName(), stroke.getName());
				stroke.setDbName(newStrokeName);
			}
		}
	}

	private void  setRadixSet(List<StrokeGroup> radixSet) {
		mRadixSetStrokeGrouList = radixSet;

		for(StrokeGroup strokeGroup : mRadixSetStrokeGrouList) {
			String newStrokeGroupName = computeUniqueStrokeGroupName(SOURCE_TYPE_RADIX_SET, "", strokeGroup.getName());
			strokeGroup.setDbName(newStrokeGroupName);

			for(Stroke stroke : strokeGroup.getStrokeList()) {
				String newStrokeName = computeUniqueStrokeName(SOURCE_TYPE_RADIX_SET, "", strokeGroup.getName(), stroke.getName());
				stroke.setDbName(newStrokeName);
			}
		}
	}

	private void  setCharacterSet(List<DCCharacter> characterSet) {
		mCharacterList = characterSet;

		for(DCCharacter character : mCharacterList) {
			String charName = character.getName();
			StrokeGroup strokeGroup = character.getStrokeGroup();
			String newStrokeGroupName = computeUniqueStrokeGroupName(SOURCE_TYPE_CHARACTER_SET, charName, strokeGroup.getName());
			strokeGroup.setDbName(newStrokeGroupName);

			int order = 1;
			for(Stroke stroke : strokeGroup.getStrokeList()) {
				stroke.setName(String.format("$%s#%d", strokeGroup.getName(), order));

				String newStrokeName = computeUniqueStrokeName(SOURCE_TYPE_CHARACTER_SET, charName, strokeGroup.getName(), stroke.getName());
				stroke.setDbName(newStrokeName);
				order++;
			}

			for(AddendumRange range : character.getAddendumRangeList()) {
				String name = range.getName();
				String newStrokeName = computeUniqueAddendumRangeName(SOURCE_TYPE_CHARACTER_SET, charName, name);
				range.setDbName(newStrokeName);
			}
		}
	}

	public List<StrokeGroup> getStrokeSet() {
		return mStrokeSetStrokeGrouList;
	}

	public List<StrokeGroup> getRadixSet() {
		return mRadixSetStrokeGrouList;
	}

	public List<DCCharacter> getCharacterSet() {
		return mCharacterList;
	}

	public List<AddendumRange> getAddendumRangeList() {
		List<AddendumRange> rangeList = new ArrayList<AddendumRange>();
		for(DCCharacter character : getCharacterSet()) {
			List<AddendumRange> tmpRangeList = character.getAddendumRangeList();
			rangeList.addAll(tmpRangeList);
		}
		return rangeList;
	}

	private String computeUniqueStrokeGroupName(String sourceType, String charName, String oldStrokeGroupName) {
		String newStrokeGroupName = String.format(FORMAT_UNIQUE_STROKE_GROUP_NAME, sourceType,
				charName != null ? charName : "", oldStrokeGroupName != null ? oldStrokeGroupName : "");
		return newStrokeGroupName;
	}

	private String computeUniqueStrokeName(String sourceType, String charName, String oldStrokeGroupName, String oldStrokeName) {
		String newStrokeGroupName = String.format(FORMAT_UNIQUE_STROKE_NAME, sourceType,
				charName != null ? charName : "", oldStrokeGroupName != null ? oldStrokeGroupName : "", oldStrokeName != null ? oldStrokeName : "");
		return newStrokeGroupName;
	}

	private String computeUniqueAddendumRangeName(String sourceType, String charName, String oldAddendumRangeName) {
		String newStrokeGroupName = String.format(FORMAT_UNIQUE_ADDENDUM_NAME, sourceType,
				charName != null ? charName : "", oldAddendumRangeName != null ? oldAddendumRangeName : "");
		return newStrokeGroupName;
	}
}
