package idv.xrloong.qiangheng.tools.activity;

import idv.xrloong.qiangheng.tools.QHToolContent;
import idv.xrloong.qiangheng.tools.QHToolFactory;
import idv.xrloong.qiangheng.tools.R;
import idv.xrloong.qiangheng.tools.fragment.ItemListFragment;
import idv.xrloong.qiangheng.tools.util.Logger;
import android.app.Activity;
import android.app.Fragment;
import android.content.Intent;
import android.os.Bundle;

public class ItemListActivity extends Activity implements ItemListFragment.Callbacks {
	private static final String LOG_TAG = Logger.getLogTag(ItemListActivity.class);

	private boolean mTwoPane;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_item_list);

		if (findViewById(R.id.item_detail_container) != null) {
			mTwoPane = true;
			((ItemListFragment) getFragmentManager().findFragmentById(R.id.item_list)).setActivateOnItemClick(true);
		}
	}

	@Override
	public void onItemSelected(String id) {
		Logger.d(LOG_TAG, "onItemSelected %s", id);

		QHToolContent.QHToolType type = QHToolContent.QHToolType.valueOf(id);

		if (mTwoPane) {
			Fragment fragment = QHToolFactory.generateFagment(type);
			getFragmentManager().beginTransaction().replace(R.id.item_detail_container, fragment).commit();
		} else {
			Intent intent = QHToolFactory.generateInent(this, type);
			startActivity(intent);
		}
	}
}
