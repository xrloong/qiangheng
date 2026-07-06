import unittest

from xie.graphics.canvas import BaseTextCanvasController
from xie.graphics.drawing import DrawingSystem
from xie.graphics.factory import ComponentFactory
from xie.graphics.factory import StrokeFactory
from xie.graphics.factory import StrokeSpec
from xie.graphics.shape import Pane

from coding.DynamicComposition.fastdraw import StrokeRenderer


strokeFactory = StrokeFactory()
componentFactory = ComponentFactory()


def generateStroke(typeName, splinePointsList, startPoint):
    spec = StrokeSpec(typeName, splinePointsList=splinePointsList)
    return strokeFactory.generateStrokeBySpec(spec, startPoint=startPoint)


def generateBaseStrokes():
    # 取自 qhdata/dc/radix/template.yaml 的代表性筆劃：
    # 橫（infoPane 高為 0）、豎（infoPane 寬為 0）、點（斜線）、
    # 橫折鉤（含二次貝茲曲線段）、橫折彎（多段混合）
    return [
        generateStroke("橫", [[[202, 0]]], (20, 123)),
        generateStroke("豎", [[[0, 216]]], (96, 17)),
        generateStroke("點", [[[60, 73]]], (93, 91)),
        generateStroke(
            "橫折鉤",
            [[[182, 0]], [[182, 203], [145, 203]], [[108, 171]]],
            (38, 26),
        ),
        generateStroke(
            "橫折彎",
            [[[88, 0]], [[88, 80]], [[88, 90], [98, 90]], [[145, 90]]],
            (77, 17),
        ),
    ]


def generateTransformedStrokes():
    # 透過元件組合產生經過縮放/平移的筆劃，涵蓋非整數與負座標
    strokes = generateBaseStrokes()
    component = componentFactory.generateComponentByStrokes(strokes)
    panes = [
        Pane(8, 8, 247, 127.5),
        Pane(-20, 30.25, 97, 141),
        Pane(0, 0, 33, 251),
    ]
    transformed = []
    for pane in panes:
        newComponent = componentFactory.generateComponentByComponentPane(
            component, pane
        )
        transformed.extend(newComponent.getStrokeList())
    return transformed


def renderStrokeByXie(stroke):
    controller = BaseTextCanvasController()
    ds = DrawingSystem(controller)
    stroke.draw(ds)
    expressionList = controller.expressionList
    return expressionList[0] if expressionList else ""


class FastDrawTestCase(unittest.TestCase):
    def setUp(self):
        self.renderer = StrokeRenderer()

    def testBaseStrokesMatchXie(self):
        for stroke in generateBaseStrokes():
            with self.subTest(stroke=stroke.getName()):
                self.assertEqual(
                    self.renderer.renderStroke(stroke), renderStrokeByXie(stroke)
                )

    def testTransformedStrokesMatchXie(self):
        for stroke in generateTransformedStrokes():
            with self.subTest(stroke=stroke.getName()):
                self.assertEqual(
                    self.renderer.renderStroke(stroke), renderStrokeByXie(stroke)
                )

    def testNoStateLeakBetweenStrokes(self):
        for stroke in generateTransformedStrokes():
            self.renderer.renderStroke(stroke)
            ds = self.renderer.drawingSystem
            self.assertEqual(ds.stack, [])
            self.assertEqual((ds.a, ds.c, ds.e, ds.f), (1.0, 0.0, 1.0, 0.0))

    def testRenderingIsMemoized(self):
        strokes = generateBaseStrokes()
        expected = [renderStrokeByXie(stroke) for stroke in strokes]

        for stroke, expectedExpression in zip(strokes, expected):
            self.renderer.renderStroke(stroke)
        cacheSize = len(self.renderer.cache)
        self.assertEqual(cacheSize, len(strokes))

        # 相同 (path, 起始點, 佔位 pane) 的筆劃需命中快取且結果不變
        for stroke, expectedExpression in zip(strokes, expected):
            self.assertEqual(self.renderer.renderStroke(stroke), expectedExpression)
        self.assertEqual(len(self.renderer.cache), cacheSize)

    def testTransformedCopiesShareCacheEntries(self):
        strokes = generateBaseStrokes()
        component = componentFactory.generateComponentByStrokes(strokes)
        pane = Pane(8, 8, 247, 127.5)

        copyA = componentFactory.generateComponentByComponentPane(component, pane)
        for stroke in copyA.getStrokeList():
            self.renderer.renderStroke(stroke)
        cacheSize = len(self.renderer.cache)

        # 同樣的組合再做一次：path 物件共享、幾何相同 → 不新增快取項目
        copyB = componentFactory.generateComponentByComponentPane(component, pane)
        for stroke in copyB.getStrokeList():
            self.renderer.renderStroke(stroke)
        self.assertEqual(len(self.renderer.cache), cacheSize)


if __name__ == "__main__":
    unittest.main()
