package idv.xrloong.qiangheng.tools.model;

import idv.xrloong.qiangheng.tools.util.Logger;
import idv.xrloong.qiangheng.tools.view.IStrokeDrawable;
import idv.xrloong.qiangheng.tools.view.StrokeDrawableInfo;

import java.util.ArrayList;
import java.util.List;

import android.graphics.Path;
import android.graphics.Point;

public class StrokeAction implements IStrokeDrawable {
	private final static String LOG_TAG = Logger.getLogTag(StrokeAction.class);

	private String mName;
	private Path mPath;

	public StrokeAction(String description) {
		Logger.d(LOG_TAG, "Stroke()");

		mPath=new Path();

		mPath.reset();
		drawPath(mPath, description);
	}

	public String getName()
	{
		return mName;
	}

	@Override
	public List<StrokeDrawableInfo> getInfoList() {
		List<StrokeDrawableInfo> pathList = new ArrayList<StrokeDrawableInfo>();
		pathList.add(new StrokeDrawableInfo(mPath));
		return pathList;
	}

	public static void drawPath(Path path, String description)
	{
		String[] points = description.split(",");

		boolean isCurve = false;

		List<Point> pointList = new ArrayList<Point>();
		for(String d:points)
		{
			int action =Integer.parseInt(d.substring(0, 4), 16);
			int x=Integer.parseInt(d.substring(4, 6), 16);
			int y=Integer.parseInt(d.substring(6, 8), 16);
			Point p = new Point(x, y);
			pointList.add(p);
			int numPoints = pointList.size();
			switch(action){
			case 0:
				path.moveTo(x, y);
				break;
			case 1:
				if(isCurve)
				{
					Point p1 = pointList.get(numPoints-2);
					Point p2 = pointList.get(numPoints-1);
					path.quadTo(p1.x, p1.y, p2.x, p2.y);
				}
				else
				{
					Point p1 = pointList.get(numPoints-1);
					path.lineTo(p1.x, p1.y);
				}
				isCurve = false;
				break;
			case 2:
				isCurve = true;
				break;
			}
		}
	}
}
