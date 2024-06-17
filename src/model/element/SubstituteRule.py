from parser.model import SubstituteRuleMatchingModel
from parser.model import SubstituteRuleModel
from parser.model import SubstituteRuleSetModel

from tree.regexp import compile

from tree.node import Node as TreeExpression
from tree.parser import TreeParser


class SubstituteRule:
    def __init__(self, model: SubstituteRuleModel):
        matching = model.matching
        if isinstance(matching, SubstituteRuleMatchingModel):
            modelMatching = matching
            operator = modelMatching.operator
            operandCount = modelMatching.operandCount
            expression = " ".join("." for _ in range(operandCount))
            pattern = "({{運算={name}}} {exp})".format(name=operator, exp=expression)
        else:
            pattern = matching

        goal: TreeExpression = TreeParser.parse(
            model.replacement, supportBackReference=True
        )
        self.__goal = goal
        self.__tre = compile(pattern)

    @property
    def tre(self):
        return self.__tre

    @property
    def goal(self) -> TreeExpression:
        return self.__goal


class SubstituteRuleSet:
    def __init__(self, model: SubstituteRuleSetModel):
        self.rules = tuple(SubstituteRule(model=ruleModel) for ruleModel in model.rules)
