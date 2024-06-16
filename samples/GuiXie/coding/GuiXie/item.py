
from .constant import GXStroke
from .constant import GXCorner

from .util import computeStrokeCode


class GXLump:
    cornerToIndexDict = {
        GXCorner.TopLeft: 0,
        GXCorner.TopRight: 1,
        GXCorner.BottomLeft: 2,
        GXCorner.BottomRight: 3,
    }

    def __init__(self, corners, rectCount=0):
        bricks = []
        positions = [
            GXCorner.TopLeft,
            GXCorner.TopRight,
            GXCorner.BottomLeft,
            GXCorner.BottomRight,
        ]
        for pos, corner in zip(positions, corners):
            if isinstance(corner, GXStroke):
                stroke = corner
                brick = GXBrick.instanceForStroke(pos, stroke)
                bricks.append(brick)
            elif isinstance(corner, GXCorner):
                index = GXLump.cornerToIndexDict[corner]
                targetBrick = bricks[index]

                brick = GXBrick.instanceForReference(pos, targetBrick)
                bricks.append(brick)
            else:
                brick = GXBrick.instanceForInvalidate()
                bricks.append(brick)

        [self._top_left, self._top_right, self._bottom_left, self._bottom_right] = (
            bricks
        )
        self._corners = bricks
        self._rectCount = rectCount

    def computeStrokes(self, cornerCodes):
        for brick in self._corners:
            brick.setUsedByCorner(GXCorner.CornerNone)

        strokes = []
        for cornerCode in cornerCodes:
            index = GXLump.cornerToIndexDict[cornerCode]
            brick = self._corners[index]
            if not brick.isUsed():
                stroke = brick.getStroke()
                brick.setUsedByCorner(cornerCode)
            else:
                stroke = GXStroke.StrokeNone
            strokes.append(stroke)
        return strokes

    def computeStrokesOnAllCorners(self):
        return self.computeStrokes(
            (
                GXCorner.TopLeft,
                GXCorner.TopRight,
                GXCorner.BottomLeft,
                GXCorner.BottomRight,
            )
        )

    def computeStrokesOnMainDiagonal(self):
        return self.computeStrokes((GXCorner.TopLeft, GXCorner.BottomRight))

    def computeStrokesOnAntiDiagonal(self):
        return self.computeStrokes((GXCorner.TopRight, GXCorner.BottomLeft))

    def computeAllStrokes(self):
        return self.computeStrokes(
            (
                GXCorner.TopLeft,
                GXCorner.TopRight,
                GXCorner.BottomLeft,
                GXCorner.BottomRight,
            )
        )

    def computeCode(
        self,
        cornerCodes=(
            GXCorner.TopLeft,
            GXCorner.TopRight,
            GXCorner.BottomLeft,
            GXCorner.BottomRight,
        ),
    ):
        strokes = self.computeStrokes(cornerCodes)
        return "".join(computeStrokeCode(stroke) for stroke in strokes)

    def computeCodesOnMainDiagonal(self):
        return self.computeCodes((GXCorner.TopLeft, GXCorner.BottomRight))

    def computeCodesOnAntiDiagonal(self):
        return self.computeCodes((GXCorner.TopRight, GXCorner.BottomLeft))

    def computeCodesOfTop(self):
        return self.computeCodes((GXCorner.TopLeft, GXCorner.TopRight))

    def computeCodesOfBottom(self):
        return self.computeCodes((GXCorner.BottomLeft, GXCorner.BottomRight))

    def computeCodesOfAll(self):
        return self.computeCodes(
            (
                GXCorner.TopLeft,
                GXCorner.TopRight,
                GXCorner.BottomLeft,
                GXCorner.BottomRight,
            )
        )

    def computeCodes(self, positions):

        cornerToBrick = {}
        bricks = []
        for pos in positions:
            stroke = self.getStroke(pos)

            if isinstance(stroke, GXStroke):
                brick = GXBrick.instanceForStroke(stroke)
                cornerToBrick[pos] = brick
            elif isinstance(stroke, GXCorner):
                corner = stroke
                if corner in cornerToBrick:
                    wrapperBrick = cornerToBrick[corner]
                    brick = GXBrick.instanceForReference(wrapperBrick)
                else:
                    stroke = self.getStroke(corner)
                    brick = GXBrick.instanceForStroke(stroke)
                cornerToBrick[corner] = brick
            else:
                brick = GXBrick.instanceForInvalidate()

            bricks.append(brick)

        codes = []
        for brick in bricks:
            stroke = brick.getStrokeOrCorner()
            codes.append(stroke)
            brick.setUsedByPosition()

        return tuple(codes)

    def getStroke(self, pos):
        stroke = GXStroke.StrokeNone
        if pos == GXCorner.TopLeft:
            stroke = self.topLeft
        elif pos == GXCorner.TopRight:
            stroke = self.topRight
        elif pos == GXCorner.BottomLeft:
            stroke = self.bottomLeft
        elif pos == GXCorner.BottomRight:
            stroke = self.bottomRight
        else:
            stroke = GXStroke.StrokeNone
        return stroke

    @property
    def corners(self):
        return (self.topLeft, self.topRight, self.bottomLeft, self.bottomRight)

    @property
    def topLeft(self):
        return self._top_left

    @property
    def topRight(self):
        return self._top_right

    @property
    def bottomLeft(self):
        return self._bottom_left

    @property
    def bottomRight(self):
        return self._bottom_right

    @property
    def rectCount(self):
        return self._rectCount


