import uuid, datetime

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
	    return "\n".join(list(map(lambda x : self.cmfmt.format(*x), cm)))
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
	    return "SCIM_Generic_Table_Phrase_Library_TEXT\n" \
	    + "VERSION_1_0\n\n" \
	    + "BEGIN_DEFINITION\n\n" \
	    + "UUID = %s\n\n"%str(uuid.uuid4()) \
	    + "SERIAL_NUMBER = %s\n\n"%datetime.date.today().strftime("%Y%m%d") \
	    + "ICON = @SCIM_ICONDIR@/%s\n\n"%self.im.getIconFileName() \
	    + "NAME = %s\n\n"%self.im.getName('en') \
	    + "NAME.zh_CN = %s\n\n"%self.im.getName('cn') \
	    + "NAME.zh_TW = %s\n\n"%self.im.getName('tw') \
	    + "NAME.zh_HK = %s\n\n"%self.im.getName('hk') \
	    + "LANGUAGES = zh_TW,zh_HK,zh_CN,zh_SG\n\n" \
	    + "STATUS_PROMPT = 中\n\n" \
	    + "KEYBOARD_LAYOUT = US_Default\n\n" \
	    + "AUTO_SELECT = FALSE\n\n" \
	    + "AUTO_WILDCARD = TRUE\n\n" \
	    + "AUTO_COMMIT = FALSE\n\n" \
	    + "AUTO_SPLIT = TRUE\n\n" \
	    + "DYNAMIC_ADJUST = FALSE\n\n" \
	    + "AUTO_FILL = FALSE\n\n" \
	    + "ALWAYS_SHOW_LOOKUP = TRUE\n\n" \
	    + "DEF_FULL_WIDTH_PUNCT = TRUE\n\n" \
	    + "DEF_FULL_WIDTH_LETTER = FALSE\n\n" \
	    + "MAX_KEY_LENGTH = %s\n\n"%self.im.getMaxKeyLength() \
	    + "VALID_INPUT_CHARS = %s\n\n"%self.im.getKeyList() \
	    + "MULTI_WILDCARD_CHAR = *\n\n" \
	    + "SPLIT_KEYS = quoteright\n\n" \
	    + "COMMIT_KEYS = space\n\n" \
	    + "FORWARD_KEYS = Return\n\n" \
	    + "SELECT_KEYS = 1,2,3,4,5,6,7,8,9,0\n\n" \
	    + "PAGE_UP_KEYS = Page_Up,comma,minus\n\n" \
	    + "PAGE_DOWN_KEYS = Page_Down,period,equal\n\n" \
	    + self.genKeyMappings() \
	    + "END_DEFINITION\n"

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
	    return "# 瑲珩\n" \
	    + "%%gen_inp\n" \
	    + "%%ename %s\n"%self.im.getName('en') \
	    + "%%cname %s\n"%self.im.getName('tw') \
	    + "%%selkey 1234567890\n" \
	    + "%%space_style 4\n" \
	    + self.genKeyMappings()

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
