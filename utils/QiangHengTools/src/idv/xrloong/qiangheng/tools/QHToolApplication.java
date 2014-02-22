package idv.xrloong.qiangheng.tools;

import idv.xrloong.qiangheng.tools.model.OperatorManager;
import idv.xrloong.qiangheng.tools.model.QHToolContent;
import idv.xrloong.qiangheng.tools.model.StrokeTypeManager;
import android.app.Application;

public class QHToolApplication extends Application {

	@Override
	public void onCreate () {
		super.onCreate();

		QHToolContent.initInstance(this);
		StrokeTypeManager.initInstance(this);
		OperatorManager.initInstance(this);
	}
}
