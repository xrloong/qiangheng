package idv.xrloong.qiangheng.tools.fragment;

import idv.xrloong.qiangheng.tools.R;
import idv.xrloong.qiangheng.tools.FindCommonComponent.StrokeHelper;
import idv.xrloong.qiangheng.tools.model.DCCharacter;
import idv.xrloong.qiangheng.tools.model.DCData;
import idv.xrloong.qiangheng.tools.model.ReplaceStrokeGroup;
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
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class FindCommonComponentFragment extends Fragment {
	private static final String LOG_TAG = Logger.getLogTag(FindCommonComponentFragment.class);
	private StrokeControlView mControlView;
	private StrokeControlView mReplaceControlView;
	private IStrokeDrawable mOriginalStrokeGroup;
	private ReplaceStrokeGroup mReplaceStrokeGroup;

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
		mReplaceControlView = (StrokeControlView) rootView.findViewById(R.id.replace_stroke_control_view);
		mReplaceControlView.setOnIndexChangedListener(new StrokeControlView.OnIndexChangedListener() {
			@Override
			public void onJump(int index) {
				jumpToStrokeGroup(index);
			}
		});

		Button buttonUpdate = (Button) rootView.findViewById(R.id.button_update);
		buttonUpdate.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				EditText editText = (EditText) rootView.findViewById(R.id.edittext_replace_sequence);

				String sequence = editText.getText().toString();
				if(mReplaceStrokeGroup != null) {
					mReplaceStrokeGroup.setSequence(sequence);
				}

				StrokeView sv = (StrokeView) rootView.findViewById(R.id.stroke_view);
				sv.invalidate();
			}
		});
		Button buttonUpdateStrokeGroup = (Button) rootView.findViewById(R.id.button_update_stroke_group);
		buttonUpdateStrokeGroup.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				Context context = getActivity();

				EditText editText = (EditText) getView().findViewById(R.id.edittext_stroke_group);
				String strokeName = "$" + editText.getText().toString();
				int index = mReplaceControlView.getCurrentIndex() - 1;
				final StrokeGroup strokeGroup = StrokeHelper.queryStrokeGroup(context, strokeName, index);
				if(mReplaceStrokeGroup != null) {
					mReplaceStrokeGroup.setReplace(strokeGroup);
				}
				mReplaceControlView.findViewById(R.id.stroke_view).invalidate();
				mControlView.findViewById(R.id.stroke_view).invalidate();
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
			mOriginalStrokeGroup = StrokeHelper.queryStrokeGroup(context, groupingId);
			mReplaceStrokeGroup = new ReplaceStrokeGroup(mOriginalStrokeGroup);

			IStrokeViewController controller = new IStrokeViewController() {
				@Override
				public IStrokeDrawable getStrokeDrawable() {
					return mReplaceStrokeGroup;
				}
			};
			sv.setController(controller);
		}
	}

	private void jumpToStrokeGroup(int dataID){
		Context context = getActivity();

		EditText editText = (EditText) getView().findViewById(R.id.edittext_stroke_group);
		String strokeName = "$" + editText.getText().toString();
		int index = dataID -1;
		final StrokeGroup strokeGroup = StrokeHelper.queryStrokeGroup(context, strokeName, index);
		if(strokeGroup != null)
		{
			Logger.e(LOG_TAG, "XXXXXXXXXXXXXXXXXXXXXXXXXXXX AAAA");

/*
			TextView textDataID = (TextView) rootView.findViewById(R.id.data_id);
			TextView textCharacterName = (TextView) rootView.findViewById(R.id.character_name);

			textDataID.setText(String.format("%d", dataID));
			textCharacterName.setText(String.format("%s", characterName));
*/

			StrokeView sv = (StrokeView) mReplaceControlView.findViewById(R.id.stroke_view);

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
