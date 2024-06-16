import unittest

from coding.GuiXie.constant import GXGenre
from coding.GuiXie.constant import GXStroke

from coding.GuiXie.item import GXLump
from coding.GuiXie.GuiXie import GXCodeInfo
from coding.GuiXie.GuiXie import computeStrokes
from coding.GuiXie import util


class GXCodeInfoTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGXCodeInfo(self):
        # 舟（1/28330）
        gxLump1 = GXLump(util.constructCorners("2833"))
        codeInfo = GXCodeInfo(GXGenre.Zhong, [gxLump1])
        self.assertEqual(codeInfo.computeCode(), "1/28330")

        # 秉（1/20602）
        gxLump1 = GXLump(util.constructCorners("2060"), 2)
        codeInfo = GXCodeInfo(GXGenre.Zhong, [gxLump1])
        self.assertEqual(codeInfo.computeCode(), "1/20602")

        # 目（2/88113）
        gxLump1 = GXLump(util.constructCorners("8888"), 1)
        gxLump2 = GXLump(util.constructCorners("1111"))
        codeInfo = GXCodeInfo(GXGenre.Guo, [gxLump1, gxLump2], 2)
        self.assertEqual(codeInfo.computeCode(), "2/88113")

        # 閉（2/82304）
        gxLump1 = GXLump(util.constructCorners("8822"), 4)
        gxLump2 = GXLump(util.constructCorners("3070"), 0)
        codeInfo = GXCodeInfo(GXGenre.Guo, [gxLump1, gxLump2], 0)
        self.assertEqual(codeInfo.computeCode(), "2/82304")

    def test_computeStrokes_Zhong(self):
        # 「中」體

        # 承（1/18590）
        gxLump1 = GXLump(util.constructCorners("1859"))
        self.assertEqual(
            computeStrokes(GXGenre.Zhong, [gxLump1]),
            [GXStroke.Stroke1, GXStroke.Stroke8, GXStroke.Stroke5, GXStroke.Stroke9],
        )

        # 舟（1/28330）
        gxLump1 = GXLump(util.constructCorners("2833"))
        self.assertEqual(
            computeStrokes(GXGenre.Zhong, [gxLump1]),
            [GXStroke.Stroke2, GXStroke.Stroke8, GXStroke.Stroke3, GXStroke.Stroke3],
        )

        # 中（1/58082）
        gxLump1 = GXLump(util.constructCorners("58a8"), 2)
        self.assertEqual(
            computeStrokes(GXGenre.Zhong, [gxLump1]),
            [GXStroke.Stroke5, GXStroke.Stroke8, GXStroke.StrokeNone, GXStroke.Stroke8],
        )

    def test_computeStrokes_Guo(self):
        # 「國」體

        # 匿（2/81381）
        gxLump1 = GXLump(util.constructCorners("8181"))
        gxLump2 = GXLump(util.constructCorners("3388"))
        self.assertEqual(
            computeStrokes(GXGenre.Guo, [gxLump1, gxLump2]),
            [GXStroke.Stroke8, GXStroke.Stroke1, GXStroke.Stroke3, GXStroke.Stroke8],
        )

        # 延（2/14270）
        gxLump1 = GXLump(util.constructCorners("1844"))
        gxLump2 = GXLump(util.constructCorners("2077"))
        self.assertEqual(
            computeStrokes(GXGenre.Guo, [gxLump1, gxLump2]),
            [GXStroke.Stroke1, GXStroke.Stroke4, GXStroke.Stroke2, GXStroke.Stroke7],
        )

    def test_computeStrokes_Zi(self):
        # 「字」體

        # 荷（3/33921）
        gxLump1 = GXLump(util.constructCorners("3003"))
        gxLump2 = GXLump(util.constructCorners("9702"))
        self.assertEqual(
            computeStrokes(GXGenre.Zi, [gxLump1, gxLump2]),
            [GXStroke.Stroke3, GXStroke.Stroke3, GXStroke.Stroke9, GXStroke.Stroke2],
        )

        # 腎（3/84825）
        gxLump1 = GXLump(util.constructCorners("8884"))
        gxLump2 = GXLump(util.constructCorners("8822"))
        self.assertEqual(
            computeStrokes(GXGenre.Zi, [gxLump1, gxLump2]),
            [GXStroke.Stroke8, GXStroke.Stroke4, GXStroke.Stroke8, GXStroke.Stroke2],
        )

    def test_computeStrokes_Gui(self):
        # 「庋」體

        # 厚（4/12832）
        gxLump1 = GXLump(util.constructCorners("8120"))
        gxLump2 = GXLump(util.constructCorners("8803"))
        self.assertEqual(
            computeStrokes(GXGenre.Gui, [gxLump1, gxLump2]),
            [GXStroke.Stroke1, GXStroke.Stroke2, GXStroke.Stroke8, GXStroke.Stroke3],
        )

        # 名（4/82881）
        gxLump1 = GXLump(util.constructCorners("2820"))
        gxLump2 = GXLump(util.constructCorners("8888"))
        self.assertEqual(
            computeStrokes(GXGenre.Gui, [gxLump1, gxLump2]),
            [GXStroke.Stroke8, GXStroke.Stroke2, GXStroke.Stroke8, GXStroke.Stroke8],
        )

        # 多（4/82220）
        gxLump1 = GXLump(util.constructCorners("282c"))
        gxLump2 = GXLump(util.constructCorners("282c"))
        self.assertEqual(
            computeStrokes(GXGenre.Gui, [gxLump1, gxLump2]),
            [GXStroke.Stroke8, GXStroke.Stroke2, GXStroke.Stroke2, GXStroke.Stroke2],
        )

    def test_computeStrokes_Xie(self):
        # 「㩪」體

        # 欺（5/39293）
        gxLump1 = GXLump(util.constructCorners("3309"))
        gxLump2 = GXLump(util.constructCorners("2809"))
        self.assertEqual(
            computeStrokes(GXGenre.Xie, [gxLump1, gxLump2]),
            [GXStroke.Stroke3, GXStroke.Stroke9, GXStroke.Stroke2, GXStroke.Stroke9],
        )

        # 務（5/12920）    5/12920
        gxLump1 = GXLump(util.constructCorners("1072"))
        gxLump2 = GXLump(util.constructCorners("9032"))
        self.assertEqual(
            computeStrokes(GXGenre.Xie, [gxLump1, gxLump2]),
            [GXStroke.Stroke1, GXStroke.Stroke2, GXStroke.Stroke9, GXStroke.Stroke2],
        )
