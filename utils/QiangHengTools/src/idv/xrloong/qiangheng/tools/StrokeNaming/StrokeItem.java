package idv.xrloong.qiangheng.tools.StrokeNaming;

public class StrokeItem {
	public String charName;
	public int strokeNo;
	public String strokeName;
	public String strokeDescription;
	
	public StrokeItem(String charName, int strokeNo, String strokeDescription, String strokeName) {
		this.charName=charName;
		this.strokeNo=strokeNo;
		this.strokeName=strokeName;
		this.strokeDescription=strokeDescription;
	}
}
