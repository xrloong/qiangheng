from injector import Module
from injector import provider

from model.BaseCoding import CodeInfoEncoder
from model.BaseCoding import CodingInfo
from model.BaseCoding import CodingRadixParser

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
