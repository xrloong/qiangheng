import unittest

class GuiXieTestCase(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_ImportGuiXie(self):
		try:
			import coding.GuiXie
		except:
			self.fail("coding.GuiXie 不存在。")

	def test_CodingSubstituteFileList_exists(self):
		import coding.GuiXie

		try:
			from coding.GuiXie import CodingSubstituteFileList
		except ImportError:
			self.fail("coding.GuiXie 中缺少 CodingSubstituteFileList")

		for f in CodingSubstituteFileList:
			# 確認檔案存在
			try:
				open(f, "r").close()
			except FileNotFoundError:
				self.fail("{} 不存在".format(f))

	def test_CodingRadixFileList_exists(self):
		import coding.GuiXie

		try:
			from coding.GuiXie import CodingRadixFileList
		except ImportError:
			self.fail("coding.GuiXie 中缺少 CodingRadixFileList")

		for f in CodingRadixFileList:
			# 確認檔案存在
			try:
				open(f, "r").close()
			except FileNotFoundError:
				self.fail("{} 不存在".format(f))

	def test_codingType_exists(self):
		try:
			from coding.GuiXie import codingType
		except ImportError:
			self.fail("coding.GuiXie 中缺少 codingType")

	def test_fontVariance_exists(self):
		try:
			from coding.GuiXie import fontVariance
		except ImportError:
			self.fail("coding.GuiXie 中缺少 fontVariance")

	def test_codeMappingInfoInterpreter_exists(self):
		try:
			from coding.GuiXie import codeMappingInfoInterpreter
		except ImportError:
			self.fail("coding.GuiXie 中缺少 codeMappingInfoInterpreter")

