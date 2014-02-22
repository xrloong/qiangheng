package idv.xrloong.qiangheng.tools.model;

public class AddendumRange {
	private String mName;
	private Geometry mGeometry;
	private long mDbId;
	private String mDbName;

	public AddendumRange(String name) {
		mName = name;
	}

	public void setGeometry(Geometry geometry) {
		mGeometry = geometry;
	}

	public String getName() {
		return mName;
	}

	public Geometry getGeometry() {
		return mGeometry;
	}

	public String getExpression() {
		return mGeometry.getExpression();
	}

	public void setDbId(long id) {
		mDbId = id;
	}

	public long getDbId() {
		return mDbId;
	}

	public void setDbName(String dbName) {
		mDbName = dbName;
	}

	public String getDbName() {
		return mDbName;
	}
}
