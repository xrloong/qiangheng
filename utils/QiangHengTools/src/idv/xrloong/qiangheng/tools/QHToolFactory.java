package idv.xrloong.qiangheng.tools;

import java.io.Serializable;

import idv.xrloong.qiangheng.tools.activity.FragmentActivity;
import idv.xrloong.qiangheng.tools.fragment.DecomposingExtentionBFragment;
import idv.xrloong.qiangheng.tools.fragment.FindCommonComponentFragment;
import idv.xrloong.qiangheng.tools.fragment.StrokeNamingFragment;
import idv.xrloong.qiangheng.tools.model.QHToolContent;
import idv.xrloong.qiangheng.tools.util.Logger;
import android.app.Fragment;
import android.content.Context;
import android.content.Intent;

public class QHToolFactory {
	private static final String LOG_TAG = Logger.getLogTag(QHToolFactory.class);

	private static String EXTRA_TOOL_ID = "EXTRA_TOOL_ID";

	public static Intent generateInent(Context context, QHToolContent.QHToolType type) {
		Intent intent = new Intent(context, FragmentActivity.class);
		intent.putExtra(EXTRA_TOOL_ID, type);

		return intent;
	}

	public static Fragment generateFragmentFromIntent(Intent intent) {
		Serializable serializable = intent.getSerializableExtra(EXTRA_TOOL_ID);

		QHToolContent.QHToolType type = QHToolContent.QHToolType.None;
		if(serializable instanceof QHToolContent.QHToolType) {
			type = (QHToolContent.QHToolType) serializable;
		} else {
			Logger.w(LOG_TAG, "parseIntent(): serializable is not the type QHToolContent.QHToolType.");
		}

		return generateFagment(type);
	}

	public static Fragment generateFagment(QHToolContent.QHToolType type) {
		Logger.i(LOG_TAG, "generateFagment() with type: %s", type);

		Fragment fragment = new Fragment();

		switch(type) {
		case NamingStroke:
			fragment = new StrokeNamingFragment();
			break;
		case FindingCommonComponent:
			fragment = new FindCommonComponentFragment();
			break;

		case DecomposingExtB:
			fragment = new DecomposingExtentionBFragment();
			break;

		default:
		case None:
			fragment = new Fragment();
			break;
		}

		return fragment;
	}
}
