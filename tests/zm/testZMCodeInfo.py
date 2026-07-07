import unittest

from coding.ZhengMa.ZhengMa import ZMCodeInfo
from coding.ZhengMa.ZhengMa import ZMCodeInfoEncoder
from element.operator import Operator


class ZMCodeInfoTestCase(unittest.TestCase):
    # 鄭碼取碼規則（依字根數與首字根碼長分段）：
    # 一字根：全取
    # 二字根且皆為一碼：首、尾字根各取首碼，補 vv
    # 二字根其餘情形：首、尾字根串接後取前四碼
    # 三字根：依首字根碼長取一/二/三碼，再取後續字根首碼補滿四碼
    # 四字根以上：取首字根碼後，取倒數第二、最後字根的首碼

    def code(self, codes, extraCode=None, codesSingleton=None):
        return ZMCodeInfo(codes, extraCode, codesSingleton).code

    def testSingleRadix(self):
        self.assertEqual(self.code(("ab",)), "ab")
        self.assertEqual(self.code(("abcd",)), "abcd")

    def testTwoSingleCodeRadicesPadWithVv(self):
        self.assertEqual(self.code(("a", "b")), "abvv")

    def testTwoRadicesTakeFirstFourCodes(self):
        self.assertEqual(self.code(("ab", "cd")), "abcd")
        self.assertEqual(self.code(("a", "bc")), "abc")
        self.assertEqual(self.code(("abc", "de")), "abcd")

    def testThreeRadicesDependOnFirstRadixLength(self):
        # 首字根一碼：首、次字根首碼＋尾字根前二碼
        self.assertEqual(self.code(("a", "bc", "de")), "abde")
        # 首字根二碼：首字根＋倒數第二、最後字根首碼
        self.assertEqual(self.code(("ab", "cd", "ef")), "abce")
        # 首字根三碼：首字根＋最後字根首碼
        self.assertEqual(self.code(("abc", "de", "fg")), "abcf")

    def testFourRadicesDependOnFirstRadixLength(self):
        # 首字根一碼：首、次字根首碼＋倒數第二、最後字根首碼
        self.assertEqual(self.code(("a", "bc", "de", "fg")), "abdf")
        # 首字根二碼：首字根＋倒數第二、最後字根首碼
        self.assertEqual(self.code(("ab", "cd", "ef", "gh")), "abeg")
        # 首字根三碼：首字根＋最後字根首碼
        self.assertEqual(self.code(("abc", "de", "fg", "hi")), "abch")

    def testExtraCodeIsAppended(self):
        self.assertEqual(self.code(("ab",), extraCode="c"), "abc")

    def testSingletonCodesTakePriority(self):
        # 如「冈」類字根：構字時當成單一字根，為此字本身編碼時用原字根序列
        codeInfo = ZMCodeInfo(("ld",), "x", ("a", "b"))
        self.assertEqual(codeInfo.code, "abvv")


class ZMCodeInfoEncoderTestCase(unittest.TestCase):
    def setUp(self):
        self.encoder = ZMCodeInfoEncoder()

    def codeInfo(self, codes):
        return ZMCodeInfo(codes, None, None)

    def testEncodeAsLoongConcatenatesRadices(self):
        codeInfo = self.encoder.setByComps(
            Operator.Loong,
            [self.codeInfo(("a", "b")), self.codeInfo(("c",))],
        )

        self.assertEqual(codeInfo.getRtList(), ("a", "b", "c"))

    def testEncodeAsLoongTruncatesKeepingHeadTwo(self):
        codeInfo = self.encoder.setByComps(
            Operator.Loong,
            [self.codeInfo(("a", "b", "c")), self.codeInfo(("d", "e"))],
        )

        self.assertEqual(codeInfo.getRtList(), ("a", "b", "d", "e"))

    def testEncodeAsHanSwapsOperands(self):
        codeInfo = self.encoder.setByComps(
            Operator.Han,
            [self.codeInfo(("a",)), self.codeInfo(("b", "c"))],
        )

        self.assertEqual(codeInfo.getRtList(), ("b", "c", "a"))

    def testEncodeAsYouRotatesOperands(self):
        codeInfo = self.encoder.setByComps(
            Operator.You,
            [self.codeInfo(("a",)), self.codeInfo(("b",)), self.codeInfo(("c",))],
        )

        self.assertEqual(codeInfo.getRtList(), ("b", "c", "a"))

    def testEncodeAsLiangKeepsOnlyFirstRadix(self):
        codeInfo = self.encoder.setByComps(
            Operator.Liang,
            [self.codeInfo(("a", "b")), self.codeInfo(("c",))],
        )

        self.assertEqual(codeInfo.getRtList(), ("a",))

    def testOperationUnavailableWhenComponentHasNoCode(self):
        codeInfo = self.encoder.setByComps(
            Operator.Loong,
            [self.codeInfo(("a",)), self.codeInfo(())],
        )

        self.assertIsNone(codeInfo)


if __name__ == "__main__":
    unittest.main()
