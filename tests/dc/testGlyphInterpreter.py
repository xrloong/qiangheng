import unittest

from xie.graphics.factory import ComponentFactory
from xie.graphics.factory import StrokeFactory
from xie.graphics.factory import StrokeSpec

from coding.DynamicComposition.DynamicComposition import GlyphDescriptionInterpreter


strokeFactory = StrokeFactory()
componentFactory = ComponentFactory()


def generateStroke(typeName, splinePointsList, startPoint):
    spec = StrokeSpec(typeName, splinePointsList=splinePointsList)
    return strokeFactory.generateStrokeBySpec(spec, startPoint=startPoint)


def generateComponent():
    strokes = [
        generateStroke("橫", [[[202, 0]]], (20, 123)),
        generateStroke("豎", [[[0, 216]]], (96, 17)),
        generateStroke("點", [[[60, 73]]], (93, 91)),
    ]
    return componentFactory.generateComponentByStrokes(strokes)


def strokeSignatures(strokes):
    return [
        (stroke.getTypeName(), stroke.getStartPoint(), stroke.getStatePane().boundary)
        for stroke in strokes
    ]


class GlyphInterpreterTestCase(unittest.TestCase):
    """省略「順序」時，應等同依序引用全部筆劃。"""

    def setUp(self):
        self.interpreter = GlyphDescriptionInterpreter()
        self.component = generateComponent()

    def testOmittedOrderMeansAllStrokes(self):
        explicit = self.interpreter.retrieveStrokesOfComponentIntoPosition(
            self.component, [0, 1, 2], None
        )
        omitted = self.interpreter.retrieveStrokesOfComponentIntoPosition(
            self.component, None, None
        )
        self.assertEqual(strokeSignatures(omitted), strokeSignatures(explicit))

    def testOmittedOrderWithPosition(self):
        position = (8, 8, 247, 127)
        explicit = self.interpreter.retrieveStrokesOfComponentIntoPosition(
            self.component, [0, 1, 2], position
        )
        omitted = self.interpreter.retrieveStrokesOfComponentIntoPosition(
            self.component, None, position
        )
        self.assertEqual(strokeSignatures(omitted), strokeSignatures(explicit))

    def testPartialOrderStillSelects(self):
        strokes = self.interpreter.retrieveStrokesOfComponentIntoPosition(
            self.component, [0, 2], None
        )
        self.assertEqual(
            [stroke.getTypeName() for stroke in strokes],
            ["橫", "點"],
        )
