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
from model.element.enum import CodingType
from model.element.enum import FontVariance

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
	def provideCodingType(self, codingPackage: Package) -> CodingType:
		return codingPackage.codingType

	@provider
	def provideFontVariance(self, codingPackage: Package) -> FontVariance:
		return codingPackage.fontVariance

	@provider
	def provideCodeMappingInfoInterpreter(self, codingPackage: Package) -> CodeMappingInfoInterpreter:
		return codingPackage.codeMappingInfoInterpreter

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
	__rangeCJK = range(0x4E00, 0x9FA5 + 1)
	__rangeCJKextA = range(0x3400, 0x4DB5 + 1)

	def __getCharacters(self) -> itertools.chain:
		return itertools.chain(
				CharacterModule.__rangeCJK,
				CharacterModule.__rangeCJKextA,
				)

	@provider
	def provideCharaceters(self) -> Characters:
		characters = tuple(chr(c) for c in self.__getCharacters())
		return characters
