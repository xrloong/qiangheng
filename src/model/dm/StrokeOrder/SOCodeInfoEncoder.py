from .SOCodeInfo import SOCodeInfo
from ..DynamicComposition.DCCodeInfoEncoder import DCCodeInfoEncoder
from model.base.CodeInfo import CodeInfo
from model.calligraphy.Calligraphy import Pane
from model.calligraphy.Calligraphy import StrokeGroup

class SOCodeInfoEncoder(DCCodeInfoEncoder):
	@classmethod
	def generateDefaultCodeInfo(cls, strokeGroup):
		return SOCodeInfo.generateDefaultCodeInfo(strokeGroup)
