from ..base.StructureRearranger import StructureRearranger
from im.gear import Operator

class ZMStructureRearranger(StructureRearranger):
	def getPatternList(self):
		return [
			("({運算=範湘} ({名稱=行.0}) .* ({名稱=行.1}) )", "(龍 行 \\2)"),
			("({運算=範湘} ({名稱=儿.0}) .* ({名稱=儿.1}) )", "(龍 儿 \\2)"),
			("({運算=範湘} ({名稱=[丨丨].0}) .* ({名稱=[丨丨].1}) )", "(龍 [丨丨] \\2)"),
			("({運算=範湘} ({名稱=[丨丿].0}) .* ({名稱=[丨丿].1}) )", "(龍 [丨丿] \\2)"),
			("({運算=範湘} ({名稱=[丿丨].0}) .* ({名稱=[丿丨].1}) )", "(龍 [丿丨] \\2)"),

			("({運算=範焤} ({名稱=辰}) .* )", "(廖 辰 \\2)"),
			("({運算=範焤} ({名稱=廣}) .* )", "(廖 廣 \\2)"),
		]