class GXBrick:
    TYPE_INVALIDATE = 0
    TYPE_STROKE = 1
    TYPE_REFERENCE = 2

    def __init__(self, position=GXCorner.CornerNone):
        self.setAsInvalidate()
        self._position = position
        self._usedByCorner = GXCorner.CornerNone

    def __str__(self):
        if self.isStroke():
            return "(1, %s)" % self.stroke
        elif self.isReference():
            return "(2, %s)" % self.wrapperBrick.getStroke()
        elif self.isInvalidate():
            return "%s" % GXStroke.StrokeNone
        else:
            return "%s" % GXStroke.StrokeNone

    @property
    def position(self):
        if self.isStroke():
            return self._position
        elif self.isReference():
            return self.wrapperBrick.position
        elif self.isInvalidate():
            return self._position
        else:
            return self._position

    @staticmethod
    def instanceForInvalidate():
        return GXBrick(GXBrick.TYPE_INVALIDATE)

    @staticmethod
    def instanceForStroke(position, stroke):
        brick = GXBrick(position)
        brick.setAsStroke(stroke)
        return brick

    @staticmethod
    def instanceForReference(position, referencedBrick):
        brick = GXBrick(position)
        brick.setAsReference(referencedBrick)
        return brick
        return GXBrick(GXBrick.TYPE_REFERENCE, wrapperBrick=referencedBrick)

    def setAsInvalidate(self):
        self._type = GXBrick.TYPE_INVALIDATE

    def setAsStroke(self, stroke):
        self._type = GXBrick.TYPE_STROKE
        self.stroke = stroke

    def setAsReference(self, wrapperBrick):
        self._type = GXBrick.TYPE_REFERENCE
        self.wrapperBrick = wrapperBrick

    def isInvalidate(self):
        return self._type == GXBrick.TYPE_INVALIDATE

    def isStroke(self):
        return self._type == GXBrick.TYPE_STROKE

    def isReference(self):
        return self._type == GXBrick.TYPE_REFERENCE

    def setUsedByPosition(self):
        self.setUsedByCorner(self._position)

    def setUsedByCorner(self, corner):
        if self.isReference():
            self.wrapperBrick.setUsedByCorner(corner)
            return
        self._usedByCorner = corner

    def isUsed(self):
        if self.isReference():
            return self.wrapperBrick.isUsed()
        return self.getUsedCorner() != GXCorner.CornerNone

    def getUsedCorner(self):
        if self.isStroke():
            return self._usedByCorner
        elif self.isReference():
            return self.wrapperBrick.getUsedCorner()
        elif self.isInvalidate():
            return GXCorner.CornerNone
        else:
            return GXCorner.CornerNone

    def getStroke(self):
        if self.isStroke():
            return self.stroke
        elif self.isReference():
            return self.wrapperBrick.getStroke()
        elif self.isInvalidate():
            return GXStroke.StrokeNone
        else:
            return GXStroke.StrokeNone

    def getStrokeOrCorner(self):
        if self.isStroke():
            return self.stroke
        elif self.isReference():
            return self.position
        elif self.isInvalidate():
            return GXStroke.StrokeNone
        else:
            return GXStroke.StrokeNone
