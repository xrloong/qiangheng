from coding.Array.Array import ARCodeInfo
from coding.Array.Array import ARCodeInfoEncoder
from element.operator import Operator

import unittest


class ARCodeInfoTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPrecoditions(self):
        pass

    def testArray(self):
        # 一
        codeInfo = ARCodeInfo(["1-"])
        self.assertEqual(codeInfo.code, "a")

        # 丁
        codeInfo = ARCodeInfo(["1-", "3-"])
        self.assertEqual(codeInfo.code, "ad")

        # 丐
        codeInfo = ARCodeInfo(["1-", "3^", "5-"])
        self.assertEqual(codeInfo.code, "aeg")

        # 丏
        codeInfo = ARCodeInfo(["1-", "3-", "2-", "5-"])
        self.assertEqual(codeInfo.code, "adsg")

        # 噩
        codeInfo = ARCodeInfo(["1^", "0-", "4^", "0-", "0-"])
        self.assertEqual(codeInfo.code, "q;r;")


class ARCodeInfoEncoderTestCase(unittest.TestCase):
    def setUp(self):
        self.encoder = ARCodeInfoEncoder()

    def testEncodeAsLoongConcatenatesCodes(self):
        codeInfo = self.encoder.setByComps(
            Operator.Loong, [ARCodeInfo(["1-", "3-"]), ARCodeInfo(["5-"])]
        )

        self.assertEqual(codeInfo.code, "adg")

    def testEncodeAsLoongTruncatesLongCodes(self):
        # 超過四碼時，取首、次、三、尾碼
        codeInfo = self.encoder.setByComps(
            Operator.Loong,
            [ARCodeInfo(["1-", "3-", "2-"]), ARCodeInfo(["5-", "1^"])],
        )

        self.assertEqual(codeInfo.code, "adsq")

    def testGooseFallsBackToLoong(self):
        codeInfo = self.encoder.setByComps(
            Operator.Goose, [ARCodeInfo(["1-"]), ARCodeInfo(["3-"])]
        )

        self.assertEqual(codeInfo.code, "ad")

    def testEncodeAsHanSwapsOperands(self):
        codeInfo = self.encoder.setByComps(
            Operator.Han, [ARCodeInfo(["1-"]), ARCodeInfo(["3-", "5-"])]
        )

        self.assertEqual(codeInfo.code, "dga")

    def testEncodeAsZheSwapsOperands(self):
        codeInfo = self.encoder.setByComps(
            Operator.Zhe, [ARCodeInfo(["1-"]), ARCodeInfo(["3-"])]
        )

        self.assertEqual(codeInfo.code, "da")

    def testEncodeAsYouRotatesOperands(self):
        codeInfo = self.encoder.setByComps(
            Operator.You,
            [ARCodeInfo(["1-"]), ARCodeInfo(["3-"]), ARCodeInfo(["5-"])],
        )

        self.assertEqual(codeInfo.code, "dga")

    def testEncodeAsLuanRepeatsSecondOperand(self):
        codeInfo = self.encoder.setByComps(
            Operator.Luan, [ARCodeInfo(["1-"]), ARCodeInfo(["3-"])]
        )

        self.assertEqual(codeInfo.code, "add")

    def testOperationUnavailableWhenComponentHasNoCode(self):
        codeInfo = self.encoder.setByComps(
            Operator.Loong, [ARCodeInfo(["1-"]), ARCodeInfo(())]
        )

        self.assertIsNone(codeInfo)
