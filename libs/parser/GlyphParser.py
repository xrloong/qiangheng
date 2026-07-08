import abc
from typing import Any, Optional

import ruamel.yaml
from pydantic import BaseModel


class GlyphTags(object):
    STROKE_SET = "筆劃集"
    PART_SET = "零件集"
    COMPONENT_SET = "部件集"

    STROKE = "筆劃"
    NAME = "名稱"
    COMMENT = "註記"

    METHOD = "方式"
    TYPE = "類型"
    START_POINT = "起始點"
    PARAMETER = "參數"
    SPLINE_POINTS_LIST = "樣條節點串列"

    METHOD__DEFINITION = "定義"
    METHOD__REFERENCE = "引用"
    METHOD__ANCHOR = "錨點"

    REFRENCE_NAME = "引用名稱"
    ORDER = "順序"

    POSITION = "定位"


class GlyphElementDescription(BaseModel, frozen=True):
    method: str

    @property
    def isAnchor(self) -> bool:
        return self.method == GlyphTags.METHOD__ANCHOR

    @property
    def isReference(self) -> bool:
        return self.method == GlyphTags.METHOD__REFERENCE

    @property
    def isDefinition(self) -> bool:
        return self.method == GlyphTags.METHOD__DEFINITION


class GlyphDefinitionElementDescription(GlyphElementDescription, frozen=True):
    method: str = GlyphTags.METHOD__DEFINITION
    strokeType: str
    startPoint: Optional[list[Any]] = None
    position: Optional[list[Any]] = None
    params: Optional[Any] = None
    splinePointsList: Optional[list[Any]] = None


class GlyphAnchorElementDescription(GlyphElementDescription, frozen=True):
    method: str = GlyphTags.METHOD__ANCHOR
    name: str
    referenceName: str
    position: Optional[list[Any]] = None


class GlyphReferenceElementDescription(GlyphElementDescription, frozen=True):
    method: str = GlyphTags.METHOD__REFERENCE
    referenceName: str
    order: Optional[list[int]] = None
    position: Optional[list[Any]] = None


class GlyphStrokeDescription(BaseModel, frozen=True):
    name: str
    comment: Optional[str] = None
    element: GlyphElementDescription


class GlyphComponentDescription(BaseModel, frozen=True):
    name: str
    comment: Optional[str] = None
    elements: list[GlyphElementDescription]


class GlyphDataSetDescription(BaseModel, frozen=True):
    strokes: list[GlyphStrokeDescription]
    parts: list[GlyphComponentDescription]
    components: list[GlyphComponentDescription]


class GlyphParser(object):
    def __init__(self):
        super().__init__()
        self.yaml = ruamel.yaml.YAML(typ="safe")

    def load(self, filename):
        with open(filename) as f:
            rootNode = self.yaml.load(f)
        dataSet = self.parseAllDataSet(rootNode)
        return dataSet

    def parseDefinitionElement(self, elementNode) -> GlyphDefinitionElementDescription:
        return GlyphDefinitionElementDescription(
            strokeType=elementNode.get(GlyphTags.TYPE),
            params=elementNode.get(GlyphTags.PARAMETER),
            splinePointsList=elementNode.get(GlyphTags.SPLINE_POINTS_LIST),
            startPoint=elementNode.get(GlyphTags.START_POINT),
            position=elementNode.get(GlyphTags.POSITION),
        )

    def parseAnchorElement(self, elementNode) -> GlyphAnchorElementDescription:
        return GlyphAnchorElementDescription(
            name=elementNode.get(GlyphTags.NAME),
            referenceName=elementNode.get(GlyphTags.REFRENCE_NAME),
            position=elementNode.get(GlyphTags.POSITION),
        )

    def parseReferenceElement(self, elementNode) -> GlyphReferenceElementDescription:
        return GlyphReferenceElementDescription(
            referenceName=elementNode.get(GlyphTags.REFRENCE_NAME),
            order=elementNode.get(GlyphTags.ORDER),
            position=elementNode.get(GlyphTags.POSITION),
        )

    def parseElement(self, elementNode) -> GlyphElementDescription:
        method = elementNode.get(GlyphTags.METHOD)

        if method == GlyphTags.METHOD__DEFINITION:
            return self.parseDefinitionElement(elementNode)
        elif method == GlyphTags.METHOD__ANCHOR:
            return self.parseAnchorElement(elementNode)
        elif method == GlyphTags.METHOD__REFERENCE:
            return self.parseReferenceElement(elementNode)

        return GlyphElementDescription(method=method)

    def parseStroke(self, strokeNode) -> GlyphStrokeDescription:
        elementNode = strokeNode.get(GlyphTags.STROKE)
        return GlyphStrokeDescription(
            name=strokeNode.get(GlyphTags.NAME),
            comment=strokeNode.get(GlyphTags.COMMENT),
            element=self.parseElement(elementNode),
        )

    def parseComponent(self, componentNode) -> GlyphComponentDescription:
        elements = [
            self.parseElement(en) for en in componentNode.get(GlyphTags.STROKE)
        ]
        return GlyphComponentDescription(
            name=componentNode.get(GlyphTags.NAME),
            comment=componentNode.get(GlyphTags.COMMENT),
            elements=elements,
        )

    def parseDataSet(self, dataSetNode) -> list[GlyphComponentDescription]:
        return [self.parseComponent(n) for n in dataSetNode]

    def parseAllDataSet(self, rootNode) -> GlyphDataSetDescription:
        strokes = [
            self.parseStroke(n) for n in rootNode.get(GlyphTags.STROKE_SET)
        ]
        parts = self.parseDataSet(rootNode.get(GlyphTags.PART_SET))
        components = self.parseDataSet(rootNode.get(GlyphTags.COMPONENT_SET))
        return GlyphDataSetDescription(strokes=strokes, parts=parts, components=components)


class IfGlyphDescriptionInterpreter(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def interpretElement(self, element: GlyphElementDescription):
        pass

    @abc.abstractmethod
    def interpretStroke(self, component: GlyphStrokeDescription):
        pass

    @abc.abstractmethod
    def interpretComponent(self, component: GlyphComponentDescription):
        pass

    @abc.abstractmethod
    def interpretDataSet(self, dataSet: GlyphDataSetDescription):
        pass
