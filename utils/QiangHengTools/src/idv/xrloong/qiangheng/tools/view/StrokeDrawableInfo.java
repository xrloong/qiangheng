package idv.xrloong.qiangheng.tools.view;

import idv.xrloong.qiangheng.tools.model.Geometry;
import android.graphics.Color;
import android.graphics.Path;

public class StrokeDrawableInfo {
	private static int COLORS[] = new int[] {Color.GREEN, Color.BLUE, Color.CYAN, Color.MAGENTA, Color.YELLOW};
	private Path mPath;
	private int mColor;
	private Geometry mGeometry = new Geometry("0000FFFF");

	public static int getNormalColor() {
		return Color.BLACK;
	}

	public static int getGuessColor() {
		return Color.RED;
	}

	public static int getRefColor(int i) {
		int size = COLORS.length;
		return COLORS[i%size];
	}

	public StrokeDrawableInfo(Path path) {
		this(path, getNormalColor());
	}

	public StrokeDrawableInfo(Path path, int color) {
		mPath = path;
		mColor = color;
	}

	public void setGeometry(Geometry geometry) {
		mGeometry = geometry;
	}

	public Geometry getGeometry() {
		return mGeometry;
	}

	public Path getPath() {
		return mPath;
	}

	public int getColor() {
		return mColor;
	}

	public void setColor(int color) {
		mColor = color;
	}
}
