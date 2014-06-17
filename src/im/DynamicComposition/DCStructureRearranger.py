from ..base.StructureRearranger import StructureRearranger
from im.gear import Operator

class DCStructureRearranger(StructureRearranger):
	def getPatternList(self):
		return [
			("({運算=範湘} ({名稱=儿.0}) .* ({名稱=儿.1}) )", "(鴻 丿 \\2 乚)"),
			("({運算=範產} . )", "(範志 文 (範廖 厂 \\1))"),
		]

