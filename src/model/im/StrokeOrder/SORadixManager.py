from .SOCodeInfoEncoder import SOCodeInfoEncoder
from ..DynamicComposition.DCRadixManager import DCRadixParser

class SORadixParser(DCRadixParser):
	def __init__(self, nameInputMethod, codeInfoEncoder):
		super().__init__("動態組字", codeInfoEncoder)

