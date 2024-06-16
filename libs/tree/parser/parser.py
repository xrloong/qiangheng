import ply.lex as lex
import ply.yacc as yacc

from ..node import Node

tokens = (
    "NAME",
    "PARENTHESIS_LEFT",
    "PARENTHESIS_RIGHT",
    "BRACE_LEFT",
    "BRACE_RIGHT",
    "EQUAL",
    "BACK_REFERENCE_EXPRESSION",
)

t_NAME = r"([一-龥㐀-䶵]+|\[[一-龥㐀-䶵]+\])(\.[0-9])?"
t_PARENTHESIS_LEFT = r"\("
t_PARENTHESIS_RIGHT = r"\)"
t_BRACE_LEFT = r"\{"
t_BRACE_RIGHT = r"\}"
t_EQUAL = r" = "
t_BACK_REFERENCE_EXPRESSION = r"\\[0-9]+(\.[0-9]+)?"

t_ignore = " \t"


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def p_node(t):
    """node : NAME
    | BACK_REFERENCE_EXPRESSION
    | PARENTHESIS_LEFT PARENTHESIS_RIGHT
    | PARENTHESIS_LEFT prop node_list PARENTHESIS_RIGHT
    | PARENTHESIS_LEFT prop PARENTHESIS_RIGHT"""
    if len(t) == 2:
        if t[1][0] == "\\":
            backRefExp = t[1]
            node = Node(backRefExp=backRefExp)
        else:
            prop = Node.genProp(name=t[1])
            node = Node(prop=prop)
        t[0] = node

    if len(t) == 3:
        node = Node()
        t[0] = node

    if len(t) == 4:
        prop = t[2]

        node = Node(prop=prop)

        t[0] = node

    if len(t) == 5:
        prop = t[2]
        nodes = t[3]

        node = Node(prop=prop, children=nodes)

        t[0] = node


def p_node_list(t):
    """node_list : node
    | node node_list"""
    if len(t) == 2:
        t[0] = (t[1],)
    if len(t) == 3:
        t[0] = (t[1],) + t[2]


def p_attrib(t):
    "attrib : NAME EQUAL NAME"
    t[0] = {t[1]: t[3]}


def p_prop(t):
    """prop : NAME
    | BRACE_LEFT attrib BRACE_RIGHT"""

    if len(t) == 2:
        prop = Node.genProp(operator=t[1])
        t[0] = prop
    if len(t) == 4:
        t[0] = t[2]


def p_error(t):
    print("Syntax error at '%s'" % t.value)


def parse(expression, supportBackReference: bool = False) -> Node:
    node = parser.parse(expression, lexer=lexer)

    if not supportBackReference:
        assert node.hasBackRef is False

    return node


lexer = lex.lex()
parser = yacc.yacc()
