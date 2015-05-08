<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:param name="type" select="'all'" />
  <xsl:param name="onlycharacter" select="'true'" />

  <xsl:output method="text" encoding="UTF-8" indent="yes"/>

  <xsl:variable name='tab'><xsl:text>	</xsl:text></xsl:variable>
  <xsl:variable name='space'><xsl:text> </xsl:text></xsl:variable>
  <xsl:variable name='newline'><xsl:text>
</xsl:text></xsl:variable>

  <xsl:template match="/">
    <xsl:call-template name="輸出描繪對應"/>
  </xsl:template>

  <xsl:template name="輸出描繪對應">
    <xsl:apply-templates select="描繪法/字圖集/字圖">
      <xsl:sort select="@名稱"/>
    </xsl:apply-templates>
  </xsl:template>

  <xsl:template match="字圖">
    <xsl:choose>
      <xsl:when test="($onlycharacter = 'false')">
        <xsl:call-template name="輸出描繪-判斷類型"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:if test="string-length(@名稱) = 1">
          <xsl:call-template name="輸出描繪-判斷類型"/>
        </xsl:if>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="輸出描繪-判斷類型">
    <xsl:choose>
      <xsl:when test="($type = 'standard')">
        <xsl:if test="@類型 = '標準'">
          <xsl:call-template name="輸出描繪"/>
        </xsl:if>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="輸出描繪"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="輸出描繪">
    <xsl:value-of select="@名稱"/>
    <xsl:value-of select="$tab"/>
    <xsl:for-each select="筆劃">
      <xsl:if test="position()>1">
        <xsl:text>;</xsl:text>
      </xsl:if>
      <xsl:value-of select="@描繪"/>
    </xsl:for-each>
    <xsl:value-of select="$newline"/>
  </xsl:template>
</xsl:stylesheet>

