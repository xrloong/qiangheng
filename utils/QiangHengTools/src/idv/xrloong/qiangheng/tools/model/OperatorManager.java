package idv.xrloong.qiangheng.tools.model;

import idv.xrloong.qiangheng.tools.util.Logger;

import java.util.ArrayList;
import java.util.List;

import junit.framework.Assert;
import android.content.Context;

public class OperatorManager {
	private static final String LOG_TAG = Logger.getLogTag(StrokeTypeManager.class);

	List<OperatorInfo> mOperatorList = new ArrayList<OperatorInfo>();
	{
		mOperatorList.add(new OperatorInfo("XXXX", 0));
		mOperatorList.add(new OperatorInfo("龜", 0));

		mOperatorList.add(new OperatorInfo("範好"));
		mOperatorList.add(new OperatorInfo("範志"));

		mOperatorList.add(new OperatorInfo("範起"));
		mOperatorList.add(new OperatorInfo("範這"));
		mOperatorList.add(new OperatorInfo("範廖"));
		mOperatorList.add(new OperatorInfo("範載"));
		mOperatorList.add(new OperatorInfo("範斗"));

		mOperatorList.add(new OperatorInfo("範回"));
		mOperatorList.add(new OperatorInfo("範同"));
		mOperatorList.add(new OperatorInfo("範函"));
		mOperatorList.add(new OperatorInfo("範區"));
		mOperatorList.add(new OperatorInfo("範左"));

		mOperatorList.add(new OperatorInfo("範衍"));
		mOperatorList.add(new OperatorInfo("範衷"));
		mOperatorList.add(new OperatorInfo("範句"));


		mOperatorList.add(new OperatorInfo("範林", 1));
		mOperatorList.add(new OperatorInfo("範圭", 1));
		mOperatorList.add(new OperatorInfo("範㴇", 1));
		mOperatorList.add(new OperatorInfo("範鑫", 1));
		mOperatorList.add(new OperatorInfo("範燚", 1));

		mOperatorList.add(new OperatorInfo("範霜", 3));
		mOperatorList.add(new OperatorInfo("範想", 3));
		mOperatorList.add(new OperatorInfo("範怡", 3));
		mOperatorList.add(new OperatorInfo("範韻", 3));

		mOperatorList.add(new OperatorInfo("範算", 3));
		mOperatorList.add(new OperatorInfo("範湘", 3));
		mOperatorList.add(new OperatorInfo("範纂", 4));
		mOperatorList.add(new OperatorInfo("範膷", 4));
//		mOperatorList.add(new OperatorInfo("範舝", 5));

		mOperatorList.add(new OperatorInfo("範粦", 3));
		mOperatorList.add(new OperatorInfo("範瓥", 4));

		mOperatorList.add(new OperatorInfo("範㘴", 3));
		mOperatorList.add(new OperatorInfo("範畞", 3));
		mOperatorList.add(new OperatorInfo("範幽", 3));
		mOperatorList.add(new OperatorInfo("範㒳", 3));
		mOperatorList.add(new OperatorInfo("範夾", 3));

		mOperatorList.add(new OperatorInfo("範聖"));
		mOperatorList.add(new OperatorInfo("範燞"));
		mOperatorList.add(new OperatorInfo("範薤"));
		mOperatorList.add(new OperatorInfo("範簸"));

		mOperatorList.add(new OperatorInfo("範敫"));
		mOperatorList.add(new OperatorInfo("範類"));
		mOperatorList.add(new OperatorInfo("範碋"));
		mOperatorList.add(new OperatorInfo("範璳"));

		mOperatorList.add(new OperatorInfo("範搻"));
		mOperatorList.add(new OperatorInfo("範瞿"));
		mOperatorList.add(new OperatorInfo("範徰"));
		mOperatorList.add(new OperatorInfo("範贁"));

		mOperatorList.add(new OperatorInfo("範䜌"));
		mOperatorList.add(new OperatorInfo("範辦"));
	}

	private static OperatorManager sInstance;
	public static void initInstance(Context context) {
		Assert.assertNull("initInstance() is already called before.", sInstance);
		if(sInstance != null) {
			Logger.w(LOG_TAG, "initInstance() is already called before.");
		}

		sInstance = new OperatorManager();
	}

	public static OperatorManager getInstance() {
		Assert.assertNotNull("initInstance() is not yet called before.", sInstance);
		if(sInstance == null) {
			Logger.w(LOG_TAG, "initInstance() is not yet called before.");
		}

		return sInstance;
	}

	public List<String> getOperatorNameList() {
		List<String> operatorNameList = new ArrayList<String>();
		for(OperatorInfo operatorInfo : mOperatorList) {
			operatorNameList.add(operatorInfo.getName());
		}

		return operatorNameList;
	}

	public int getOperandCount(String operatorName) {
		int operandCount = 0;
		for(OperatorInfo operator : mOperatorList) {
			if(operatorName.equals(operator.getName())) {
				operandCount = operator.getOperandCount();
			}
		}

		return operandCount;
	}

	static class OperatorInfo {
		private String mName;
		private int mOperandCount;

		OperatorInfo(String name) {
			this(name, 2);
		}

		OperatorInfo(String name, int operandCount) {
			mName = name;
			mOperandCount = operandCount;
		}

		String getName() {
			return mName;
		}

		int getOperandCount() {
			return mOperandCount;
		}
	}
}
