"""動態組字的快速筆劃描繪。

xie 的 DrawingSystem 對每個點做 numpy 3×3 矩陣乘法，並在每次
translate/scale 配置新陣列。但其矩陣恆為

    [[a, 0, c],
     [0, e, f],
     [0, 0, 1]]

（translate 以矩陣「加法」只修改 c、f；scale 以對角陣左乘），
因此用四個純 float 重現即可；a*x + 0*y + c 與 a*x + c 在 IEEE 754
下位元相同，輸出與 xie 完全一致。

筆劃的描繪表達式只由 (筆劃路徑, 起始點, 佔位 pane) 決定，且
Stroke.transform 產生的複本共享同一個路徑物件，故可跨字元記憶化。

元件組合（ComponentFactory.generateComponentByComponentPanePairs）同理：
xie 對每個點重算 pane 的中心與縮放比，這裡每個 (元件, pane) 只算一次，
運算順序與 xie 相同，結果位元一致。
"""

from xie.graphics.component import Component
from xie.graphics.component import ComponentInfo
from xie.graphics.shape import Pane
from xie.graphics.shape import mergePanes
from xie.graphics.stroke import Stroke
from xie.graphics.stroke import StrokePosition


def _transformedStrokes(component, targetPane):
    """等價於 xie 的 [s.transform(fromPane, targetPane) for s in strokes]，
    但 pane 幾何只計算一次；運算順序對應 shape.py 的
    transformRelativePointByTargetPane。"""
    fromPane = component.getStatePane()
    fl, ft, fr, fb = fromPane.boundary
    fw = fr - fl
    fh = fb - ft
    fcx = fl + fw / 2
    fcy = ft + fh / 2

    tl, tt, tr, tb = targetPane.boundary
    tw = tr - tl
    th = tb - tt
    tcx = tl + tw / 2
    tcy = tt + th / 2

    scaleX = tw / fw if fw != 0 else None
    scaleY = th / fh if fh != 0 else None

    def transformPoint(x, y):
        newX = x - fcx
        newY = y - fcy
        if scaleX is not None:
            newX *= scaleX
        if scaleY is not None:
            newY *= scaleY
        return (newX + tcx, newY + tcy)

    strokes = []
    for stroke in component.getStrokeList():
        startPoint = stroke.getStartPoint()
        statePane = stroke.getStatePane()
        left, top = transformPoint(statePane.left, statePane.top)
        right, bottom = transformPoint(statePane.right, statePane.bottom)
        strokes.append(
            Stroke(
                stroke.getTypeName(),
                stroke.getStrokePath(),
                StrokePosition(
                    transformPoint(startPoint[0], startPoint[1]),
                    Pane(left, top, right, bottom),
                ),
            )
        )
    return strokes


def fastGenerateComponentByComponentPanePairs(componentPanePairs):
    strokes = []
    for component, pane in componentPanePairs:
        strokes.extend(_transformedStrokes(component, pane))

    panes = [stroke.getStatePane() for stroke in strokes]
    return Component(ComponentInfo(strokes), mergePanes(panes))


class StrokeExpressionCollector:
    """收集單一筆劃的描繪表達式，等價於 BaseTextCanvasController 的
    編碼行為（round 後以 TextCodec 的格式串接）。"""

    def __init__(self, size=(256, 256)):
        self.size = size
        self.points = []
        self.expression = ""

    def getWidth(self):
        return self.size[0]

    def getHeight(self):
        return self.size[1]

    def clear(self):
        self.points = []
        self.expression = ""

    def onPreDrawCharacter(self, character):
        pass

    def onPostDrawCharacter(self, character):
        pass

    def onPreDrawStroke(self, stroke):
        self.points = []

    def onPostDrawStroke(self, stroke):
        self.expression = ",".join(self.points)

    def moveTo(self, p):
        self.points = ["0.{}.{}".format(round(p[0]), round(p[1]))]

    def lineTo(self, p):
        self.points.append("1.{}.{}".format(round(p[0]), round(p[1])))

    def qCurveTo(self, cp, p):
        self.points.append("2.{}.{}".format(round(cp[0]), round(cp[1])))
        self.points.append("1.{}.{}".format(round(p[0]), round(p[1])))


