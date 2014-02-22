from im.CangJie.CJLump import CJLump
#import im.CangJie.CJLump

import unittest

class CJLumpTestCase(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testPrecoditions(self):
		self.setUpLumps()

	def testSingleton(self):
		self.setUpLumps()

		self.assertEqual(self.lump_一.getCodeAsSingleton(), "m")

		self.assertEqual(self.lump_丁.getCodeAsSingleton(), "mn")

		self.assertEqual(self.lump_丂.getCodeAsSingleton(), "mvs")

		self.assertEqual(self.lump_丏.getCodeAsSingleton(), "mlvs")

		self.assertEqual(self.lump_离.getCodeAsSingleton(), "yukb")

	def setUpLumps(self):
		self.lump_一=CJLump.generate("m", "", "")
		self.assertIsNotNone(self.lump_一)

		self.lump_丁=CJLump.generate("mn", "", "")
		self.assertIsNotNone(self.lump_丁)

		self.lump_丂=CJLump.generate("mvs", "", "")
		self.assertIsNotNone(self.lump_丂)

		self.lump_丏=CJLump.generate("mlvs", "", "")
		self.assertIsNotNone(self.lump_丏)

		self.lump_离=CJLump.generate("yukib", "", "")
		self.assertIsNotNone(self.lump_离)

		self.lump_口=CJLump.generate("r", "", "")
		self.assertIsNotNone(self.lump_口)

		self.lump_土=CJLump.generate("g", "", "")
		self.assertIsNotNone(self.lump_土)

		self.lump_木=CJLump.generate("d", "", "")
		self.assertIsNotNone(self.lump_木)
#		self.lump_吐
#		self.lump_呆
#		self.lump_㕲
#		self.lump_杏
#		self.lump_杜
#		self.lump_林
#		self.lump_森
#		self.lump_品
#		self.lump_圭
#		self.lump_垚
#		self.lump_晏
#		self.lump_䁙
		self.lump_貝=CJLump.generate("buc", "", "")
		self.assertIsNotNone(self.lump_貝)
#		self.lump_賏
#		self.lump_贔
#		self.lump_曾
#		self.lump_㬝
#		self.lump_䯫
#		self.lump_高
#		self.lump_稿
#		self.lump_咼
#		self.lump_剮
#		self.lump_過
#		self.lump_卨
#		self.lump_需
#		self.lump_曷
#		self.lump_闌
#		self.lump_每
		self.lump_舟=CJLump.generate("h", "BY", "i")
		self.assertIsNotNone(self.lump_舟)

		self.lump_母=CJLump.generate("", "WY", "i")
		self.assertIsNotNone(self.lump_母)

		self.lump_毋=CJLump.generate("wj", "", "")
		self.assertIsNotNone(self.lump_毋)
#		self.lump_介
#		self.lump_夰
#		self.lump_昦
#		self.lump_兒
#		self.lump_儿
		self.lump_乚=CJLump.generate("u", "", "")
		self.assertIsNotNone(self.lump_乚)

		self.lump_丨=CJLump.generate("l", "", "")
		self.assertIsNotNone(self.lump_丨)

		self.lump_丿=CJLump.generate("h", "", "")
		self.assertIsNotNone(self.lump_丿)
#		胤
#		旁蒡徬
#		回圖牆嗇
#		柬闌䑌
#		夙風悤鏓
#		虍虎彪
#		䁓傻㚇鎫
#		甚堪
#		臧贓藏贜覸調䞁剮颱
#		乯
#		乖乘䏋
#		䯫髇嫓颪乯

if __name__ == '__main__':
	unittest.main()

