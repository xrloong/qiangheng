<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <!--
	Python 的 ElementTree 目前的 XML 輸出沒有很好，
	所以使用此 XSLT 轉換成較好的格式。
   -->

  <xsl:output method="xml" encoding="UTF-8" indent="yes"/>
  <xsl:variable name='tab'><xsl:text>	</xsl:text></xsl:variable>
  <xsl:variable name='newline'><xsl:text>
</xsl:text></xsl:variable>

  <xsl:template match="/">
    <xsl:apply-templates select="對應集" />
  </xsl:template>
 
  <xsl:template match="對應集">
    <xsl:copy><xsl:value-of select="$newline" />
      <xsl:for-each select="對應">
        <xsl:sort select="@按鍵"/>
        <xsl:value-of select="$tab" />
        <xsl:copy-of select="."/>
        <xsl:value-of select="$newline" />
      </xsl:for-each>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>