class FastAffineDrawingSystem:
    """xie DrawingSystem 的替代品，由 xie 的 Stroke/StrokePath/Segment
    以相同 API 驅動。所有運算順序都對應 xie/graphics/drawing.py。"""

    def __init__(self, canvasController):
        self.canvasController = canvasController
        self.a = 1.0
        self.c = 0.0
        self.e = 1.0
        self.f = 0.0
        self.stack = []
        self.lastPoint = (0, 0)

    def getWidth(self):
        return self.canvasController.getWidth()

    def getHeight(self):
        return self.canvasController.getHeight()

    def save(self):
        self.stack.append((self.a, self.c, self.e, self.f))

    def restore(self):
        self.a, self.c, self.e, self.f = self.stack.pop()

    def translate(self, x, y):
        # xie 的 translate 是矩陣加法，只修改平移項
        self.c += x
        self.f += y

    def scale(self, sx, sy):
        self.a *= sx
        self.c *= sx
        self.e *= sy
        self.f *= sy

    def startDrawing(self):
        self.lastPoint = (0, 0)

    def endDrawing(self):
        self.lastPoint = (0, 0)

    def onPreDrawCharacter(self, character):
        self.canvasController.onPreDrawCharacter(character)

    def onPostDrawCharacter(self, character):
        self.canvasController.onPostDrawCharacter(character)

    def onPreDrawStroke(self, stroke):
        self.canvasController.onPreDrawStroke(stroke)

    def onPostDrawStroke(self, stroke):
        self.canvasController.onPostDrawStroke(stroke)

    def __convertPoint(self, point):
        # 對應 _convertPointByBoundary（來源邊界固定 256×256）再加上
        # 前一點位移
        lastPoint = self.lastPoint
        return (
            lastPoint[0] + (point[0] - 0) * self.getWidth() / 256,
            lastPoint[1] + (point[1] - 0) * self.getHeight() / 256,
        )

    def moveTo(self, point):
        p = self.__convertPoint(point)
        self.canvasController.moveTo((self.a * p[0] + self.c, self.e * p[1] + self.f))
        self.lastPoint = p

    def lineTo(self, point):
        p = self.__convertPoint(point)
        self.canvasController.lineTo((self.a * p[0] + self.c, self.e * p[1] + self.f))
        self.lastPoint = p

    def qCurveTo(self, p1, p2):
        # 兩點都相對於同一個 lastPoint（xie 在兩次轉換間不更新它）
        cp = self.__convertPoint(p1)
        p = self.__convertPoint(p2)
        self.canvasController.qCurveTo(
            (self.a * cp[0] + self.c, self.e * cp[1] + self.f),
            (self.a * p[0] + self.c, self.e * p[1] + self.f),
        )
        self.lastPoint = p

    def clear(self):
        self.canvasController.clear()

    def draw(self, shape):
        shape.draw(self)


class StrokeRenderer:
    """全程重用一組 collector 與 drawing system，並以
    (id(路徑), 起始點, 佔位 pane 邊界) 記憶化筆劃表達式。
    快取值保留路徑物件，避免 id 被回收重用。"""

    def __init__(self):
        self.controller = StrokeExpressionCollector()
        self.drawingSystem = FastAffineDrawingSystem(self.controller)
        self.cache = {}

    def renderStroke(self, stroke):
        path = stroke.getStrokePath()
        key = (
            id(path),
            tuple(stroke.getStartPoint()),
            stroke.getStatePane().boundary,
        )
        entry = self.cache.get(key)
        if entry is None:
            stroke.draw(self.drawingSystem)
            entry = (self.controller.expression, path)
            self.cache[key] = entry
        return entry[0]
