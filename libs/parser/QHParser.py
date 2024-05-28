import ruamel.yaml

from .model import CharacterDecompositionSetModel
from .model import SubstituteRuleSetModel
from .model import RadicalSetModel

class QHParser:
	def __init__(self, yaml: ruamel.yaml.YAML):
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
