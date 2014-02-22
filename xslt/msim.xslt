<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="text" encoding="UTF-8" indent="yes"/>

  <xsl:variable name='tab'><xsl:text>	</xsl:text></xsl:variable>
  <xsl:variable name='space'><xsl:text> </xsl:text></xsl:variable>
  <xsl:variable name='newline'><xsl:text>
</xsl:text></xsl:variable>

  <xsl:template match="/">
    <xsl:for-each select="輸入法/按鍵對應集/按鍵對應">
      <xsl:apply-templates select="."/>
    </xsl:for-each>
    <xsl:for-each select="輸入法/對應集/對應">
      <xsl:sort select="@按鍵序列"/>
      <xsl:apply-templates select="."/>
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="按鍵對應">
    <xsl:text>/S</xsl:text>
    <xsl:value-of select="$space"/>
    <xsl:value-of select="@按鍵"/>
    <xsl:value-of select="@顯示"/>
    <xsl:value-of select="$newline"/>
  </xsl:template>

  <xsl:template match="對應">
    <xsl:call-template name="編碼對應">
      <xsl:with-param name="鍵"><xsl:value-of select="@按鍵序列"/></xsl:with-param>
      <xsl:with-param name="值"><xsl:value-of select="@字符"/></xsl:with-param>
    </xsl:call-template>
  </xsl:template>

  <xsl:template name="編碼對應">
    <xsl:param name="鍵"/>
    <xsl:param name="值"/>
    <xsl:value-of select="$鍵"/>
    <xsl:value-of select="$space"/>
    <xsl:value-of select="$值"/>
    <xsl:value-of select="$newline"/>
  </xsl:template>
</xsl:stylesheet>

