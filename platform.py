
class NonePlatform:

    def __init__(self, im):
        self.im=im
        self.cmfmt='{0}\t{1}'
        self.fmt='{0} {1}'

        self.strBeginTable=""
        self.strEndTable=""

    def keyMappings(self):
	    # 要求 self.im.keyMaps 的格式為
	    # [  [按鍵一, 提示一],
	    #    [按鍵二, 提示二],
	    #    [按鍵三, 提示三],
	    # ]
	    return map(lambda x: self.fmt.format(*x), self.im.keyMaps)

    def genCodeMappingsTable(self, cm):
	    return "\n".join(sorted(map(lambda x : self.cmfmt.format(*x), cm)))

    def genKeyMappings(self):
	    return "\n".join(self.keyMappings())

    def genHeader(self):
	    return ""

class ScimPlatform(NonePlatform):
    def __init__(self, im):
        self.im=im
        self.cmfmt='{0}\t{1}'
        self.fmt='{0} {1}'

        self.strBeginTable="BEGIN_TABLE"
        self.strEndTable="END_TABLE"

    def genKeyMappings(self):
        return 'BEGIN_CHAR_PROMPTS_DEFINITION\n' + \
            '\n'.join(self.keyMappings()) + \
            '\nEND_CHAR_PROMPTS_DEFINITION\n'

    def genHeader(self):
	    return """SCIM_Generic_Table_Phrase_Library_TEXT
VERSION_1_0

BEGIN_DEFINITION

UUID = {{ uuid }}

SERIAL_NUMBER = {{ datestamp }}

ICON = @SCIM_ICONDIR@/CangJie.png

NAME = {{ SRF.name }}

NAME.zh_CN = {{ SRF.name_cn }}
NAME.zh_TW = {{ SRF.name_tw }}
NAME.zh_HK = {{ SRF.name_hk }}

LANGUAGES = zh_TW,zh_HK,zh_CN,zh_SG

STATUS_PROMPT = 中

KEYBOARD_LAYOUT = US_Default

AUTO_SELECT = FALSE

AUTO_WILDCARD = TRUE

AUTO_COMMIT = FALSE

AUTO_SPLIT = TRUE

DYNAMIC_ADJUST = FALSE

AUTO_FILL = FALSE

ALWAYS_SHOW_LOOKUP = TRUE

DEF_FULL_WIDTH_PUNCT = TRUE

DEF_FULL_WIDTH_LETTER = FALSE

MAX_KEY_LENGTH = 5

VALID_INPUT_CHARS = abcdefghijklmnopqrstuvwxyz

MULTI_WILDCARD_CHAR = *

SPLIT_KEYS = quoteright

COMMIT_KEYS = space

FORWARD_KEYS = Return

SELECT_KEYS = 1,2,3,4,5,6,7,8,9,0

PAGE_UP_KEYS = Page_Up,comma,minus

PAGE_DOWN_KEYS = Page_Down,period,equal

"""+self.genKeyMappings()+"END_DEFINITION\n"

class GcinPlatform(NonePlatform):
    def __init__(self, im):
        self.im=im
        self.cmfmt='{0}\t{1}'
        self.fmt='{0} {1}'

        self.strBeginTable="%chardef begin"
        self.strEndTable="%chardef end"

    def genKeyMappings(self):
        return '%keyname begin\n' + \
            '\n'.join(self.keyMappings()) + \
            '\n%keyname end\n'

    def genHeader(self):
	    return """# 瑲珩
%gen_inp
%ename {{ SRF.name_en }}
%cname {{ SRF.name_tw }}
%selkey 1234567890
%space_style 4
"""+self.genKeyMappings()

class MSimPlatform(NonePlatform):
    def __init__(self, im):
        self.im=im
        self.cmfmt='{0} {1}'
        self.fmt='/S {0}{1}'

        self.strBeginTable=""
        self.strEndTable=""

    def genKeyMappings(self):
        return '\n'.join(self.keyMappings())

    def genHeader(self):
        return self.genKeyMappings()

if __name__=='__main__':
    pass
