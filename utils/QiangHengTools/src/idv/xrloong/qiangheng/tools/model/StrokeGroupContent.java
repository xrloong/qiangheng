package idv.xrloong.qiangheng.tools.model;

public class StrokeGroupContent {

	private int mOrder;
	private long mStrokeGroupDbId;
	private long mStrokeDbId;

	public StrokeGroupContent(StrokeGroup strokeGroup, int order, Stroke stroke) {
		mStrokeGroupDbId = strokeGroup.getDbId();
		mStrokeDbId = stroke.getDbId();
		mOrder = order;
	}

	public int getOrder() {
		return mOrder;
	}

	public long getStrokGroupDbId() {
		return mStrokeGroupDbId;
	}

	public long getStrokDbId() {
		return mStrokeDbId;
	}
}
