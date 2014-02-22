package idv.xrloong.qiangheng.tools.fragment;

import idv.xrloong.qiangheng.tools.R;
import idv.xrloong.qiangheng.tools.FindCommonComponent.StrokeHelper;
import idv.xrloong.qiangheng.tools.model.DCCharacter;
import idv.xrloong.qiangheng.tools.model.DCData;
import idv.xrloong.qiangheng.tools.model.StrokeGroup;
import idv.xrloong.qiangheng.tools.model.StrokeTypeManager;
import idv.xrloong.qiangheng.tools.util.Logger;
import idv.xrloong.qiangheng.tools.view.IStrokeDrawable;
import idv.xrloong.qiangheng.tools.view.IStrokeViewController;
import idv.xrloong.qiangheng.tools.view.StrokeControlView;
import idv.xrloong.qiangheng.tools.view.StrokeView;
import android.app.Fragment;
import android.content.Context;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

public class FindCommonComponentFragment extends Fragment {
	private static final String LOG_TAG = Logger.getLogTag(FindCommonComponentFragment.class);
	private StrokeControlView mControlView;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		Logger.v(LOG_TAG, "onCreate() +");

		super.onCreate(savedInstanceState);

		StrokeTypeManager.getInstance().setupStrokeNameList();
		setHasOptionsMenu(true);

		Logger.v(LOG_TAG, "onCreate() -");
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		Logger.v(LOG_TAG, "onCreateView() +");

		final View rootView = inflater.inflate(R.layout.activity_find_common_component, container, false);
		mControlView = (StrokeControlView) rootView.findViewById(R.id.stroke_control_view);
		mControlView.setOnIndexChangedListener(new StrokeControlView.OnIndexChangedListener() {
			@Override
			public void onJump(int index) {
				jumpTo(index);
			}
		});

		Logger.v(LOG_TAG, "onCreateView() -");
		return rootView;
	}

	@Override
	public void onCreateOptionsMenu (Menu menu, MenuInflater inflater) {
		inflater.inflate(R.menu.naming_stroke, menu);
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		boolean bResult = false;

		switch(item.getItemId()) {
		case R.id.menu_item_read_description:
			bResult = true;
			fromFileToDb();
			break;

		case R.id.menu_item_write_description:
			bResult = true;
			fromDbToFile();
			break;

		default:
			bResult = false;
			break;
		}

		return bResult;
	}

	private void jumpTo(int dataID){
		Context context = getActivity();

		DCCharacter character = StrokeHelper.queryCharacter(context, dataID);
		View rootView = getView();

		if(character != null)
		{
			String characterName = character.getName();
																																																																																																																																																																																																																				
			TextView textDataID = (TextView) rootView.findViewById(R.id.data_id);
			TextView textCharacterName = (TextView) rootView.findViewById(R.id.character_name);

			textDataID.setText(String.format("%d", dataID));
			textCharacterName.setText(String.format("%s", characterName));

			StrokeView sv = (StrokeView) rootView.findViewById(R.id.stroke_view);

			long groupingId = character.getGroupingId();
			final StrokeGroup strokeGroup = StrokeHelper.queryStrokeGroup(context, groupingId);

			IStrokeViewController controller = new IStrokeViewController() {
				@Override
				public IStrokeDrawable getStrokeDrawable() {
					return strokeGroup;
				}
			};
			sv.setController(controller);
		}
	}

	private void fromFileToDb() {
		Context context = getActivity();

		DCData dcData = XmlReadWrite.parseAllData(context);
		StrokeHelper.insertDCData(context, dcData);
	}

	private void fromDbToFile() {
		Context context = getActivity();

		DCData dcData = StrokeHelper.queryDCData(context);
		XmlReadWrite.serializeAllData(context, dcData);
	}
}
