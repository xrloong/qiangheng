from coding.Drawing import CodeInfo
from coding.Drawing import CodeInfoEncoder
from coding.Drawing import CodingRadixParser
from coding.Drawing import CodeMappingInfoInterpreter

from ..DynamicComposition.DynamicComposition import DCCodeInfo
from ..DynamicComposition.DynamicComposition import DCCodeInfoEncoder
from ..DynamicComposition.DynamicComposition import DCRadixParser

from ..DynamicComposition.layout import JointOperator
from ..DynamicComposition.layout import LayoutFactory
from ..DynamicComposition.layout import LayoutSpec

class SOCodeInfo(DCCodeInfo):
	INSTALLMENT_SEPERATOR='|'
	STROKE_SEPERATOR=';'
	RADIX_SEPERATOR=','

	def __init__(self, strokeGroup):
		super().__init__(strokeGroup)

	@staticmethod
	def generateDefaultCodeInfo(components, panes):
		component = DCComponent.generateDefaultComponent(components, panes)
		codeInfo = SOCodeInfo(component)
		return codeInfo

class SOCodeInfoEncoder(DCCodeInfoEncoder):
	def generateDefaultCodeInfo(self, codeInfos, layoutSpec: LayoutSpec):
		panes = self.layoutFactory.generateLayouts(layoutSpec)
		components = [codeInfo.getComponent() for codeInfo in codeInfos]

		return DCCodeInfo.generateDefaultCodeInfo(components, panes)

class SORadixParser(DCRadixParser):
	def __init__(self):
		super().__init__()

class SOCodeMappingInfoInterpreter(CodeMappingInfoInterpreter):
	def __init__(self):
		super().__init__()

	def interpretCodeMappingInfo(self, codeMappingInfo):
		charName = codeMappingInfo.getName()
		dcComponent = codeMappingInfo.getCode()
		variance = codeMappingInfo.getVariance()

		component = dcComponent.getComponent()
		strokes = component.getStrokeList()
		names = tuple(stroke.getTypeName() for stroke in strokes)
		return {"字符": charName, "類型": variance, "筆順": names}

