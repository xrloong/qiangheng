from .SOCodeInfo import SOCodeInfo
from ..DynamicComposition.DCCodeInfoEncoder import DCCodeInfoEncoder
from ..DynamicComposition.Calligraphy import Pane
from ..DynamicComposition.Calligraphy import StrokeGroup
from ..base.CodeInfo import CodeInfo

import sys
import copy

class SOCodeInfoEncoder(DCCodeInfoEncoder):
	def __init__(self):
		pass

	def generateDefaultCodeInfo(self, strokeGroup):
		return SOCodeInfo.generateDefaultCodeInfo(strokeGroup)
