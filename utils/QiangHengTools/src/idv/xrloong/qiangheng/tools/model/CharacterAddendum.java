package idv.xrloong.qiangheng.tools.model;

public class CharacterAddendum {

	private long mCharacterDbId;
	private long mAddendumRangeDbId;

	public CharacterAddendum(DCCharacter character, AddendumRange addendumRange) {
		mCharacterDbId = character.getDbId();
		mAddendumRangeDbId = addendumRange.getDbId();
	}

	public long getCharacterId() {
		return mCharacterDbId;
	}

	public long getAddendumRangeDbId() {
		return mAddendumRangeDbId;
	}
}
