package idv.xrloong.qiangheng.tools.model;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import idv.xrloong.qiangheng.tools.FindCommonComponent.StrokeHelper;
import idv.xrloong.qiangheng.tools.util.Logger;
import junit.framework.Assert;
import android.content.Context;

public class StrokeTypeManager {
	private static final String LOG_TAG = Logger.getLogTag(StrokeTypeManager.class);

	List<String> mStrokeNameList = new ArrayList<String>();
	{
		mStrokeNameList.add("多筆劃");

		mStrokeNameList.add("點");
		mStrokeNameList.add("長頓點");

		mStrokeNameList.add("橫");
		mStrokeNameList.add("橫鉤");
		mStrokeNameList.add("橫折");
		mStrokeNameList.add("橫折橫");
		mStrokeNameList.add("橫折鉤");
		mStrokeNameList.add("橫撇");
		mStrokeNameList.add("橫曲鉤");
		mStrokeNameList.add("橫撇橫折鉤");
		mStrokeNameList.add("橫斜鉤");
		mStrokeNameList.add("橫折橫折");

		mStrokeNameList.add("豎");
		mStrokeNameList.add("豎折");
		mStrokeNameList.add("豎挑");
		mStrokeNameList.add("豎橫折");
		mStrokeNameList.add("豎橫折鉤");
		mStrokeNameList.add("豎曲鉤");
		mStrokeNameList.add("豎鉤");
		mStrokeNameList.add("臥鉤");
		mStrokeNameList.add("斜鉤");
		mStrokeNameList.add("彎鉤");

		mStrokeNameList.add("撇");
		mStrokeNameList.add("撇頓點");
		mStrokeNameList.add("撇橫");
		mStrokeNameList.add("撇挑");
		mStrokeNameList.add("撇折");
		mStrokeNameList.add("豎撇");
		mStrokeNameList.add("挑");
		mStrokeNameList.add("挑折");
		mStrokeNameList.add("捺");

		mStrokeNameList.add("挑捺");
		mStrokeNameList.add("橫捺");

		mStrokeNameList.add("圓");
	}

	private static StrokeTypeManager sInstance;
	public static void initInstance(Context context) {
		Assert.assertNull("initInstance() is already called before.", sInstance);
		if(sInstance != null) {
			Logger.w(LOG_TAG, "initInstance() is already called before.");
		}

		sInstance = new StrokeTypeManager(context);
	}

	public static StrokeTypeManager getInstance() {
		Assert.assertNotNull("initInstance() is not yet called before.", sInstance);
		if(sInstance == null) {
			Logger.w(LOG_TAG, "initInstance() is not yet called before.");
		}

		return sInstance;
	}

	private Context mContext;
	private StrokeTypeManager(Context context) {
		mContext = context;
	}

	public List<String> getStrokeNameList() {
		return mStrokeNameList;
	}

	private Map<String, Long> mMapId = new HashMap<String, Long>();
	public void setupStrokeNameList() {
		StrokeHelper.insertAllStrokeTypes(mContext);
		List<StrokeType> strokeTypeList = StrokeHelper.queryAllStrokeTypes(mContext);
		for(StrokeType type : strokeTypeList) {
			mMapId.put(type.getName(), type.getDBID());
		}
	}

	public long getTypeId(String name) {
		return mMapId.get(name);
	}

	public String getTypeName(long id) {
		return mStrokeNameList.get((int) id);
	}
}
