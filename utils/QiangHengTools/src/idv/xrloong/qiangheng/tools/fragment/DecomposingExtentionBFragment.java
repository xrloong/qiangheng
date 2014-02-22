package idv.xrloong.qiangheng.tools.fragment;

import idv.xrloong.qiangheng.tools.R;
import idv.xrloong.qiangheng.tools.model.CharacterDecomposition;
import idv.xrloong.qiangheng.tools.model.ExtentionBHelper;
import idv.xrloong.qiangheng.tools.model.OperatorManager;
import idv.xrloong.qiangheng.tools.util.Logger;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Reader;
import java.io.Writer;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import android.app.Fragment;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.os.Environment;
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
import android.widget.ImageView;
import android.widget.SimpleAdapter;
import android.widget.TextView;

public class DecomposingExtentionBFragment extends Fragment {
	private static final String LOG_TAG = Logger.getLogTag(DecomposingExtentionBFragment.class);
	private static final String CODE_CHART_DIR = Environment.getExternalStorageDirectory().getPath() + "/unicode/U20000/";
	private static final String FORMAT_CODE_CHART = "U%X.gif";
	private static final String FORMAT_CHARACTER_PATH = CODE_CHART_DIR + FORMAT_CODE_CHART;

	private int mCurrentCodePoint = 0x20000;
	private static final int CODE_POINT_START = 0x20000;
	private static final int CODE_POINT_END = 0x2A6D6;
	private static final int BASE = 16;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		Logger.v(LOG_TAG, "onCreate() +");

		super.onCreate(savedInstanceState);

		setHasOptionsMenu(true);

		Logger.v(LOG_TAG, "onCreate() -");
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		Logger.v(LOG_TAG, "onCreateView() +");

		final View rootView = inflater.inflate(R.layout.activity_decompose_ext_b, container, false);

		final EditText editText = (EditText) rootView.findViewById(R.id.edittext_data_id);
		editText.setText(String.format("%X", mCurrentCodePoint));


		Button buttonPreve = (Button) rootView.findViewById(R.id.button_prev);
		Button buttonNext = (Button) rootView.findViewById(R.id.button_next);
		Button buttonJump = (Button) rootView.findViewById(R.id.button_jump);

		buttonPreve.setOnClickListener(new OnClickListener(){
			@Override
			public void onClick(View v) {
				Logger.d(LOG_TAG, "onClick() prev");
				jumpTo(mCurrentCodePoint-1);
				doWork();
			}
		});
		buttonNext.setOnClickListener(new OnClickListener(){
			@Override
			public void onClick(View v) {
				Logger.d(LOG_TAG, "onClick() next");
				jumpTo(mCurrentCodePoint+1);
				doWork();
			}
		});

		buttonJump.setOnClickListener(new OnClickListener(){
			@Override
			public void onClick(View v) {
				Logger.d(LOG_TAG, "onClick() jump");
				String strCodePoint = editText.getText().toString();
				int codePoint = Integer.parseInt(strCodePoint, BASE);
				jumpTo(codePoint);

				doWork();
			}
		});

		Button buttonSave = (Button) rootView.findViewById(R.id.button_save);
		buttonSave.setOnClickListener(new OnClickListener(){
			@Override
			public void onClick(View v) {
				EditText editTextOperator = (EditText) rootView.findViewById(R.id.edittext_operator);
				EditText editTextOperand1 = (EditText) rootView.findViewById(R.id.edittext_operand_1);
				EditText editTextOperand2 = (EditText) rootView.findViewById(R.id.edittext_operand_2);
				EditText editTextOperand3 = (EditText) rootView.findViewById(R.id.edittext_operand_3);
				EditText editTextOperand4 = (EditText) rootView.findViewById(R.id.edittext_operand_4);

				OperatorManager operatorManger = OperatorManager.getInstance();

				int codePoint = mCurrentCodePoint;
				String operator = editTextOperator.getText().toString();

				int operandCount = operatorManger.getOperandCount(operator);
				String operand1 = editTextOperand1.getText().toString();
				String operand2 = editTextOperand2.getText().toString();
				String operand3 = editTextOperand3.getText().toString();
				String operand4 = editTextOperand4.getText().toString();

				CharacterDecomposition characterDecomposition = new CharacterDecomposition(codePoint, operator, operand1, operand2);
				switch(operandCount) {
				case 0:
					characterDecomposition = new CharacterDecomposition(codePoint, operator);
					break;
				case 1:
					characterDecomposition = new CharacterDecomposition(codePoint, operator, operand1);
					break;
				case 2:
					characterDecomposition = new CharacterDecomposition(codePoint, operator, operand1, operand2);
					break;
				case 3:
					characterDecomposition = new CharacterDecomposition(codePoint, operator, operand1, operand2, operand3);
					break;
				case 4:
					characterDecomposition = new CharacterDecomposition(codePoint, operator, operand1, operand2, operand3, operand4);
					break;
				}
				ExtentionBHelper.updateCodePoint(getActivity(), characterDecomposition);
			}
		});

