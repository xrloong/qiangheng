from injector import Module
from injector import provider

from coding.Base import CodeInfoEncoder
from coding.Base import CodingInfo
from coding.Base import CodingRadixParser

from hanzi.network import HanZiNetwork

from model.StructureManager import StructureManager
from model.CharacterDescriptionManager import RadixManager

from Constant import Package

class PackageModule(Module):
	@provider
	def provideCodingInfo(self, package: Package) -> CodingInfo:
		return package.CodingInfo()

	@provider
	def provideCodeInfoEncoder(self, codingPackage: Package) -> CodeInfoEncoder:
		return codingPackage.CodeInfoEncoder

	@provider
	def provideCodingRadixParser(self, codingPackage: Package) -> CodingRadixParser:
		return codingPackage.CodingRadixParser()

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

