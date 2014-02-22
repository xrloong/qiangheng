from .SOCodeInfo import SOCodeInfo
from ..DynamicComposition.DCCodeInfoEncoder import DCCodeInfoEncoder
from ..DynamicComposition.Calligraphy import Pane
from ..DynamicComposition.Calligraphy import StrokeGroup
from ..base.CodeInfo import CodeInfo

class SOCodeInfoEncoder(DCCodeInfoEncoder):
	@classmethod
	def generateDefaultCodeInfo(cls, strokeGroup):
		return SOCodeInfo.generateDefaultCodeInfo(strokeGroup)
