package idv.xrloong.qiangheng.tools.view;

import java.util.List;

public interface IStrokeDrawable {
	public final static int MAX_WIDTH = 256;
	public final static int MAX_HEIGHT = 256;

	public List<StrokeDrawableInfo> getInfoList();
}
