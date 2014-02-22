
class NonePlatform:
    def __init__(self):
        self.strBeginTable=""
        self.strEndTable=""

    def genHeader(self):
	    return ""

class ScimPlatform(NonePlatform):
    def __init__(self):
        self.strBeginTable="BEGIN_TABLE"
        self.strEndTable="END_TABLE"

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

BEGIN_CHAR_PROMPTS_DEFINITION
a 日
b 月
c 金
d 木
e 水
f 火
g 土
h 竹
i 戈
j 十
k 大
l 中
m 一
n 弓
o 人
p 心
q 手
r 口
s 尸
t 廿
u 山
v 女
w 田
x 難
y 卜
z 符
END_CHAR_PROMPTS_DEFINITION
END_DEFINITION"""

class GcinPlatform(NonePlatform):
    def __init__(self):
        self.strBeginTable="%chardef begin"
        self.strEndTable="%chardef end"

    def genHeader(self):
	    return """# 瑲珩
%gen_inp
%ename {{ SRF.name_en }}
%cname {{ SRF.name_tw }}
%selkey 1234567890
%space_style 4
%keyname begin
a 日
b 月
c 金
d 木
e 水
f 火
g 土
h 竹
i 戈
j 十
k 大
l 中
m 一
n 弓
o 人
p 心
q 手
r 口
s 尸
t 廿
u 山
v 女
w 田
x 難
y 卜
z 符
%keyname end
"""

class MSimPlatform(NonePlatform):
    def __init__(self):
        self.strBeginTable=""
        self.strEndTable=""

    def genHeader(self):
	    return """/S A日
/S B月
/S C金
/S D木
/S E水
/S F火
/S G土
/S H竹
/S I戈
/S J十
/S K大
/S L中
/S M一
/S N弓
/S O人
/S P心
/S Q手
/S R口
/S S尸
/S T廿
/S U山
/S V女
/S W田
/S X難
/S Y卜
/S Z符"""

if __name__=='__main__':
    pass
