from ..base.StructureRearranger import StructureRearranger
from im.gear import Operator

class CJStructureRearranger(StructureRearranger):
	def getPatternList(self):
		return [
			("({運算=範焤} ({名稱=厭}) .* )", "(廖 厭 \\2)"),
			("({運算=範焤} ({名稱=辰}) .* )", "(廖 辰 \\2)"),
			("({運算=範焤} ({名稱=麻}) .* )", "(廖 麻 \\2)"),

			("({運算=範湘} ({名稱=儿.0}) .* ({名稱=儿.1}) )", "(鴻 丨 \\2 乚)"),
			("({運算=範威} . )", "(範同 戊 (範志 一 \\1))"),
			("({運算=範產} . )", "(範志 文 (範廖 厂 \\1))"),
		]

