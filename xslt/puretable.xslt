<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:param name="type" select="'all'" />
  <xsl:param name="main" select="'keybinding'" />
  <xsl:param name="onlycharacter" select="'true'" />

  <xsl:output method="text" encoding="UTF-8" indent="yes"/>

  <xsl:variable name='tab'><xsl:text>	</xsl:text></xsl:variable>
  <xsl:variable name='space'><xsl:text> </xsl:text></xsl:variable>
  <xsl:variable name='newline'><xsl:text>
</xsl:text></xsl:variable>

  <xsl:template match="/">
    <xsl:call-template name="輸出編碼對應"/>
  </xsl:template>

  <xsl:template name="輸出標题">
  </xsl:template>

  <xsl:template name="輸出設定">
  </xsl:template>

  <xsl:template name="輸出按鍵對應">
  </xsl:template>

  <xsl:template name="輸出編碼對應">
    <xsl:choose>
      <xsl:when test="($main = 'character')">
        <xsl:apply-templates select="輸入法/對應集/對應">
          <xsl:sort select="@字符"/>
        </xsl:apply-templates>
      </xsl:when>
      <xsl:otherwise>
        <xsl:apply-templates select="輸入法/對應集/對應">
          <xsl:sort select="@按鍵序列"/>
        </xsl:apply-templates>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="對應">
    <xsl:choose>
      <xsl:when test="($onlycharacter = 'false')">
        <xsl:call-template name="輸出對應-判斷類型"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:if test="string-length(@字符) = 1">
          <xsl:call-template name="輸出對應-判斷類型"/>
        </xsl:if>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="輸出對應-判斷類型">
    <xsl:choose>
      <xsl:when test="($type = 'standard')">
        <xsl:if test="@類型 = '標準'">
          <xsl:call-template name="輸出對應"/>
        </xsl:if>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="輸出對應"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="輸出對應">
    <xsl:choose>
      <xsl:when test="($main = 'character')">
        <xsl:value-of select="@字符"/>
        <xsl:value-of select="$tab"/>
        <xsl:value-of select="@按鍵序列"/>
        <xsl:value-of select="$newline"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="@按鍵序列"/>
        <xsl:value-of select="$tab"/>
        <xsl:value-of select="@字符"/>
        <xsl:value-of select="$newline"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
</xsl:stylesheet>

