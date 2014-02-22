from .SOCodeInfo import SOCodeInfo
from ..DynamicComposition.DCCodeInfoEncoder import DCCodeInfoEncoder
from ..base.CodeInfo import CodeInfo

import sys
import copy

class SOCodeInfoEncoder(DCCodeInfoEncoder):
	WIDTH=256
	HEIGHT=256
	def __init__(self):
		pass

	def generateDefaultCodeInfo(self, strokeList, region=[0, 0, 0xFF, 0xFF]):
		return SOCodeInfo.generateDefaultCodeInfo(strokeList, region)

