package idv.xrloong.qiangheng.tools.model;

import java.util.ArrayList;
import java.util.List;

public class DCCharacter {
	private String mName;
	private String mComment;
	private StrokeGroup mStrokeGroup;
	private long mDbId;
	private long mGroupingId;
	private List<AddendumRange> mAddonRangeList = new ArrayList<AddendumRange>();

	public DCCharacter(String name, String comment) {
		mName = name;
		mComment = comment;
	}

	public void setAddonRangeList(List<AddendumRange> rangeList) {
		mAddonRangeList = rangeList;
	}

	public List<AddendumRange> getAddendumRangeList() {
		return mAddonRangeList;
	}

	public void setStrokeGroup(StrokeGroup strokeGroup) {
		mStrokeGroup = strokeGroup;
	}

	public StrokeGroup getStrokeGroup() {
		return mStrokeGroup;
	}

	public String getName() {
		return mName;
	}

	public String getComment() {
		return mComment;
	}

	public void setDbId(long id) {
		mDbId = id;
	}

	public long getDbId() {
		return mDbId;
	}

	public void setGroupingId(long id) {
		mGroupingId = id;
	}

	public long getGroupingId() {
		return mGroupingId;
	}
}
