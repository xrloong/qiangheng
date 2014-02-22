package idv.xrloong.qiangheng.tools.model;

import idv.xrloong.qiangheng.tools.util.Logger;
import idv.xrloong.qiangheng.tools.view.IStrokeDrawable;
import idv.xrloong.qiangheng.tools.view.StrokeDrawableInfo;

import java.util.ArrayList;
import java.util.List;

public class ReplaceStrokeGroup implements IStrokeDrawable {
	private IStrokeDrawable mDrawable;
	private IStrokeDrawable mReplaceDrawable;
	private List<Integer> mSequence = new ArrayList<Integer>();

	public ReplaceStrokeGroup(IStrokeDrawable drawable) {
		mDrawable = drawable;
	}

	public void setSequence(String sequence) {
		mSequence.clear();

		for(String text : sequence.split(",")) {
			try {
				int index = Integer.parseInt(text)-1;
				mSequence.add(index);
			} catch (Exception e) {
			}
		}
	}

	public void setReplace(IStrokeDrawable replaceDrawable) {
		mReplaceDrawable = replaceDrawable;
		Logger.e("AAAAAAAAAAAA", "XXXXXXXXXXXXXXXXXXXXXXXXXX setReplace "+this+", "+replaceDrawable);
	}

	@Override
	public List<StrokeDrawableInfo> getInfoList() {
		Logger.e("AAAAAAAAAAAA", "XXXXXXXXXXXXXXXXXXX getInfoList "+this);
		if(mReplaceDrawable == null) {
			Logger.e("AAAAAAAAAAAA", "XXXXXXXXXXXXXXXXXXX SSSSSSSSSSSS");
			List<StrokeDrawableInfo> infoList = new ArrayList<StrokeDrawableInfo>(mDrawable.getInfoList());
			for(int index : mSequence) {
				infoList.get(index).setColor(StrokeDrawableInfo.getGuessColor());
			}
			return infoList;
		} else {
			Logger.e("AAAAAAAAAAAA", "XXXXXXXXXXXXXXXXXXX MMMMMMMM 1");
			List<StrokeDrawableInfo> infoList = new ArrayList<StrokeDrawableInfo>();
			int index = 0;
			for(StrokeDrawableInfo info : mDrawable.getInfoList()) {
				if(mSequence.contains(index)) {
				} else {
					infoList.add(info);
				}
				index ++;
			}
			Logger.e("AAAAAAAAAAAA", "XXXXXXXXXXXXXXXXXXX MMMMMMMM 2");
			if(mReplaceDrawable != null) {
				infoList.addAll(mReplaceDrawable.getInfoList());
			}
			return infoList;
		}

//		return infoList;
	}
}
