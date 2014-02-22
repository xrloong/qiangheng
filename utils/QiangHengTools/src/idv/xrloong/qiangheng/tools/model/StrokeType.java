package idv.xrloong.qiangheng.tools.model;

public class StrokeType {

	private String mStrokeTypeName;
	private long mDBID;

	public StrokeType(String name, long id) {
		mStrokeTypeName = name;
		mDBID = id;
	}

	public long getDBID() {
		return mDBID;
	}

	public String getName() {
		return mStrokeTypeName;
	}
}
