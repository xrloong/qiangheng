package idv.xrloong.qiangheng.tools.model;

import idv.xrloong.qiangheng.tools.view.IStrokeDrawable;

import java.util.ArrayList;
import java.util.List;

import android.graphics.Path;

public class StrokeGroup implements IStrokeDrawable {

	private long mDbId = 0;
	private String mDbName;
	private String mName;

	private List<Stroke> mStrokeList = new ArrayList<Stroke>();
	public StrokeGroup(List<Stroke> strokeList) {
		mStrokeList = strokeList;
	}

	public void setName(String name) {
		mName = name;
	}

	public String getName() {
		return mName;
	}

	public void setStrokeList(List<Stroke> strokeList) {
		mStrokeList = strokeList;
	}

	public List<Stroke> getStrokeList() {
		return mStrokeList;
	}

	@Override
	public List<Path> getPathList() {
		List<Path> strokeList = new ArrayList<Path>();
		for(Stroke stroke : getStrokeList()) {
			StrokeAction strokeAction = new StrokeAction(stroke.getExpression());
			List<Path> tmpPathList = strokeAction.getPathList();
			strokeList.addAll(tmpPathList);
		}
		return strokeList;
	}

	public void setDbName(String dbName) {
		mDbName = dbName;
	}

	public String getDbName() {
		return mDbName;
	}

	public void setDbId(long id) {
		mDbId = id;
	}

	public long getDbId() {
		return mDbId;
	}
}
