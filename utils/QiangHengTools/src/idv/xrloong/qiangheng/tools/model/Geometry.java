package idv.xrloong.qiangheng.tools.model;

import junit.framework.Assert;
import android.graphics.Rect;

public class Geometry {

	private Rect mRect = new Rect();
	public Geometry(String description) {
		Assert.assertNotNull("The description should be non-null", description);
		Assert.assertEquals("The length of description should be 8", description.length(), 8);

		int left = Integer.parseInt(description.substring(0, 2), 16);
		int top = Integer.parseInt(description.substring(2, 4), 16);
		int right = Integer.parseInt(description.substring(4, 6), 16);
		int bottom = Integer.parseInt(description.substring(6, 8), 16);

		mRect.set(left, top, right, bottom);
	}

	Geometry(int left, int top, int right, int bottom) {
		mRect.set(left, top, right, bottom);
	}

	public int getLeft() {
		return mRect.left;
	}

	public int getTop() {
		return mRect.top;
	}

	public int getRight() {
		return mRect.right;
	}

	public int getBottom() {
		return mRect.bottom;
	}


	public String getExpression() {
		String expression = String.format("%02X%02X%02X%02X", getLeft(), getTop(), getRight(), getBottom());
		return expression;
	}
}
