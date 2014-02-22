package idv.xrloong.qiangheng.tools.fragment;

import idv.xrloong.qiangheng.tools.R;
import idv.xrloong.qiangheng.tools.StrokeNaming.StrokeActionHelper;
import idv.xrloong.qiangheng.tools.StrokeNaming.StrokeItem;
import idv.xrloong.qiangheng.tools.util.Logger;
import idv.xrloong.qiangheng.tools.view.StrokeView;
import idv.xrloong.qiangheng.tools.widget.Stroke;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import android.app.Fragment;
import android.content.Context;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.GridView;
import android.widget.SimpleAdapter;
import android.widget.TextView;

public class StrokeNamingFragment extends Fragment {
	private static final String LOG_TAG = Logger.getLogTag(StrokeNamingFragment.class);
	private int mCurrentDataID=1;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);

		setHasOptionsMenu(true);
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		Logger.v(LOG_TAG, "onCreateView()");

		final View rootView = inflater.inflate(R.layout.activity_naming_stroke, container, false);

		Button buttonPreve = (Button) rootView.findViewById(R.id.button_prev);
		Button buttonNext = (Button) rootView.findViewById(R.id.button_next);
		Button buttonJump = (Button) rootView.findViewById(R.id.button_jump);
		buttonPreve.setOnClickListener(new OnClickListener(){
			@Override
			public void onClick(View v) {
				jumpTo(mCurrentDataID-1);
			}
		});
		buttonNext.setOnClickListener(new OnClickListener(){
			@Override
			public void onClick(View v) {
				jumpTo(mCurrentDataID+1);
			}
		});

		buttonJump.setOnClickListener(new OnClickListener(){
			@Override
			public void onClick(View v) {
				EditText editTextDataID = (EditText) rootView.findViewById(R.id.edittext_data_id);
				String strDataID = editTextDataID.getText().toString();
				int dataID=Integer.parseInt(strDataID);
				jumpTo(dataID);
			}
		});


		GridView gv = (GridView) rootView.findViewById(R.id.gridView);
		SimpleAdapter adpater = getStrokeNameAdapter();
		gv.setAdapter(adpater);
		gv.setOnItemClickListener(new AdapterView.OnItemClickListener() {
			@Override
			public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
				// TODO Auto-generated method stub
				Context context = getActivity();
				TextView textView = (TextView)view.findViewById(android.R.id.text1);
				String strokeName = textView.getText().toString();
				StrokeActionHelper.update(context, mCurrentDataID, strokeName);
				jumpTo(mCurrentDataID);
			}
		});

		mCurrentDataID = 1;

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

			insertAllData();
			break;

		case R.id.menu_item_write_description:
			bResult = true;

			writeAllData();
			break;

		default:
			bResult = false;
			break;
		}

		return bResult;
	}

	private void jumpTo(int dataID){
		Context context = getActivity();
		StrokeItem item = StrokeActionHelper.query(context, dataID);
		View rootView = getView();

		if(item!=null)
		{
			mCurrentDataID = dataID;
			String characterName = item.charName;
			String strokeName = item.strokeName;
			int strokeNo = item.strokeNo;
			String description = item.strokeDescription;
	
			TextView textDataID = (TextView) rootView.findViewById(R.id.data_id);
			TextView textCharacterName = (TextView) rootView.findViewById(R.id.character_name);
			TextView textStrokeName = (TextView) rootView.findViewById(R.id.stroke_name);
			TextView textStrokeNo = (TextView) rootView.findViewById(R.id.stroke_no);
			EditText editTextDataID = (EditText) rootView.findViewById(R.id.edittext_data_id);

			textDataID.setText(String.format("%d", dataID));
			editTextDataID.setText(String.format("%d", dataID));
			textCharacterName.setText(String.format("%s", characterName));
			textStrokeName.setText(String.format("%s", strokeName));
			textStrokeNo.setText(String.format("%d", strokeNo));

			Stroke s = new Stroke(description);
			StrokeView sv = (StrokeView) rootView.findViewById(R.id.stroke_view);
			sv.setStroke(s);
		}
	}

	private void insertAllData() {
		Context context = getActivity();
		InputStream is;
		char buffers[]=new char[300000];
		String content = null;
		try {
			File file = new File(context.getExternalFilesDir(null), "input_descriptions.txt");

			is = new FileInputStream(file);
			InputStreamReader isr = new InputStreamReader(is, "UTF-8");
			int count=isr.read(buffers);

			content = String.format("%s", String.valueOf(buffers, 0, count));
		} catch (IOException e) {
			e.printStackTrace();
		}

		String lines[]=content.split("\n");
		List<StrokeItem> itemList=new ArrayList<StrokeItem>();
		for(String line: lines){
			String splitions[]=line.split("\t");
			String charName=splitions[0];
			int strokeNo=Integer.parseInt(splitions[1]);
			String strokeDescription=splitions[2];
			String strokeName=splitions[3];

			StrokeItem strokeItem = new StrokeItem(charName, strokeNo, strokeDescription, strokeName);
			itemList.add(strokeItem);
		}
		StrokeActionHelper.bulkInsert(context, itemList);
	}

	private void writeAllData() {
		Context context = getActivity();
		List<StrokeItem> strokes = StrokeActionHelper.query(context);

		try {
			File file = new File(context.getExternalFilesDir(null), "output_descriptions.txt");

			FileOutputStream fos = new FileOutputStream(file);
			String format = "%s\t%d\t%s\t%s\n";
			for(StrokeItem stroke : strokes) {
				String line = String.format(format, stroke.charName, stroke.strokeNo, stroke.strokeDescription, stroke.strokeName);
				fos.write(line.getBytes());
			}
			fos.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private SimpleAdapter getStrokeNameAdapter() {
		String strokeNames[] = { "XXXX",

		"點", "長頓點",

		"橫", "橫鉤", "橫折", "橫折橫", "橫折鉤", "橫撇", "橫曲鉤", "橫撇橫折鉤", "橫斜鉤", "橫折橫折",

		"豎", "豎折", "豎挑", "豎橫折", "豎橫折鉤", "豎曲鉤", "豎鉤", "臥鉤", "斜鉤", "彎鉤",

		"撇", "撇頓點", "撇橫", "撇挑", "撇折", "豎撇", "挑", "挑折", "捺",

		"圓" };

		Context context = getActivity();
		String dataFieldStrokeName = "strokeName";
		List<HashMap<String, String>> data = new ArrayList<HashMap<String, String>>();

		for(String name:strokeNames)
		{
			HashMap<String, String> m = new HashMap<String, String>();
			m.put(dataFieldStrokeName, name);
			data.add(m);
		}

		SimpleAdapter adpater = new SimpleAdapter(context, data,
				android.R.layout.simple_list_item_1,
				new String[] { dataFieldStrokeName },
				new int[] { android.R.id.text1 });
		return adpater;
	}
}
