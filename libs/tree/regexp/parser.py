import ply.lex as lex
import ply.yacc as yacc

from .item import TreeRegExp

tokens = (
    "NAME",
    "PARENTHESIS_LEFT",
    "PARENTHESIS_RIGHT",
    "BRACE_LEFT",
    "BRACE_RIGHT",
    "BACKREF_LEFT",
    "BACKREF_RIGHT",
    "STAR",
    "DOT",
    "EQUAL",
)

t_NAME = r"[一-龥㐀-䶵\[\]][一-龥㐀-䶵\[\]\.0-9]*"
t_PARENTHESIS_LEFT = r"\("
t_PARENTHESIS_RIGHT = r"\)"
t_BRACE_LEFT = r"\{"
t_BRACE_RIGHT = r"\}"
t_BACKREF_LEFT = r"\\\("
t_BACKREF_RIGHT = r"\\\)"
t_STAR = r"\*"
t_DOT = r"\."
t_EQUAL = r" = "

t_ignore = " \t"


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def p_node(t):
    """node : PARENTHESIS_LEFT prop PARENTHESIS_RIGHT
    | PARENTHESIS_LEFT prop re_list PARENTHESIS_RIGHT"""
    if len(t) == 4:
        current = TreeRegExp()
        current.updateProp(t[2])

        t[0] = current

    if len(t) == 5:
        current = TreeRegExp()
        current.updateProp(t[2])
        current.setChildren(t[3])

        t[0] = current


def p_re(t):
    """re : node
    | DOT
    | re STAR
    | BACKREF_LEFT re_list BACKREF_RIGHT"""
    if len(t) == 2:
        if isinstance(t[1], TreeRegExp):
            node = t[1]
            t[0] = node
        else:
            # dot
            token = TreeRegExp.generateDot()
            t[0] = token

    if len(t) == 3:
        t[0] = t[1]
        t[0].setWithStar()


def p_re_list(t):
    """re_list : re
    | re re_list"""
    if len(t) == 2:
        t[0] = [t[1]]
    if len(t) == 3:
        t[0] = [t[1]] + t[2]


def p_attrib(t):
    "attrib : NAME EQUAL NAME"
    t[0] = {t[1]: t[3]}


def p_prop(t):
    """prop : BRACE_LEFT attrib BRACE_RIGHT
    | BRACE_LEFT BRACE_RIGHT
    |
    """
    if len(t) == 4:
        t[0] = t[2]
    else:
        t[0] = {}


def p_error(t):
    print("Syntax error at '%s'" % t.value)


def compile(expression):
    return parser.parse(expression, lexer=lexer)


lexer = lex.lex()
parser = yacc.yacc()
