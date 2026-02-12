import ruamel.yaml

from .model import CharacterDecompositionSetModel
from .model import SubstituteRuleSetModel
from .model import RadicalSetModel


class QHParser:
    def __init__(self, yaml: ruamel.yaml.YAML):
        self.yaml = yaml

    def loadSubstituteRuleSet(self, filename) -> SubstituteRuleSetModel:
        with open(filename) as f:
            node = self.yaml.load(f)
        return SubstituteRuleSetModel(**node)

    def loadRadicalSet(self, filename) -> RadicalSetModel:
        with open(filename) as f:
            node = self.yaml.load(f)
        return RadicalSetModel(**node)

    def loadCharacterDecompositionSet(self, filename) -> CharacterDecompositionSetModel:
        with open(filename) as f:
            node = self.yaml.load(f)
        return CharacterDecompositionSetModel(**node)
