package idv.xrloong.qiangheng.tools.view;

import java.util.ArrayList;
import java.util.List;

import idv.xrloong.qiangheng.tools.R;
import idv.xrloong.qiangheng.tools.util.Logger;
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Path;
import android.util.AttributeSet;
import android.view.View;

public class StrokeView extends View {
	private static final String LOG_TAG = Logger.getLogTag(StrokeView.class);

	private IStrokeViewController mController = new IStrokeViewController() {
		@Override
		public IStrokeDrawable getStrokeDrawable() {
			return new IStrokeDrawable() {

				@Override
				public List<Path> getPathList() {
					return new ArrayList<Path>();
				}
			};
		}
	};
	private Paint mPaintStroke;
	private Paint paintBoundry;

	public StrokeView(Context context, AttributeSet attrs) {
		super(context, attrs);

		initBoundaryPaint();
		initStrokePaint();
	}

	public void setController(IStrokeViewController controller) {
		Logger.d(LOG_TAG, "setController() +");

		mController = controller;
		invalidate();

		Logger.d(LOG_TAG, "setController() -");
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
		float sx = width * 1.f / IStrokeDrawable.MAX_WIDTH;
		float sy = height * 1.f / IStrokeDrawable.MAX_HEIGHT;
		canvas.scale(sx, sy);

		drawAllStrokes(canvas);

		canvas.restore();
	}

	private void drawAllStrokes(Canvas canvas) {
		IStrokeDrawable strokeDrawable = mController.getStrokeDrawable();
		drawStroke(canvas, strokeDrawable);
	}

	private void drawStroke(Canvas canvas, IStrokeDrawable drawableStroke) {
		List<Path> pathList = drawableStroke.getPathList();
		for(Path path : pathList) {
			drawPath(canvas, path);
		}
	}

	private void drawPath(Canvas canvas, Path path) {
		canvas.drawPath(path, mPaintStroke);
	}

	private void initBoundaryPaint() {
		paintBoundry = new Paint();
		int boundaryColor = this.getContext().getResources().getColor(R.color.boundary_color);
		paintBoundry.setColor(boundaryColor);
	}

	private void initStrokePaint() {
		int strokeColor = this.getContext().getResources().getColor(R.color.stroke_color);

		mPaintStroke = new Paint();
		mPaintStroke.setStyle(Paint.Style.STROKE);
		mPaintStroke.setColor(strokeColor);
		mPaintStroke.setStrokeWidth(10);
	}
}
