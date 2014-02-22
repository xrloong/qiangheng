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

		# 小於等四碼，全取
		self.assertEqual(self.lump_一.getCodeAsSingleton(), "m")
		self.assertEqual(self.lump_丁.getCodeAsSingleton(), "mn")
		self.assertEqual(self.lump_丂.getCodeAsSingleton(), "mvs")
		self.assertEqual(self.lump_丏.getCodeAsSingleton(), "mlvs")

		# 大於四碼，取首、次、次次、尾碼
		self.assertEqual(self.lump_离.getCodeAsSingleton(), "yukb")

	def testHead(self):
		self.setUpLumps()

		# 小於等二碼，全取
		self.assertEqual(self.lump_一.getCodeAsHead(), "m")
		self.assertEqual(self.lump_丁.getCodeAsHead(), "mn")

		# 大於二碼，取首碼
		self.assertEqual(self.lump_丂.getCodeAsHead(), "ms")
		self.assertEqual(self.lump_丏.getCodeAsHead(), "ms")

		self.assertEqual(self.lump_柬.getCodeAsHead(), "dw")
		self.assertEqual(self.lump_母.getCodeAsHead(), "wy")
		self.assertEqual(self.lump_舟.getCodeAsHead(), "hy")

	def testBody(self):
		self.setUpLumps()

		# 小於等二碼，全取
		self.assertEqual(self.lump_一.getCodeAsBody(), "m")
		self.assertEqual(self.lump_丁.getCodeAsBody(), "mn")
		self.assertEqual(self.lump_丂.getCodeAsBody(), "mvs")

		# 大於二碼，取首碼
		self.assertEqual(self.lump_丏.getCodeAsBody(), "mls")

		self.assertEqual(self.lump_柬.getCodeAsBody(), "dwf")
		self.assertEqual(self.lump_母.getCodeAsBody(), "wyi")
		self.assertEqual(self.lump_舟.getCodeAsBody(), "hby")

	def testTail(self):
		self.setUpLumps()

		self.assertEqual(self.lump_一.getCodeAsTail(), "m")

		self.assertEqual(self.lump_柬.getCodeAsTail(), "w")
		self.assertEqual(self.lump_母.getCodeAsTail(), "y")
		self.assertEqual(self.lump_舟.getCodeAsTail(), "y")

	def testTotal(self):
		self.setUpLumps()

	def testSameDirection(self):
		self.setUpLumps()

		# 字首為一碼，代表字：札、枰、梘
		code=self.computeTotalCode([self.lump_木, self.lump_乚])
		self.assertEqual(code, "du")

		code=self.computeTotalCode([self.lump_木, self.lump_交])
		self.assertEqual(code, "dyck")

		code=self.computeTotalCode([self.lump_木, self.lump_見])
		self.assertEqual(code, "dbuu")


		# 字首為二碼，代表字：玌、玶、現
		code=self.computeTotalCode([self.lump_王, self.lump_乚])
		self.assertEqual(code, "mgu")

		code=self.computeTotalCode([self.lump_王, self.lump_交])
		self.assertEqual(code, "mgyck")

		code=self.computeTotalCode([self.lump_王, self.lump_見])
		self.assertEqual(code, "mgbuu")


		# 字首大於二碼，代表字：虬、蚲、蜆
		code=self.computeTotalCode([self.lump_虫, self.lump_乚])
		self.assertEqual(code, "liu")

		code=self.computeTotalCode([self.lump_虫, self.lump_交])
		self.assertEqual(code, "liyck")

		code=self.computeTotalCode([self.lump_虫, self.lump_見])
		self.assertEqual(code, "libuu")


		# 同向三個部件，第二個部件為一碼。代表字：玳。
		code=self.computeTotalCode([self.lump_王, self.lump_亻, self.lump_弋])
		self.assertEqual(code, "mgoip")

		# 同向三個部件，第二個部件為二碼。代表字：瑘。
		code=self.computeTotalCode([self.lump_王, self.lump_耳, self.lump_阝])
		self.assertEqual(code, "mgsjl")

		# 同向三個部件，第二個部件大於二碼。代表字：琊。
		code=self.computeTotalCode([self.lump_王, self.lump_牙, self.lump_阝])
		self.assertEqual(code, "mgmhl")


		# 同向四個部件，第二個部件為一碼。代表字：娰。
		code=self.computeTotalCode([self.lump_魚, self.lump_亻, self.lump_丨, self.lump_攵])
		self.assertEqual(code, "nfolk")

		# 同向四個部件，第二個部件為二碼。代表字：䮛。
		code=self.computeTotalCode([self.lump_馬, self.lump_阝, self.lump_亻, self.lump_寸])
		self.assertEqual(code, "sfnli")

		# 同向四個部件，第二個部件大於二碼。代表字：㗾。
		code=self.computeTotalCode([self.lump_口, self.lump_革, self.lump_亻, self.lump_匕])
		self.assertEqual(code, "rtjp")

	def testDifferentDirection(self):
		self.setUpLumps()

	def computeTotalCode(self, lumpList):
		return CJLump.computeTotalCode(lumpList)

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

		self.lump_王=CJLump.generate("mg", "", "")
		self.assertIsNotNone(self.lump_王)

		self.lump_虫=CJLump.generate("lmi", "", "")
		self.assertIsNotNone(self.lump_虫)

		self.lump_交=CJLump.generate("yck", "", "")
		self.assertIsNotNone(self.lump_交)

		self.lump_見=CJLump.generate("buhu", "", "")
		self.assertIsNotNone(self.lump_見)

		self.lump_亻=CJLump.generate("o", "", "")
		self.assertIsNotNone(self.lump_亻)

		self.lump_弋=CJLump.generate("ip", "", "")
		self.assertIsNotNone(self.lump_弋)

		self.lump_牙=CJLump.generate("mvdh", "", "")
		self.assertIsNotNone(self.lump_牙)

		self.lump_耳=CJLump.generate("sj", "", "")
		self.assertIsNotNone(self.lump_耳)

		self.lump_阝=CJLump.generate("nl", "", "")
		self.assertIsNotNone(self.lump_阝)

		self.lump_革=CJLump.generate("tlj", "", "")
		self.assertIsNotNone(self.lump_革)

		self.lump_匕=CJLump.generate("p", "", "")
		self.assertIsNotNone(self.lump_匕)

		self.lump_馬=CJLump.generate("sqsf", "", "")
		self.assertIsNotNone(self.lump_馬)

		self.lump_魚=CJLump.generate("nwf", "", "")
		self.assertIsNotNone(self.lump_魚)

		self.lump_攵=CJLump.generate("ok", "", "")
		self.assertIsNotNone(self.lump_攵)

		self.lump_寸=CJLump.generate("di", "", "")
		self.assertIsNotNone(self.lump_寸)

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
		self.lump_柬=CJLump.generate("d", "W", "f")
		self.assertIsNotNone(self.lump_柬)

		self.lump_門=CJLump.generate("an", "", "")
		self.assertIsNotNone(self.lump_門)

		self.lump_更=CJLump.generate("mlwk", "", "")
		self.assertIsNotNone(self.lump_更)
#		闌蘭爤爛
#		夙風悤鏓
#		虍虎彪
#		䁓傻㚇鎫
#		甚堪
#		臧贓藏贜覸調䞁剮颱
#		乖乘䏋
#		䯫髇嫓颪乯

if __name__ == '__main__':
	unittest.main()

