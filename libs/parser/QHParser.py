import ruamel.yaml

from .model import CharacterDecompositionSetModel
from .model import SubstituteRuleSetModel
from .model import RadicalSetModel

from model.element.CharacterDescription import CharacterDescription
from model.helper import StructureParser

class QHParser:
	def __init__(self, structureParser: StructureParser, yaml: ruamel.yaml.YAML):
		self.structureParser = structureParser
		self.yaml = yaml

	def loadSubstituteRuleSet(self, filename) -> SubstituteRuleSetModel:
		node = self.yaml.load(open(filename))
		return SubstituteRuleSetModel(**node)

	def loadRadicalSet(self, filename) -> RadicalSetModel:
		node = self.yaml.load(open(filename))
		return RadicalSetModel(**node)

	def loadCharacters(self, filename) -> CharacterDecompositionSetModel:
		node = self.yaml.load(open(filename))
		return CharacterDecompositionSetModel(**node)
