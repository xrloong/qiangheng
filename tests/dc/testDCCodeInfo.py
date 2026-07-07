import unittest

from xie.graphics.factory import StrokeFactory
from xie.graphics.factory import StrokeSpec

from coding.DynamicComposition.DynamicComposition import DCCodeInfo
from coding.DynamicComposition.DynamicComposition import DCCodeInfoEncoder
from coding.DynamicComposition.DynamicComposition import DCComponent
from element.operator import Operator


strokeFactory = StrokeFactory()


def generateStroke(typeName, splinePointsList, startPoint):
    spec = StrokeSpec(typeName, splinePointsList=splinePointsList)
    return strokeFactory.generateStrokeBySpec(spec, startPoint=startPoint)


def codeInfo一():
    strokes = [generateStroke("橫", [[[202, 0]]], (20, 123))]
    return DCCodeInfo(DCComponent.generateComponentByStrokes(strokes))


def codeInfo十():
    strokes = [
        generateStroke("橫", [[[202, 0]]], (20, 123)),
        generateStroke("豎", [[[0, 216]]], (96, 17)),
    ]
    return DCCodeInfo(DCComponent.generateComponentByStrokes(strokes))


class EmptyCodeInfo:
    """xie 無法建構零筆劃的元件，這裡只需要 getStrokeCount 回報 0。"""

    def getStrokeCount(self):
        return 0


class DCCodeInfoTestCase(unittest.TestCase):
    def testStrokeCount(self):
        self.assertEqual(codeInfo一().getStrokeCount(), 1)
        self.assertEqual(codeInfo十().getStrokeCount(), 2)

    def testCodeIsComponent(self):
        codeInfo = codeInfo一()
        self.assertIs(codeInfo.code, codeInfo.getComponent())


class DCCodeInfoEncoderTestCase(unittest.TestCase):
    def setUp(self):
        self.encoder = DCCodeInfoEncoder()

    def testEncodeAsEqualReturnsFirstCodeInfo(self):
        codeInfo = codeInfo一()
        encoded = self.encoder.setByComps(Operator.Equal, [codeInfo])

        self.assertIs(encoded, codeInfo)

    def testEncodeAsSilkwormMergesStrokes(self):
        encoded = self.encoder.setByComps(
            Operator.Silkworm, [codeInfo一(), codeInfo十()]
        )

        self.assertEqual(encoded.getStrokeCount(), 3)

    def testEncodeAsGooseMergesStrokes(self):
        encoded = self.encoder.setByComps(Operator.Goose, [codeInfo十(), codeInfo十()])

        self.assertEqual(encoded.getStrokeCount(), 4)

    def testEncodeAsLoopMergesStrokes(self):
        encoded = self.encoder.setByComps(Operator.Loop, [codeInfo十(), codeInfo一()])

        self.assertEqual(encoded.getStrokeCount(), 3)

    def testSilkwormLaysComponentsTopToBottom(self):
        first = codeInfo一()
        second = codeInfo一()
        encoded = self.encoder.setByComps(Operator.Silkworm, [first, second])

        strokes = encoded.getComponent().getComponent().getStrokeList()
        paneTop = strokes[0].getStatePane()
        paneBottom = strokes[1].getStatePane()
        self.assertLess(paneTop.top, paneBottom.top)

    def testGooseLaysComponentsLeftToRight(self):
        first = codeInfo一()
        second = codeInfo一()
        encoded = self.encoder.setByComps(Operator.Goose, [first, second])

        strokes = encoded.getComponent().getComponent().getStrokeList()
        paneLeft = strokes[0].getStatePane()
        paneRight = strokes[1].getStatePane()
        self.assertLess(paneLeft.left, paneRight.left)

    def testOperationUnavailableWhenComponentHasNoStrokes(self):
        encoded = self.encoder.setByComps(
            Operator.Silkworm, [codeInfo一(), EmptyCodeInfo()]
        )

        self.assertIsNone(encoded)


if __name__ == "__main__":
    unittest.main()
