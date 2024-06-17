from parser.model import SubstituteRuleMatchingModel
from parser.model import SubstituteRuleModel
from parser.model import SubstituteRuleSetModel

from tree.regexp.item import TreeRegExp
from tree.regexp import compile


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

        self.__replacement = model.replacement
        self.__tre = compile(pattern)

    @property
    def tre(self):
        return self.__tre

    @property
    def replacement(self):
        return self.__replacement


class SubstituteRuleSet:
    def __init__(self, model: SubstituteRuleSetModel):
        self.rules = tuple(SubstituteRule(model=ruleModel) for ruleModel in model.rules)
