import ruamel.yaml
import abc


class GlyphElementDescription:
    def __init__(self, method):
        self.method = method

    @property
    def isAnchor(self):
        return self.method == GlyphTags.METHOD__ANCHOR

    @property
    def isReference(self):
        return self.method == GlyphTags.METHOD__REFERENCE

    @property
    def isDefinition(self):
        return self.method == GlyphTags.METHOD__DEFINITION


class GlyphDefinitionElementDescription(GlyphElementDescription):
    def __init__(
        self, strokeType, startPoint, position, params=None, splinePointsList=None
    ):
        super().__init__(GlyphTags.METHOD__DEFINITION)

        self.strokeType = strokeType
        self.params = params
        self.splinePointsList = splinePointsList

        self.startPoint = startPoint
        self.position = position


class GlyphAnchorElementDescription(GlyphElementDescription):
    def __init__(self, name, referenceName, position):
        super().__init__(GlyphTags.METHOD__ANCHOR)

        self.name = name
        self.referenceName = referenceName
        self.position = position


class GlyphReferenceElementDescription(GlyphElementDescription):
    def __init__(self, referenceName, order, position):
        super().__init__(GlyphTags.METHOD__REFERENCE)

        self.referenceName = referenceName
        self.order = order
        self.position = position


class GlyphStrokeDescription:
    def __init__(self, name, comment=None):
        self.name = name
        self.comment = comment
        self.stroke = None


class GlyphComponentDescription:
    def __init__(self, name, comment=None):
        self.name = name
        self.comment = comment
        self.elements = None


class GlyphDataSetDescription:
    def __init__(
        self,
        strokes: [GlyphStrokeDescription],
        parts: [GlyphComponentDescription],
        components: [GlyphComponentDescription],
    ):
        self.strokes = strokes
        self.parts = parts
        self.components = components


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


class GlyphParser(object):
    def __init__(self):
        super().__init__()
        self.yaml = ruamel.yaml.YAML()

    def load(self, filename):
        rootNode = self.yaml.load(open(filename))
        dataSet = self.parseAllDataSet(rootNode)
        return dataSet

    def parseDefinitionElement(self, elementNode):
        strokeType = elementNode.get(GlyphTags.TYPE)
        params = elementNode.get(GlyphTags.PARAMETER)
        startPoint = elementNode.get(GlyphTags.START_POINT)
        position = elementNode.get(GlyphTags.POSITION)
        splinePointsList = elementNode.get(GlyphTags.SPLINE_POINTS_LIST)
        return GlyphDefinitionElementDescription(
            strokeType,
            params=params,
            splinePointsList=splinePointsList,
            startPoint=startPoint,
            position=position,
        )

    def parseAnchorElement(self, elementNode):
        name = elementNode.get(GlyphTags.NAME)
        referenceName = elementNode.get(GlyphTags.REFRENCE_NAME)
        position = elementNode.get(GlyphTags.POSITION)
        return GlyphAnchorElementDescription(name, referenceName, position)

    def parseReferenceElement(self, elementNode):
        referenceName = elementNode.get(GlyphTags.REFRENCE_NAME)
        order = elementNode.get(GlyphTags.ORDER)
        position = elementNode.get(GlyphTags.POSITION)
        return GlyphReferenceElementDescription(referenceName, order, position)

    def parseElement(self, elementNode):
        method = elementNode.get(GlyphTags.METHOD)
        element = GlyphElementDescription(method)

        if method == GlyphTags.METHOD__DEFINITION:
            element = self.parseDefinitionElement(elementNode)
        elif method == GlyphTags.METHOD__ANCHOR:
            element = self.parseAnchorElement(elementNode)
        elif method == GlyphTags.METHOD__REFERENCE:
            element = self.parseReferenceElement(elementNode)

        return element

    def parseStroke(self, strokeNode):
        strokeName = strokeNode.get(GlyphTags.NAME)
        strokeComment = strokeNode.get(GlyphTags.COMMENT)

        stroke = GlyphStrokeDescription(strokeName, strokeComment)

        elementNode = strokeNode.get(GlyphTags.STROKE)
        element = self.parseElement(elementNode)

        stroke.element = element
        return stroke

    def parseComponent(self, componentNode):
        componentName = componentNode.get(GlyphTags.NAME)
        componentComment = componentNode.get(GlyphTags.COMMENT)

        component = GlyphComponentDescription(componentName, componentComment)

        elements = []
        for elementNode in componentNode.get(GlyphTags.STROKE):
            element = self.parseElement(elementNode)
            elements.append(element)

        component.elements = elements
        return component

    def parseDataSet(self, dataSetNode):
        components = []
        for componentNode in dataSetNode:
            component = self.parseComponent(componentNode)
            components.append(component)

        return components

    def parseAllDataSet(self, rootNode):
        strokeSetNode = rootNode.get(GlyphTags.STROKE_SET)
        strokes = []
        for strokeNode in strokeSetNode:
            stroke = self.parseStroke(strokeNode)
            strokes.append(stroke)

        partSetNode = rootNode.get(GlyphTags.PART_SET)
        parts = self.parseDataSet(partSetNode)

        componentSetNode = rootNode.get(GlyphTags.COMPONENT_SET)
        components = self.parseDataSet(componentSetNode)

        dataSet = GlyphDataSetDescription(strokes, parts, components)
        return dataSet


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
