from parser.model import SubstituteRuleMatchingModel
from parser.model import SubstituteRuleModel
from parser.model import SubstituteRuleSetModel

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
        self.pattern = pattern

        self.replacement = model.replacement
        self.tre = compile(self.pattern)

    def getPattern(self):
        return self.pattern

    def getReplacement(self):
        return self.replacement

    def getTRE(self):
        return self.tre


class SubstituteRuleSet:
    def __init__(self, model: SubstituteRuleSetModel):
        self.rules = tuple(SubstituteRule(model=ruleModel) for ruleModel in model.rules)
