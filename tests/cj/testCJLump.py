from coding.CangJie.CangJie import CJLump

import unittest


class CJLumpTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # 倉頡規則：
    # 1 若為獨體字，最多四碼
    # 1-1 四碼以下，全取
    # 1-2 超過四碼，取首、次、三、尾碼

    # 2 若為合體字，則分別對字首及字身取碼
    # 2-1 對字首取碼，最多二碼
    # 2-1-1 二碼以下，全取
    # 2-1-2 超過二碼，取首、尾碼
    # 2-1-2-1 字首為獨體字，取首、尾碼
    # 2-1-2-2 字首為合體字，取字首的字首的首碼及字首的字身的尾碼

    # 2-2 對字身取碼，最多三碼
    # 2-2-1 字身為獨體字
    # 2-2-1-1 三碼以下，全取
    # 2-2-1-2 超過三碼，取字身的首、次、尾碼
    # 2-2-2 字身為合體字
    # 2-2-2-1 字身的字首一碼，字身的字身一碼，全取
    # 2-2-2-2 字身的字首一碼，字身的字身二碼以上，取字身的字首及字身的字身的首、尾碼
    # 2-2-2-3 字身的字首二碼以上，字身的字身一碼，取字身的字首的首、尾碼及字身的字身
    # 2-2-2-4 字身的字首二碼，以上字身的字身二碼以上，取字身的字首的首、尾碼及字身的字身的尾碼
    def testPrecoditions(self):
        self.setUpLumps()

    def testSingleton(self):
        self.setUpLumps()

        # 規則 1-1
        self.assertEqual(self.lump_一.getCodeAsSingleton(), "m")
        self.assertEqual(self.lump_丁.getCodeAsSingleton(), "mn")
        self.assertEqual(self.lump_丂.getCodeAsSingleton(), "mvs")
        self.assertEqual(self.lump_丏.getCodeAsSingleton(), "mlvs")

        # 規則 1-2
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

        # 字首為一碼，例字：札、柤、枰、梘
        # 2-1-1 + 2-2-1-1
        code = self.computeTotalCode([self.lump_木, self.lump_乚])
        self.assertEqual(code, "du")

        # 2-1-1 + 2-2-1-1
        code = self.computeTotalCode([self.lump_木, self.lump_且])
        self.assertEqual(code, "dbm")

        # 2-1-1 + 2-2-1-1
        code = self.computeTotalCode([self.lump_木, self.lump_交])
        self.assertEqual(code, "dyck")

        # 2-1-1 + 2-2-1-2
        code = self.computeTotalCode([self.lump_木, self.lump_見])
        self.assertEqual(code, "dbuu")

        # 字首為二碼，例字：玌、珇、玶、現
        # 2-1-1 + 2-2-1-1
        code = self.computeTotalCode([self.lump_王, self.lump_乚])
        self.assertEqual(code, "mgu")

        # 2-1-1 + 2-2-1-1
        code = self.computeTotalCode([self.lump_王, self.lump_且])
        self.assertEqual(code, "mgbm")

        # 2-1-1 + 2-2-1-1
        code = self.computeTotalCode([self.lump_王, self.lump_交])
        self.assertEqual(code, "mgyck")

        # 2-1-1 + 2-2-1-2
        code = self.computeTotalCode([self.lump_王, self.lump_見])
        self.assertEqual(code, "mgbuu")

        # 字首大於二碼，例字：虬、蛆、蚲、蜆
        # 2-1-2 + 2-2-1-1
        code = self.computeTotalCode([self.lump_虫, self.lump_乚])
        self.assertEqual(code, "liu")

        # 2-1-2 + 2-2-1-1
        code = self.computeTotalCode([self.lump_虫, self.lump_且])
        self.assertEqual(code, "libm")

        # 2-1-2 + 2-2-1-1
        code = self.computeTotalCode([self.lump_虫, self.lump_交])
        self.assertEqual(code, "liyck")

        # 2-1-2 + 2-2-1-2
        code = self.computeTotalCode([self.lump_虫, self.lump_見])
        self.assertEqual(code, "libuu")

        # 同向三個部件，第二個部件為一碼。例字：琳、玳。
        # 2-1-1 + 2-2-2-1
        code = self.computeTotalCode([self.lump_王, self.lump_木, self.lump_木])
        self.assertEqual(code, "mgdd")

        # 2-1-1 + 2-2-2-2
        code = self.computeTotalCode([self.lump_王, self.lump_亻, self.lump_弋])
        self.assertEqual(code, "mgoip")

        # 同向三個部件，第二個部件為二碼。例字：珈、瑘。
        # 2-1-1 + 2-2-2-3
        code = self.computeTotalCode([self.lump_王, self.lump_力, self.lump_口])
        self.assertEqual(code, "mgksr")

        # 2-1-1 + 2-2-2-4
        code = self.computeTotalCode([self.lump_王, self.lump_耳, self.lump_阝])
        self.assertEqual(code, "mgsjl")

        # 同向三個部件，第二個部件大於二碼。例字：玼、琊。
        # 2-1-1 + 2-2-2-4
        code = self.computeTotalCode([self.lump_王, self.lump_止, self.lump_匕])
        self.assertEqual(code, "mgymp")

        # 2-1-1 + 2-2-2-4
        code = self.computeTotalCode([self.lump_王, self.lump_牙, self.lump_阝])
        self.assertEqual(code, "mgmhl")

        # 同向四個部件，第二個部件為一碼。例字：娰。
        # 2-1-2 + 2-2-2-2
        code = self.computeTotalCode(
            [self.lump_魚, self.lump_亻, self.lump_丨, self.lump_攵]
        )
        self.assertEqual(code, "nfolk")

        # 同向四個部件，第二個部件為二碼。例字：䮛。
        # 2-1-2 + 2-2-2-4
        code = self.computeTotalCode(
            [self.lump_馬, self.lump_阝, self.lump_亻, self.lump_寸]
        )
        self.assertEqual(code, "sfnli")

        # 同向四個部件，第二個部件大於二碼。例字：㗾。
        # 2-1-2 + 2-2-2-4
        code = self.computeTotalCode(
            [self.lump_口, self.lump_革, self.lump_亻, self.lump_匕]
        )
        self.assertEqual(code, "rtjp")

    def testDifferentDirection(self):
        self.setUpLumps()

        # 字首為獨體，一碼。次字首一碼，次字身一碼。例字：柦
        # 2-1-1 + 2-2-2-1
        lump_旦 = CJLump.generateBody([self.lump_日, self.lump_一])
        code = self.computeTotalCode([self.lump_木, lump_旦])
        self.assertEqual(code, "dam")

        # 字首為獨體，一碼。次字首一碼，次字身二碼。例字：榥
        # 2-1-1 + 2-2-2-1
        lump_干 = CJLump.generateBody([self.lump_日, self.lump_干])
        code = self.computeTotalCode([self.lump_木, lump_干])
        self.assertEqual(code, "damj")

        # 字首為獨體，一碼。次字首一碼，次字身大於二碼。例字：榥
        # 2-1-1 + 2-2-2-2
        lump_晃 = CJLump.generateBody([self.lump_日, self.lump_光])
        code = self.computeTotalCode([self.lump_木, lump_晃])
        self.assertEqual(code, "dafu")

        # 字首為獨體，一碼。次字首二碼，次字身一碼。例字：柸、楻
        # 2-1-1 + 2-2-2-3
        lump_丕 = CJLump.generateBody([self.lump_不, self.lump_一])
        code = self.computeTotalCode([self.lump_木, lump_丕])
        self.assertEqual(code, "dmfm")

        # 2-1-1 + 2-2-2-3
        lump_皇 = CJLump.generateBody([self.lump_白, self.lump_王])
        code = self.computeTotalCode([self.lump_木, lump_皇])
        self.assertEqual(code, "dhag")

        # 字首為獨體，一碼。次字首大於二碼，次字身一碼。例字：棔、楞
        # 2-1-1 + 2-2-2-4
        lump_昏 = CJLump.generateBody([self.lump_氏, self.lump_日])
        code = self.computeTotalCode([self.lump_木, lump_昏])
        self.assertEqual(code, "dhpa")

        # 2-1-1 + 2-2-2-4
        lump_罒方 = CJLump.generateBody([self.lump_罒, self.lump_方])
        code = self.computeTotalCode([self.lump_木, lump_罒方])
        self.assertEqual(code, "dwls")

    def computeTotalCode(self, lumpList):
        return CJLump.computeTotalCode(lumpList)

    def setUpLumps(self):
        self.lump_一 = CJLump.generate("m", "", "")
        self.assertIsNotNone(self.lump_一)

        self.lump_丁 = CJLump.generate("mn", "", "")
        self.assertIsNotNone(self.lump_丁)

        self.lump_丂 = CJLump.generate("mvs", "", "")
        self.assertIsNotNone(self.lump_丂)

        self.lump_丏 = CJLump.generate("mlvs", "", "")
        self.assertIsNotNone(self.lump_丏)

        self.lump_离 = CJLump.generate("yukib", "", "")
        self.assertIsNotNone(self.lump_离)

        self.lump_口 = CJLump.generate("r", "", "")
        self.assertIsNotNone(self.lump_口)

        self.lump_土 = CJLump.generate("g", "", "")
        self.assertIsNotNone(self.lump_土)

        self.lump_木 = CJLump.generate("d", "", "")
        self.assertIsNotNone(self.lump_木)

        self.lump_王 = CJLump.generate("mg", "", "")
        self.assertIsNotNone(self.lump_王)

        self.lump_虫 = CJLump.generate("lmi", "", "")
        self.assertIsNotNone(self.lump_虫)

        self.lump_交 = CJLump.generate("yck", "", "")
        self.assertIsNotNone(self.lump_交)

        self.lump_見 = CJLump.generate("buhu", "", "")
        self.assertIsNotNone(self.lump_見)

        self.lump_亻 = CJLump.generate("o", "", "")
        self.assertIsNotNone(self.lump_亻)

        self.lump_弋 = CJLump.generate("ip", "", "")
        self.assertIsNotNone(self.lump_弋)

        self.lump_牙 = CJLump.generate("mvdh", "", "")
        self.assertIsNotNone(self.lump_牙)

        self.lump_耳 = CJLump.generate("sj", "", "")
        self.assertIsNotNone(self.lump_耳)

        self.lump_阝 = CJLump.generate("nl", "", "")
        self.assertIsNotNone(self.lump_阝)

        self.lump_革 = CJLump.generate("tlj", "", "")
        self.assertIsNotNone(self.lump_革)

        self.lump_匕 = CJLump.generate("p", "", "")
        self.assertIsNotNone(self.lump_匕)

        self.lump_馬 = CJLump.generate("sqsf", "", "")
        self.assertIsNotNone(self.lump_馬)

        self.lump_魚 = CJLump.generate("nwf", "", "")
        self.assertIsNotNone(self.lump_魚)

        self.lump_攵 = CJLump.generate("ok", "", "")
        self.assertIsNotNone(self.lump_攵)

        self.lump_寸 = CJLump.generate("di", "", "")
        self.assertIsNotNone(self.lump_寸)

        self.lump_日 = CJLump.generate("a", "", "")
        self.assertIsNotNone(self.lump_日)

        self.lump_光 = CJLump.generate("fmu", "", "")
        self.assertIsNotNone(self.lump_光)

        self.lump_干 = CJLump.generate("mj", "", "")
        self.assertIsNotNone(self.lump_干)

        self.lump_不 = CJLump.generate("mf", "", "")
        self.assertIsNotNone(self.lump_不)

        self.lump_白 = CJLump.generate("ha", "", "")
        self.assertIsNotNone(self.lump_白)

        self.lump_氏 = CJLump.generate("hvp", "", "")
        self.assertIsNotNone(self.lump_氏)

        self.lump_罒 = CJLump.generate("", "W", "ll")
        self.assertIsNotNone(self.lump_罒)

        self.lump_方 = CJLump.generate("yhs", "", "")
        self.assertIsNotNone(self.lump_方)

        self.lump_且 = CJLump.generate("bm", "", "")
        self.assertIsNotNone(self.lump_且)

        self.lump_力 = CJLump.generate("ks", "", "")
        self.assertIsNotNone(self.lump_力)

        self.lump_止 = CJLump.generate("ylm", "", "")
        self.assertIsNotNone(self.lump_止)

        # self.lump_吐
        # self.lump_呆
        # self.lump_㕲
        # self.lump_杏
        # self.lump_杜
        # self.lump_林
        # self.lump_森
        # self.lump_品
        # self.lump_圭
        # self.lump_垚
        # self.lump_晏
        # self.lump_䁙
        self.lump_貝 = CJLump.generate("buc", "", "")
        self.assertIsNotNone(self.lump_貝)
        # self.lump_贔
        # self.lump_曾
        # self.lump_㬝
        # self.lump_䯫
        # self.lump_高
        # self.lump_稿
        # self.lump_咼
        # self.lump_剮
        # self.lump_過
        # self.lump_卨
        # self.lump_需
        # self.lump_曷
        # self.lump_闌
        # self.lump_每
        self.lump_舟 = CJLump.generate("h", "BY", "i")
        self.assertIsNotNone(self.lump_舟)

        self.lump_母 = CJLump.generate("", "WY", "i")
        self.assertIsNotNone(self.lump_母)

        self.lump_毋 = CJLump.generate("wj", "", "")
        self.assertIsNotNone(self.lump_毋)
        # self.lump_介
        # self.lump_夰
        # self.lump_昦
        # self.lump_兒
        # self.lump_儿
        self.lump_乚 = CJLump.generate("u", "", "")
        self.assertIsNotNone(self.lump_乚)

        self.lump_丨 = CJLump.generate("l", "", "")
        self.assertIsNotNone(self.lump_丨)

        self.lump_丿 = CJLump.generate("h", "", "")
        self.assertIsNotNone(self.lump_丿)
        # 胤
        # 旁蒡徬
        # 回圖牆嗇
        self.lump_柬 = CJLump.generate("d", "W", "f")
        self.assertIsNotNone(self.lump_柬)

        self.lump_門 = CJLump.generate("an", "", "")
        self.assertIsNotNone(self.lump_門)

        self.lump_更 = CJLump.generate("mlwk", "", "")
        self.assertIsNotNone(self.lump_更)


# 闌蘭爤爛
# 夙風悤鏓
# 虍虎彪
# 䁓傻㚇鎫
# 甚堪
# 臧贓藏贜覸調䞁剮颱
# 乖乘䏋
# 䯫髇嫓颪乯

if __name__ == "__main__":
    unittest.main()
