package idv.xrloong.qiangheng.tools.view;

import idv.xrloong.qiangheng.tools.R;
import idv.xrloong.qiangheng.tools.fragment.FindCommonComponentFragment;
import idv.xrloong.qiangheng.tools.util.Logger;
import android.content.Context;
import android.util.AttributeSet;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;

public class StrokeControlView extends LinearLayout {
	private static final String LOG_TAG = Logger.getLogTag(FindCommonComponentFragment.class);

	public interface OnIndexChangedListener {
		public void onJump(int index);
	}
	private OnIndexChangedListener mOnIndexChangedListener;
	private int mCurrentDataID = 1;
	private EditText mEditTextDataID;

	public StrokeControlView(Context context) {
		this(context, null);
	}

	public StrokeControlView(Context context, AttributeSet attrs) {
		this(context, attrs, 0);
	}

	public StrokeControlView(Context context, AttributeSet attrs, int defStyle) {
		super(context, attrs, defStyle);
	}

	@Override
	protected void onFinishInflate() {
		super.onFinishInflate();

		Button buttonPreve = (Button) findViewById(R.id.button_prev);
		Button buttonNext = (Button) findViewById(R.id.button_next);
		Button buttonJump = (Button) findViewById(R.id.button_jump);
		mEditTextDataID = (EditText) findViewById(R.id.edittext_data_id);

		buttonPreve.setOnClickListener(new OnClickListener(){
			@Override
			public void onClick(View v) {
				Logger.d(LOG_TAG, "onClick() prev");
				jumpTo(mCurrentDataID-1);
			}
		});
		buttonNext.setOnClickListener(new OnClickListener(){
			@Override
			public void onClick(View v) {
				Logger.d(LOG_TAG, "onClick() next");
				jumpTo(mCurrentDataID+1);
			}
		});

		buttonJump.setOnClickListener(new OnClickListener(){
			@Override
			public void onClick(View v) {
				Logger.d(LOG_TAG, "onClick() jump");

				int dataID = getCurrentEditIndex();
				jumpTo(dataID);
			}
		});
	}

	private int getCurrentEditIndex() {
		String strDataID = mEditTextDataID.getText().toString();
		int dataId = Integer.parseInt(strDataID);

		return dataId;
	}

	public int getCurrentIndex() {
		return mCurrentDataID;
	}

	public void setOnIndexChangedListener(OnIndexChangedListener listener) {
		mOnIndexChangedListener = listener;
	}

	private void jumpTo(int index) {
		Logger.d(LOG_TAG, "jumpTo %d", index);

		mCurrentDataID = index;
		mEditTextDataID.setText(String.format("%d", mCurrentDataID));

		if (mOnIndexChangedListener != null) {
			mOnIndexChangedListener.onJump(index);
		}
	}
}
