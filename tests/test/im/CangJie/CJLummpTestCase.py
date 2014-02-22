#from im.CangJie.CJLump import CJLump
import im.CangJie.CJLump

import unittest

class CJLumpTestCase(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testPrecoditions(self):
		pass

	def testSingleton(self):
		# 案例：一
		lump=CJLump.generate("m", "", "")
		self.assertEqual(lump.getCodeAsSingleton(), "m")

		# 案例：丁
		lump=CJLump.generate("mn", "", "")
		self.assertEqual(lump.getCodeAsSingleton(), "mn")

		# 案例：丂
		lump=CJLump.generate("mvs", "", "")
		self.assertEqual(lump.getCodeAsSingleton(), "mvs")

		# 案例：丏
		lump=CJLump.generate("mlvs", "", "")
		self.assertEqual(lump.getCodeAsSingleton(), "mlvs")

		# 案例：离
		lump=CJLump.generate("yukib", "", "")
		self.assertEqual(lump.getCodeAsSingleton(), "yukb")

if __name__ == '__main__':
	unittest.main()