		GridView gv = (GridView) rootView.findViewById(R.id.gridView);
		SimpleAdapter adpater = getStrokeNameAdapter();
		gv.setAdapter(adpater);
		gv.setOnItemClickListener(new AdapterView.OnItemClickListener() {
			@Override
			public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
				TextView textView = (TextView)view.findViewById(android.R.id.text1);
				String operatorName = textView.getText().toString();

				EditText editTextOperator = (EditText) rootView.findViewById(R.id.edittext_operator);
				editTextOperator.setText(operatorName);

				int operandCount = OperatorManager.getInstance().getOperandCount(operatorName);
				updateOperandView(operandCount);
			}
		});

		Button buttonApply = (Button) rootView.findViewById(R.id.button_apply);
		buttonApply.setOnClickListener(new OnClickListener(){

			@Override
			public void onClick(View v) {
				EditText editTextTmpCharacter = (EditText) rootView.findViewById(R.id.edittext_tmp_character);
				String tmpCharacter = editTextTmpCharacter.getText().toString();

				EditText editTextApplyIndex = (EditText) rootView.findViewById(R.id.edittext_apply_index);
				String applyIndex = editTextApplyIndex.getText().toString();
				int index = Integer.parseInt(applyIndex);

				EditText editTextOperand1 = (EditText) rootView.findViewById(R.id.edittext_operand_1);
				EditText editTextOperand2 = (EditText) rootView.findViewById(R.id.edittext_operand_2);
				EditText editTextOperand3 = (EditText) rootView.findViewById(R.id.edittext_operand_3);
				EditText editTextOperand4 = (EditText) rootView.findViewById(R.id.edittext_operand_4);

				switch(index) {
				case 1:
					editTextOperand1.setText(tmpCharacter);
					break;
				case 2:
					editTextOperand2.setText(tmpCharacter);
					break;
				case 3:
					editTextOperand3.setText(tmpCharacter);
					break;
				case 4:
					editTextOperand4.setText(tmpCharacter);
					break;
				}

			}
		});

		return rootView;
	}


	@Override
	public void onCreateOptionsMenu (Menu menu, MenuInflater inflater) {
		inflater.inflate(R.menu.decomposing_ext_b, menu);
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		boolean bResult = false;

		switch(item.getItemId()) {
		case R.id.menu_item_write_txt_ext_b:
			generateTxt(getActivity());
			bResult = true;
			break;

		case R.id.menu_item_read_txt_ext_b:
			readTxt(getActivity());
			bResult = true;
			break;

		default:
			bResult = false;
			break;
		}

		return bResult;
	}

	private void jumpTo(int index) {
		Logger.d(LOG_TAG, "jumpTo %d", index);

		if(index < CODE_POINT_START) {
			index = CODE_POINT_START;
		}

		if(index > CODE_POINT_END) {
			index = CODE_POINT_END;
		}

		mCurrentCodePoint = index;
		View rootView = this.getView();
		EditText editText = (EditText) rootView.findViewById(R.id.edittext_data_id);
		editText.setText(String.format("%X", mCurrentCodePoint));
	}

	private void doWork() {
		String fileName = String.format(FORMAT_CHARACTER_PATH, mCurrentCodePoint);

		Bitmap bitmap = BitmapFactory.decodeFile(fileName);

		ImageView characterView = (ImageView) getView().findViewById(R.id.character_view);
		characterView.setImageBitmap(bitmap);


		int codePoint = mCurrentCodePoint;
		CharacterDecomposition characterDecomposition = ExtentionBHelper.query(getActivity(), codePoint);

		View rootView = getView();
		EditText editTextOperator = (EditText) rootView.findViewById(R.id.edittext_operator);
		EditText editTextOperand1 = (EditText) rootView.findViewById(R.id.edittext_operand_1);
		EditText editTextOperand2 = (EditText) rootView.findViewById(R.id.edittext_operand_2);
		EditText editTextOperand3 = (EditText) rootView.findViewById(R.id.edittext_operand_3);
		EditText editTextOperand4 = (EditText) rootView.findViewById(R.id.edittext_operand_4);

		editTextOperator.setText(characterDecomposition.getOperator());
		editTextOperand1.setText(characterDecomposition.getOperand1());
		editTextOperand2.setText(characterDecomposition.getOperand2());
		editTextOperand3.setText(characterDecomposition.getOperand3());
		editTextOperand4.setText(characterDecomposition.getOperand4());

		int operandCount = characterDecomposition.getOperandCount();
		updateOperandView(operandCount);
	}

	private void updateOperandView(int operandCount) {
		View rootView = getView();

		EditText editTextOperand1 = (EditText) rootView.findViewById(R.id.edittext_operand_1);
		EditText editTextOperand2 = (EditText) rootView.findViewById(R.id.edittext_operand_2);
		EditText editTextOperand3 = (EditText) rootView.findViewById(R.id.edittext_operand_3);
		EditText editTextOperand4 = (EditText) rootView.findViewById(R.id.edittext_operand_4);

		editTextOperand1.setVisibility(operandCount >= 1 ? View.VISIBLE : View.INVISIBLE);
		editTextOperand2.setVisibility(operandCount >= 2 ? View.VISIBLE : View.INVISIBLE);
		editTextOperand3.setVisibility(operandCount >= 3 ? View.VISIBLE : View.INVISIBLE);
		editTextOperand4.setVisibility(operandCount >= 4 ? View.VISIBLE : View.INVISIBLE);
	}

	private SimpleAdapter getStrokeNameAdapter() {
		List<String> operatorNameList = new ArrayList<String>();
		List<String> tmpOperatorNameList = OperatorManager.getInstance().getOperatorNameList();
		operatorNameList.addAll(tmpOperatorNameList);

		String operatorNames[] = operatorNameList.toArray(new String[0]);

		Context context = getActivity();
		String dataFieldOperatorName = "operatorName";
		List<HashMap<String, String>> data = new ArrayList<HashMap<String, String>>();

		for(String name:operatorNames)
		{
			HashMap<String, String> m = new HashMap<String, String>();
			m.put(dataFieldOperatorName, name);
			data.add(m);
		}

		SimpleAdapter adpater = new SimpleAdapter(context, data,
				android.R.layout.simple_list_item_1,
				new String[] { dataFieldOperatorName },
				new int[] { android.R.id.text1 });
		return adpater;
	}

	private void generateTxt(Context context) {
		File file = new File(context.getExternalFilesDir(null), "output_ext_b.txt");
        try {
			FileWriter fileWriter = new FileWriter(file);
			generateTxt(fileWriter);
			fileWriter.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private void generateTxt(Writer writer) {
		List<CharacterDecomposition> characterDecompositionList = ExtentionBHelper.queryAll(getActivity());

		for(CharacterDecomposition characterDecomposition : characterDecompositionList) {
			int codePoint = characterDecomposition.getCodePoint();
			String operator = characterDecomposition.getOperator();
			int operandCount = OperatorManager.getInstance().getOperandCount(operator);
			String operand1 = characterDecomposition.getOperand1();
			String operand2 = characterDecomposition.getOperand2();
			String operand3 = characterDecomposition.getOperand3();
			String operand4 = characterDecomposition.getOperand4();

			try {
				switch(operandCount) {
				case 0:
					writer.append(String.format("%X\t%s\n", codePoint, operator));
					break;
				case 1:
					writer.append(String.format("%X\t%s\t%s\n", codePoint, operator, operand1));
					break;
				case 2:
					writer.append(String.format("%X\t%s\t%s\t%s\n", codePoint, operator, operand1, operand2));
					break;
				case 3:
					writer.append(String.format("%X\t%s\t%s\t%s\t%s\n", codePoint, operator, operand1, operand2, operand3));
					break;
				case 4:
					writer.append(String.format("%X\t%s\t%s\t%s\t%s\t%s\n", codePoint, operator, operand1, operand2, operand3, operand4));
					break;
				}
//				writer.append(String.format("%X\t%s\t%s\t%s\n", codePoint, operator, operand1, operand2));
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	private void readTxt(Context context) {
		File file = new File(context.getExternalFilesDir(null), "input_ext_b.txt");
        try {
			FileReader fileReader = new FileReader(file);
			readTxt(fileReader);
			fileReader.close();
		} catch (IOException e) {
			e.printStackTrace();
		}

        
	}

	private void readTxt(Reader reader) {
		BufferedReader bfReader = new BufferedReader(reader);

		String line = null;
		try {
			line = bfReader.readLine();
		} catch (IOException e) {
			e.printStackTrace();
		}

		List<CharacterDecomposition> characterDecompositionList = new ArrayList<CharacterDecomposition>();
		for(; line != null;) {
			String[] tokenList = line.split("\t");

			int codePoint = Integer.parseInt(tokenList[0], BASE);
			String operatorName = tokenList[1];
			int operandCount = OperatorManager.getInstance().getOperandCount(operatorName);
			String operand1 = null;
			String operand2 = null;
			String operand3 = null;
			String operand4 = null;
			if(tokenList.length > 2) {
				operand1 = tokenList[2];
			}
			if(tokenList.length > 3) {
				operand2 = tokenList[3];
			}
			if(tokenList.length > 4) {
				operand3 = tokenList[4];
			}
			if(tokenList.length > 5) {
				operand4 = tokenList[5];
			}

			CharacterDecomposition characterDecomposition = null;
			switch(operandCount) {
			case 0:
				characterDecomposition = new CharacterDecomposition(codePoint, operatorName);
				break;
			case 1:
				characterDecomposition = new CharacterDecomposition(codePoint, operatorName, operand1);
				break;
			case 2:
				characterDecomposition = new CharacterDecomposition(codePoint, operatorName, operand1, operand2);
				break;
			case 3:
				characterDecomposition = new CharacterDecomposition(codePoint, operatorName, operand1, operand2, operand3);
				break;
			case 4:
				characterDecomposition = new CharacterDecomposition(codePoint, operatorName, operand1, operand2, operand3, operand4);
				break;
			}

			characterDecompositionList.add(characterDecomposition);
			try {
				line = bfReader.readLine();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}

		ExtentionBHelper.insertList(getActivity(), characterDecompositionList);
	}
}
