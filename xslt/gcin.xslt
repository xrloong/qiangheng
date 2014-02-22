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
    <xsl:text>%</xsl:text>
    <xsl:value-of select="$選項"/>
    <xsl:value-of select="$space"/>
    <xsl:value-of select="$值"/>
    <xsl:value-of select="$newline"/>
  </xsl:template>

  <xsl:template name="輸出標题">
    <xsl:text>%gen_inp</xsl:text>
    <xsl:value-of select="$newline"/>
  </xsl:template>

  <xsl:template name="輸出設定">
    <xsl:call-template name="設定">
      <xsl:with-param name="選項">ename</xsl:with-param>
      <xsl:with-param name="值"><xsl:value-of select="輸入法/輸入法名稱/@EN"/></xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">cname</xsl:with-param>
      <xsl:with-param name="值"><xsl:value-of select="輸入法/輸入法名稱/@TW"/></xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">selkey</xsl:with-param>
      <xsl:with-param name="值">1234567890</xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="設定">
      <xsl:with-param name="選項">space_style</xsl:with-param>
      <xsl:with-param name="值">4</xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="輸出按鍵對應"/>
  </xsl:template>

  <xsl:template name="輸出按鍵對應">
    <xsl:text>%keyname begin</xsl:text><xsl:value-of select="$newline"/>
    <xsl:apply-templates select="輸入法/按鍵對應集/按鍵對應">
      <xsl:sort select="@按鍵"/>
    </xsl:apply-templates>
    <xsl:text>%keyname end</xsl:text><xsl:value-of select="$newline"/>
  </xsl:template>

  <xsl:template name="輸出編碼對應">
    <xsl:text>%chardef begin</xsl:text><xsl:value-of select="$newline"/>
    <xsl:apply-templates select="輸入法/對應集/對應">
      <xsl:sort select="@按鍵序列"/>
    </xsl:apply-templates>
    <xsl:text>%chardef end</xsl:text><xsl:value-of select="$newline"/>
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
    <xsl:value-of select="$newline"/>
  </xsl:template>

</xsl:stylesheet>

