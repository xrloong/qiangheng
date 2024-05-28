from injector import Module
from injector import provider

import ruamel.yaml
import itertools

from injection.key import Characters
from injection.key import Writer
from injection.key import Quiet

from coding.Base import CodeInfoEncoder
from coding.Base import CodingRadixParser
from coding.Base import CodeMappingInfoInterpreter

from model.element.CodingConfig import CodingConfig
from model.element.enum import FontVariance

from model.helper import StructureDescriptionGenerator
from model.helper import QHTreeParser

from parser.QHParser import QHParser

from hanzi.network import HanZiNetwork

from model.StructureManager import StructureManager
from model.CharacterDescriptionManager import RadixManager

from .key import Package

class PackageModule(Module):
	def __init__(self, codingPackage: Package):
		self.codingPackage = codingPackage

	@provider
	def provideCodingPackage(self) -> Package:
		return self.codingPackage

	@provider
	def provideCodingConfig(self, codingPackage: Package) -> CodingConfig:
		return CodingConfig(codingPackage)

	@provider
	def provideCodeInfoEncoder(self, codingPackage: Package) -> CodeInfoEncoder:
		return codingPackage.CodeInfoEncoder()

	@provider
	def provideCodingRadixParser(self, codingPackage: Package) -> CodingRadixParser:
		return codingPackage.CodingRadixParser()

	@provider
	def provideFontVariance(self, codingPackage: Package) -> FontVariance:
		return codingPackage.fontVariance

	@provider
	def provideCodeMappingInfoInterpreter(self, codingPackage: Package) -> CodeMappingInfoInterpreter:
		return codingPackage.codeMappingInfoInterpreter

class ParserModule(Module):
	def __init__(self):
		pass

	@provider
	def provideQHTreeParser(self, nodeGenerator: StructureDescriptionGenerator) -> QHTreeParser:
		return QHTreeParser(nodeGenerator = nodeGenerator)

	@provider
	def provideQHParser(self, treeParser: QHTreeParser, yaml: ruamel.yaml.YAML) -> QHParser:
		return QHParser(treeParser = treeParser, yaml = yaml)

class ManagerModule(Module):
	def __init__(self, structureManager):
		self.structureManager = structureManager
		self.hanziNetwork = HanZiNetwork()

	@provider
	def provideStructureManager(self) -> StructureManager:
		return self.structureManager

	@provider
	def provideHanZiNetwork(self) -> HanZiNetwork:
		return self.hanziNetwork

	@provider
	def provideRadixManager(self, structureManager: StructureManager) -> RadixManager:
		return structureManager.radixManager

class IOModule(Module):
	def __init__(self, quiet):
		self.quiet = quiet

	@provider
	def provideYaml(self) -> ruamel.yaml.YAML:
		yaml = ruamel.yaml.YAML(typ = 'safe')
		yaml.explicit_start = True
		yaml.explicit_end = True
		yaml.allow_unicode = True
		yaml.default_flow_style = False
		return yaml

	@provider
	def provideWriter(self, yaml: ruamel.yaml.YAML) -> Writer:
		writer = self.computeWriter(self.quiet, yaml)
		return writer

	def computeWriter(self, quiet: Quiet, yaml: ruamel.yaml.YAML) -> Writer:
		if not quiet:
			from writer import CmYamlWriter
			writer = CmYamlWriter(yaml)
		else:
			# 不輸出結果
			from writer import QuietWriter
			writer = QuietWriter()
		return writer

class CharacterModule(Module):
    # Unicode 15.1
    # CJK Unified Ideographs —— 4E00-9FFF
    # CJK Unified Ideographs Extension A —— 3400-4DBF
    # CJK Unified Ideographs Extension B —— 20000–2A6DF
    # CJK Unified Ideographs Extension C —— 2A700-2B739
    # CJK Unified Ideographs Extension D —— 2B740–2B81D
    # CJK Unified Ideographs Extension E —— 2B820–2CEA1
    # CJK Unified Ideographs Extension F —— 2CEB0–2EBE0
    # CJK Unified Ideographs Extension G —— 30000–3134A
    # CJK Unified Ideographs Extension H —— 31350–323AF
    # CJK Unified Ideographs Extension I —— 2EBF0–2EE5D
    # CJK Compatibility Ideographs —— F900–FAFF
    # CJK Compatibility Ideographs Supplement —— 2F800–2FA1F
    # Kangxi Radicals —— 2F00–2FDF
    # CJK Radicals Supplement —— 2E80–2EFF

	__rangeCJK__implemented = range(0x4E00, 0x9FA5 + 1)
	__rangeCJKextA__implemented = range(0x3400, 0x4DB5 + 1)

	__rangeCJK = range(0x4E00, 0x9FFF + 1)
	__rangeCJKextA = range(0x3400, 0x4DBF + 1)
	__rangeCJKextB = range(0x20000, 0x2A6DF + 1)
	__rangeCJKextC = range(0x2A700, 0x2B739 + 1)
	__rangeCJKextD = range(0x2B740, 0x2B81D + 1)
	__rangeCJKextE = range(0x2B820, 0x2CEA1 + 1)
	__rangeCJKextF = range(0x2CEB0, 0x2EBE0 + 1)
	__rangeCJKextG = range(0x30000, 0x3134A + 1)
	__rangeCJKextH = range(0x31350, 0x323AF + 1)
	__rangeCJKextI = range(0x2EBF0, 0x2EE5D + 1)

	def __getCharacters(self) -> itertools.chain:
		return itertools.chain(
				CharacterModule.__rangeCJK__implemented,
				CharacterModule.__rangeCJKextA__implemented,
				)

	@provider
	def provideCharaceters(self) -> Characters:
		characters = tuple(chr(c) for c in self.__getCharacters())
		return characters
