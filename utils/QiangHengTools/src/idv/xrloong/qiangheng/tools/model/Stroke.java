package idv.xrloong.qiangheng.tools.model;

import java.util.List;

import android.graphics.Path;

import idv.xrloong.qiangheng.tools.util.Logger;

public class Stroke {
	private static final String LOG_TAG = Logger.getLogTag(Stroke.class);

	private long mDdId = 0;
	private String mDbName;

	private boolean mIsRef;

	private String mName;
	private String mStrokeTypeName;
	private String mExpression;
	private String mRangeExpression;
	private long mTypeId;

	private Stroke(String name, String expression) {
		mName = name;
		mExpression = expression;
	}

	public static Stroke generateNormal(String name, String expression, String strokeTypeName) {
		Stroke stroke = new Stroke(name, expression);
		stroke.mIsRef = false;
		stroke.mStrokeTypeName = strokeTypeName;
		stroke.mTypeId = StrokeTypeManager.getInstance().getTypeId(strokeTypeName);
		return stroke;
	}

	public static Stroke generateRef(String name, String expression) {
		Stroke stroke = new Stroke(name, expression);
		stroke.mIsRef = true;
		return stroke;
	}

	public boolean isRef() {
		return mIsRef;
	}

	public boolean isNormal() {
		return !mIsRef;
	}

	public long getTypeId() {
		return mTypeId;
	}

	public String getName() {
		return mName;
	}

	public String getExpression() {
		return mExpression;
	}

	public String getXExpression() {
		if(isRef()) {
			return mExpression;
		} else {
			if(mStrokeTypeName == null) {
				return "";
			}
	
			return String.format("(%s)%s", mStrokeTypeName, mExpression);
		}
	}

	public void setRange(String rangeExpression) {
		mRangeExpression = rangeExpression;
	}

	public String getRange() {
		return mRangeExpression;
	}

	public void setDbName(String dbName) {
		mDbName = dbName;
	}

	public String getDbName() {
		return mDbName;
	}

	public void setDbId(long id) {
		mDdId = id;
	}

	public long getDbId() {
		return mDdId;
	}

	public boolean isGroup() {
		return false;
	}

	public long getRefrenceId() {
		return getDbId();
	}

	public void setName(String name) {
		mName = name;
	}

	private List<Stroke> mRefStrokeList;
	public void setRefStrokeList(List<Stroke> refStrokeList) {
		mRefStrokeList = refStrokeList;
	}

	public List<Stroke> getRefStrokeList() {
		return mRefStrokeList;
	}

	public Path getPath() {
		Path path = new Path();
		if(isNormal()) {
			StrokeAction.drawPath(path, getExpression());
		} else if(isRef()) {
			List<Stroke> refStrokeList = getRefStrokeList();
			for(Stroke tmpStroke : refStrokeList) {
				if(tmpStroke.isNormal()) {
					StrokeAction.drawPath(path, tmpStroke.getExpression());
				}
			}
		}
		return path;
	}
}
