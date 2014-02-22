package idv.xrloong.qiangheng.tools.activity;

import idv.xrloong.qiangheng.tools.QHToolFactory;
import idv.xrloong.qiangheng.tools.util.Logger;
import android.app.ActionBar;
import android.app.Activity;
import android.app.Fragment;
import android.os.Bundle;

public class FragmentActivity extends Activity {
	private static final String LOG_TAG = Logger.getLogTag(FragmentActivity.class);

	@Override
	public void onCreate(Bundle savedInstanceState) {
		Logger.d(LOG_TAG, "onCreate() +");

		super.onCreate(savedInstanceState);
        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowTitleEnabled(false);
        actionBar.setNavigationMode(ActionBar.NAVIGATION_MODE_LIST);

		Fragment fragment = QHToolFactory.generateFragmentFromIntent(getIntent());
		getFragmentManager().beginTransaction().add(android.R.id.content, fragment).commit();

		Logger.d(LOG_TAG, "onCreate() -");
	}
}
