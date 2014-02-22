package idv.xrloong.qiangheng.tools.model;

import idv.xrloong.qiangheng.tools.R;
import idv.xrloong.qiangheng.tools.util.Logger;

import java.util.ArrayList;
import java.util.List;

import junit.framework.Assert;

import android.content.Context;

public class QHToolContent {
	private static final String LOG_TAG = Logger.getLogTag(QHToolContent.class);

	public static enum QHToolType {
		None, NamingStroke, FindingCommonComponent, DecomposingExtB;

		public boolean isNamingStroke() {
			return NamingStroke.equals(this);
		}

		public boolean isFindingCommonComponent() {
			return FindingCommonComponent.equals(this);
		}
	};

	public static class QHToolItem {
		private String mTitle;
		private QHToolType mType;

		public QHToolItem(QHToolType type, String title) {
			this.mType = type;
			this.mTitle = title;
		}

		public String getId() {
			return mType.toString();
		}

		public String getTitle() {
			return mTitle;
		}

		@Override
		public String toString() {
			return mTitle;
		}
	}

	private static QHToolContent sInstance;

	private List<QHToolItem> ITEMS = new ArrayList<QHToolItem>();

	private QHToolContent(Context context) {
		init(context);
	}

	public static void initInstance(Context context) {
		Assert.assertNull("initInstance() is already called before.", sInstance);
		if(sInstance != null) {
			Logger.w(LOG_TAG, "initInstance() is already called before.");
		}

		sInstance = new QHToolContent(context);
	}

	public static QHToolContent getInstance() {
		Assert.assertNotNull("initInstance() is not yet called before.", sInstance);
		if(sInstance == null) {
			Logger.w(LOG_TAG, "initInstance() is not yet called before.");
		}

		return sInstance;
	}

	private void init(Context context) {
		ITEMS.add(new QHToolItem(QHToolType.NamingStroke, context.getString(R.string.tool_name_namming_stroking)));
		ITEMS.add(new QHToolItem(QHToolType.FindingCommonComponent, context.getString(R.string.tool_name_find_common_component)));
		ITEMS.add(new QHToolItem(QHToolType.DecomposingExtB, context.getString(R.string.tool_name_decompose_ext_b)));
	}

	public List<QHToolItem> getItems() {
		return ITEMS;
	}
}
