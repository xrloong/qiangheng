<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="text" encoding="UTF-8" indent="yes"/>

  <xsl:variable name='tab'><xsl:text>	</xsl:text></xsl:variable>
  <xsl:variable name='space'><xsl:text> </xsl:text></xsl:variable>
  <xsl:variable name='newline'><xsl:text>
</xsl:text></xsl:variable>

  <xsl:param name="UUID"/>
  <xsl:param name="SERIAL"/>
  <xsl:param name="ICON_FILE"/>
  <xsl:param name="ICON_DIR"/>

  <xsl:template match="/">
    <xsl:call-template name="輸出標题"/>
    <xsl:call-template name="輸出設定"/>
    <xsl:value-of select="$newline"/>
    <xsl:call-template name="輸出編碼對應"/>
  </xsl:template>

  <xsl:template name="設定">
    <xsl:param name="選項"/>
    <xsl:param name="值"/>
    <xsl:value-of select="$選項"/>
    <xsl:text> = </xsl:text>
    <xsl:value-of select="$值"/>
    <xsl:value-of select="$newline"/>
  </xsl:template>

  <xsl:template name="輸出標题">
    <xsl:text>SCIM_Generic_Table_Phrase_Library_TEXT</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:text>VERSION_1_0</xsl:text>
    <xsl:value-of select="$newline"/>
    <xsl:value-of select="$newline"/>
  </xsl:template>

  <xsl:template name="輸出設定">
    <xsl:text>BEGIN_DEFINITION</xsl:text>
    <xsl:value-of select="$newline"/>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">UUID</xsl:with-param>
      <xsl:with-param name="值"><xsl:value-of select="$UUID"/></xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">SERIAL_NUMBER</xsl:with-param>
      <xsl:with-param name="值"><xsl:value-of select="$SERIAL"/></xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">ICON</xsl:with-param>
      <xsl:with-param name="值">
        <xsl:value-of select="$ICON_FILE"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">NAME</xsl:with-param>
      <xsl:with-param name="值"><xsl:value-of select="編碼法/輸入法名稱/@EN"/></xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">NAME.zh_CN</xsl:with-param>
      <xsl:with-param name="值"><xsl:value-of select="編碼法/輸入法名稱/@CN"/></xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">NAME.zh_TW</xsl:with-param>
      <xsl:with-param name="值"><xsl:value-of select="編碼法/輸入法名稱/@TW"/></xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">NAME.zh_HK</xsl:with-param>
      <xsl:with-param name="值"><xsl:value-of select="編碼法/輸入法名稱/@HK"/></xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">LANGUAGES</xsl:with-param>
      <xsl:with-param name="值">zh_TW,zh_HK,zh_CN,zh_SG</xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">STATUS_PROMPT</xsl:with-param>
      <xsl:with-param name="值">CN</xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">KEYBOARD_LAYOUT</xsl:with-param>
      <xsl:with-param name="值">US_Default</xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">AUTO_SELECT</xsl:with-param>
      <xsl:with-param name="值">FALSE</xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">AUTO_WILDCARD</xsl:with-param>
      <xsl:with-param name="值">TRUE</xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">AUTO_COMMIT</xsl:with-param>
      <xsl:with-param name="值">FALSE</xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">AUTO_SPLIT</xsl:with-param>
      <xsl:with-param name="值">TRUE</xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">DYNAMIC_ADJUST</xsl:with-param>
      <xsl:with-param name="值">FALSE</xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">AUTO_FILL</xsl:with-param>
      <xsl:with-param name="值">FALSE</xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">ALWAYS_SHOW_LOOKUP</xsl:with-param>
      <xsl:with-param name="值">TRUE</xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">DEF_FULL_WIDTH_PUNCT</xsl:with-param>
      <xsl:with-param name="值">TRUE</xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">DEF_FULL_WIDTH_LETTER</xsl:with-param>
      <xsl:with-param name="值">FALSE</xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">MAX_KEY_LENGTH</xsl:with-param>
      <xsl:with-param name="值"><xsl:value-of select="編碼法/屬性/@最大按鍵數"/></xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">VALID_INPUT_CHARS</xsl:with-param>
      <xsl:with-param name="值">
        <xsl:for-each select="編碼法/按鍵對應集/按鍵對應">
          <xsl:value-of select="@按鍵"/>
        </xsl:for-each>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">MULTI_WILDCARD_CHAR</xsl:with-param>
      <xsl:with-param name="值">*</xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">SPLIT_KEYS</xsl:with-param>
      <xsl:with-param name="值">quoteright</xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">COMMIT_KEYS</xsl:with-param>
      <xsl:with-param name="值">space</xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">FORWARD_KEYS</xsl:with-param>
      <xsl:with-param name="值">Return</xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">SELECT_KEYS</xsl:with-param>
      <xsl:with-param name="值">1,2,3,4,5,6,7,8,9,0</xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">PAGE_UP_KEYS</xsl:with-param>
      <xsl:with-param name="值">Page_Up,comma,minus</xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">PAGE_DOWN_KEYS</xsl:with-param>
      <xsl:with-param name="值">Page_Down,period,equal</xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="輸出按鍵對應"/>

    <xsl:text>END_DEFINITION</xsl:text>
    <xsl:value-of select="$newline"/>
  </xsl:template>

  <xsl:template name="輸出按鍵對應">
    <xsl:text>BEGIN_CHAR_PROMPTS_DEFINITION</xsl:text><xsl:value-of select="$newline"/>
    <xsl:apply-templates select="編碼法/按鍵對應集/按鍵對應">
      <xsl:sort select="@按鍵"/>
    </xsl:apply-templates>
    <xsl:text>END_CHAR_PROMPTS_DEFINITION</xsl:text><xsl:value-of select="$newline"/>
  </xsl:template>

  <xsl:template name="輸出編碼對應">
    <xsl:text>BEGIN_TABLE</xsl:text><xsl:value-of select="$newline"/>
    <xsl:apply-templates select="編碼法/編碼集/對應">
      <xsl:sort select="@按鍵序列"/>
    </xsl:apply-templates>
    <xsl:text>END_TABLE</xsl:text><xsl:value-of select="$newline"/>
  </xsl:template>

  <xsl:template match="按鍵對應">
    <xsl:value-of select="@按鍵"/>
    <xsl:value-of select="$space"/>
    <xsl:value-of select="@顯示"/>
    <xsl:value-of select="$newline"/>
  </xsl:template>

  <xsl:template match="對應">
    <xsl:value-of select="@按鍵序列"/>
    <xsl:value-of select="$tab"/>
    <xsl:value-of select="@字符"/>

    <xsl:if test="@頻率">
      <xsl:value-of select="$tab"/>
      <xsl:value-of select="@頻率"/>
    </xsl:if>

    <xsl:value-of select="$newline"/>
  </xsl:template>

</xsl:stylesheet>

