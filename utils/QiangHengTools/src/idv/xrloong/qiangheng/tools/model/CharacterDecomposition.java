package idv.xrloong.qiangheng.tools.model;

public class CharacterDecomposition {

	private int mCodePont;
	private String mOperator;
	private int mOperandCount;
	private String mOperand1;
	private String mOperand2;
	private String mOperand3;
	private String mOperand4;

	public CharacterDecomposition(int codePoint, String operator) {
		mCodePont = codePoint;
		mOperandCount = 0;
		mOperator = operator;
	}

	public CharacterDecomposition(int codePoint, String operator, String operand1) {
		mCodePont = codePoint;
		mOperator = operator;
		mOperandCount = 1;
		mOperand1 = operand1;
	}

	public CharacterDecomposition(int codePoint, String operator, String operand1, String operand2) {
		mCodePont = codePoint;
		mOperator = operator;
		mOperandCount = 2;
		mOperand1 = operand1;
		mOperand2 = operand2;
	}

	public CharacterDecomposition(int codePoint, String operator, String operand1, String operand2, String operand3) {
		mCodePont = codePoint;
		mOperator = operator;
		mOperandCount = 3;
		mOperand1 = operand1;
		mOperand2 = operand2;
		mOperand3 = operand3;
	}

	public CharacterDecomposition(int codePoint, String operator, String operand1, String operand2, String operand3, String operand4) {
		mCodePont = codePoint;
		mOperator = operator;
		mOperandCount = 4;
		mOperand1 = operand1;
		mOperand2 = operand2;
		mOperand3 = operand3;
		mOperand4 = operand4;
	}

	public int getCodePoint() {
		return mCodePont;
	}

	public String getOperator() {
		return mOperator;
	}

	public int getOperandCount() {
		return mOperandCount;
	}

	public String getOperand1() {
		return mOperand1;
	}

	public String getOperand2() {
		return mOperand2;
	}

	public String getOperand3() {
		return mOperand3;
	}

	public String getOperand4() {
		return mOperand4;
	}
}
