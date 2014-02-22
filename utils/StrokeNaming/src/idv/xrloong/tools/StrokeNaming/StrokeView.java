package idv.xrloong.tools.StrokeNaming;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Path;
import android.util.AttributeSet;
import android.util.Log;
import android.view.View;

public class StrokeView extends View {

	private Stroke mStroke;
	private Paint mPaintStroke;
	private Paint paintBoundry;

	public StrokeView(Context context, AttributeSet attrs) {
		super(context, attrs);
		// TODO Auto-generated constructor stub

		initBoundaryPaint();
		initStrokePaint();
	}

	public void clear() {
		mStroke = null;
	}

	public void setStroke(Stroke stroke) {
		Log.e("XXXXXXXXXXx", "setStroke() +");
		mStroke = stroke;
		this.invalidate();
	}

	@Override
	public void onDraw(Canvas canvas) {
		int width = this.getWidth();
		int height = this.getHeight();
		int left = 0;
		int top = 0;
		int right = width;
		int bottom = height;
		canvas.drawLine(left, top, right, top, paintBoundry);
		canvas.drawLine(left, bottom, right, bottom, paintBoundry);
		canvas.drawLine(left, top, left, bottom, paintBoundry);
		canvas.drawLine(right, top, right, bottom, paintBoundry);

		canvas.save();
		float sx = width * 1.f / Stroke.MAX_WIDTH;
		float sy = height * 1.f / Stroke.MAX_HEIGHT;
		canvas.scale(sx, sy);
		if (mStroke != null) {
			Path path = mStroke.getPath();
			canvas.drawPath(path, mPaintStroke);
		}
		canvas.restore();
	}

	private void initBoundaryPaint() {
		paintBoundry = new Paint();
		int boundaryColor = this.getContext().getResources().getColor(R.color.boundary_color);
		paintBoundry.setColor(boundaryColor);
	}

	private void initStrokePaint() {
		int strokeColor = this.getContext().getResources().getColor(
				R.color.stroke_color);

		mPaintStroke = new Paint();
		mPaintStroke.setStyle(Paint.Style.STROKE);
		mPaintStroke.setColor(strokeColor);
		mPaintStroke.setStrokeWidth(10);
	}
}
