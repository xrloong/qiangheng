package idv.xrloong.qiangheng.tools.model;

import java.util.List;

public class DCEncoding {
	private StrokeGroup mStrokeGroup;
	private List<AddendumRange> mRangeList;

	public DCEncoding(StrokeGroup strokeGroup, List<AddendumRange> rangeList) {
		mStrokeGroup = strokeGroup;
		mRangeList = rangeList;
	}

	public StrokeGroup getStrokeGroup() {
		return mStrokeGroup;
	}

	public List<AddendumRange> getRangeList() {
		return mRangeList;
	}
}
