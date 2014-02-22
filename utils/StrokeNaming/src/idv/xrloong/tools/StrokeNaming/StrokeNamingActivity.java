package idv.xrloong.tools.StrokeNaming;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.GridView;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.TextView;

public class StrokeNamingActivity extends Activity {
	/** Called when the activity is first created. */

	private int mCurrentDataID=1;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.main);


		Button buttonPreve = (Button) findViewById(R.id.button_prev);
		Button buttonNext = (Button) findViewById(R.id.button_next);
		Button buttonJump = (Button) findViewById(R.id.button_jump);
		buttonPreve.setOnClickListener(new OnClickListener(){

			@Override
			public void onClick(View v) {
				// TODO Auto-generated method stub
				jumpTo(mCurrentDataID-1);
			}
			
		});
		buttonNext.setOnClickListener(new OnClickListener(){

			@Override
			public void onClick(View v) {
				// TODO Auto-generated method stub
				jumpTo(mCurrentDataID+1);

			}
			
		});

		buttonJump.setOnClickListener(new OnClickListener(){

			@Override
			public void onClick(View v) {
				// TODO Auto-generated method stub
				EditText editTextDataID = (EditText)findViewById(R.id.edittext_data_id);
				String strDataID = editTextDataID.getText().toString();
				int dataID=Integer.parseInt(strDataID);
				jumpTo(dataID);

			}
			
		});


		GridView gv = (GridView) findViewById(R.id.gridView);
		SimpleAdapter adpater = getStrokeNameAdapter();
		gv.setAdapter(adpater);
		gv.setOnItemClickListener(new AdapterView.OnItemClickListener() {

			@Override
			public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
				// TODO Auto-generated method stub
				TextView textView = (TextView)view.findViewById(android.R.id.text1);
				String strokeName = textView.getText().toString();
				StrokeActionHelper.update(StrokeNamingActivity.this, mCurrentDataID, strokeName);
				jumpTo(mCurrentDataID);
			}
		});

		mCurrentDataID = 1;

		
		jumpTo(1);
//		StrokeActionHelper.update(this, 1, "ABCD");
//		insertAllData();
	}

	private void jumpTo(int dataID){
		StrokeItem item = StrokeActionHelper.query(this, dataID);

		if(item!=null)
		{
			mCurrentDataID = dataID;
			String characterName = item.charName;
			String strokeName = item.strokeName;
			int strokeNo = item.strokeNo;
			String description = item.strokeDescription;
	
			TextView textDataID = (TextView) findViewById(R.id.data_id);
			TextView textCharacterName = (TextView) findViewById(R.id.character_name);
			TextView textStrokeName = (TextView) findViewById(R.id.stroke_name);
			TextView textStrokeNo = (TextView) findViewById(R.id.stroke_no);
			EditText editTextDataID = (EditText)findViewById(R.id.edittext_data_id);

			textDataID.setText(String.format("%d", dataID));
			editTextDataID.setText(String.format("%d", dataID));
			textCharacterName.setText(String.format("%s", characterName));
			textStrokeName.setText(String.format("%s", strokeName));
			textStrokeNo.setText(String.format("%d", strokeNo));

			Stroke s = new Stroke(description);
			StrokeView sv = (StrokeView) findViewById(R.id.stroke_view);
			sv.setStroke(s);
		}
	}

	private void insertAllData() {
		InputStream is;
		char buffers[]=new char[300000];
		String content = null;
		try {
			is = this.getAssets().open("descriptions.txt");
			InputStreamReader isr = new InputStreamReader(is, "UTF-8");
			int count=isr.read(buffers);

			content = String.format("%s", String.valueOf(buffers, 0, count));
		} catch (IOException e) {
			// TODO Auto-generated catch block
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
		StrokeActionHelper.bulkInsert(this, itemList);
	}

	private SimpleAdapter getStrokeNameAdapter() {
		String strokeNames[] = { "XXXX",

		"點", "長頓點",

		"橫", "橫鉤", "橫折", "橫折橫", "橫折鉤", "橫撇", "橫曲鉤", "橫撇橫折鉤", "橫斜鉤", "橫折橫折",

		"豎", "豎折", "豎挑", "豎橫折", "豎橫折鉤", "豎曲鉤", "豎鉤", "臥鉤", "斜鉤", "彎鉤",

		"撇", "撇頓點", "撇橫", "撇挑", "撇折", "豎撇", "挑", "挑折", "捺",

		"圓" };

		String dataFieldStrokeName = "strokeName";
		List<HashMap<String, String>> data = new ArrayList<HashMap<String, String>>();

		for(String name:strokeNames)
		{
			HashMap<String, String> m = new HashMap<String, String>();
			m.put(dataFieldStrokeName, name);
			data.add(m);
		}

		SimpleAdapter adpater = new SimpleAdapter(this, data,
				android.R.layout.simple_list_item_1,
				new String[] { dataFieldStrokeName },
				new int[] { android.R.id.text1 });
		return adpater;
	}
}