package idv.xrloong.qiangheng.tools.model;

import idv.xrloong.qiangheng.tools.view.IStrokeDrawable;
import idv.xrloong.qiangheng.tools.view.StrokeDrawableInfo;

import java.util.ArrayList;
import java.util.List;

import android.graphics.Path;

public class StrokeGroup implements IStrokeDrawable {

	private long mDbId = 0;
	private String mDbName;
	private String mName;

	private Geometry mGeometry;
	private List<Stroke> mStrokeList = new ArrayList<Stroke>();
	public StrokeGroup(List<Stroke> strokeList, Geometry geometry) {
		mStrokeList = strokeList;
		mGeometry = geometry;
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

	public Geometry getGeometry() {
		return mGeometry;
	}

	@Override
	public List<StrokeDrawableInfo> getInfoList() {
		List<StrokeDrawableInfo> strokeList = new ArrayList<StrokeDrawableInfo>();
		int colorIndex = 0;
		for(Stroke stroke : getStrokeList()) {
			Path path = stroke.getPath();
			int color = StrokeDrawableInfo.getNormalColor();
			if(stroke.isRef()) {
				color = StrokeDrawableInfo.getRefColor(colorIndex);
				colorIndex++;
			}

			StrokeDrawableInfo strokeDrawableInfo = new StrokeDrawableInfo(path, color);
			strokeDrawableInfo.setGeometry(new Geometry(stroke.getRange()));
			strokeList.add(strokeDrawableInfo);
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
