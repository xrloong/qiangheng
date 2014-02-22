package idv.xrloong.qiangheng.tools;

import android.app.Application;

public class QHToolApplication extends Application {

	@Override
	public void onCreate () {
		super.onCreate();

		QHToolContent.initInstance(this);
	}
}
