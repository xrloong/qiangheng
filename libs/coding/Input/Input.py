from element.enum import CodingType

from coding.Base import CodeMappingInfoInterpreter as BaseCodeMappingInfoInterpreter

class CodeMappingInfoInterpreter(BaseCodeMappingInfoInterpreter):
	def __init__(self):
		super().__init__(CodingType.Input)


