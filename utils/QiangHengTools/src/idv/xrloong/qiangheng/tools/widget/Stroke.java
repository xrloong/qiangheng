package idv.xrloong.qiangheng.tools.widget;

import idv.xrloong.qiangheng.tools.util.Logger;

import java.util.ArrayList;
import java.util.List;

import android.graphics.Path;
import android.graphics.Point;

public class Stroke {
	private final static String LOG_TAG = Logger.getLogTag(Stroke.class);

	public final static int MAX_WIDTH = 256;
	public final static int MAX_HEIGHT = 256;

	private String mName;
	private Path mPath;

	public Stroke(String description) {
		Logger.d(LOG_TAG, "Stroke()");

		mPath=new Path();

		String[] x = description.split(",");
		setPath(x);
	}

	public String getName()
	{
		return mName;
	}

	public Path getPath()
	{
		return mPath;
	}

	private void setPath(String[] points)
	{
		boolean isCurve = false;

		List<Point> pointList = new ArrayList<Point>();
		mPath.reset();
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
				mPath.moveTo(x, y);
				break;
			case 1:
				if(isCurve)
				{
					Point p1 = pointList.get(numPoints-2);
					Point p2 = pointList.get(numPoints-1);
					mPath.quadTo(p1.x, p1.y, p2.x, p2.y);
				}
				else
				{
					Point p1 = pointList.get(numPoints-1);
					mPath.lineTo(p1.x, p1.y);
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
