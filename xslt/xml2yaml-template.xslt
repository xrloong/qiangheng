<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
    xmlns:exsl="http://exslt.org/common"
    >
  <xsl:output method="text"/>
  <xsl:variable name='intent'><xsl:text>  </xsl:text></xsl:variable>
  <xsl:variable name='itemmark'><xsl:text>- </xsl:text></xsl:variable>
  <xsl:variable name='comment'><xsl:text># </xsl:text></xsl:variable>
  <xsl:variable name='tab'><xsl:text>	</xsl:text></xsl:variable>
  <xsl:variable name='newline'><xsl:text>
</xsl:text></xsl:variable>

  <xsl:template match="/瑲珩">
    <xsl:apply-templates select="規則集"/>
  </xsl:template>

  <xsl:template match="規則集">
    <xsl:text>規則集: </xsl:text>
    <xsl:value-of select="$newline" />
    <xsl:for-each select="規則|comment()">
        <xsl:if test="self::規則">
          <xsl:value-of select="$intent" />
          <xsl:value-of select="$itemmark" />
          <xsl:text>比對: </xsl:text>
          <xsl:call-template name="generate-規則" />
          <xsl:value-of select="$newline" />

          <xsl:value-of select="$intent" />
          <xsl:value-of select="$intent" />
          <xsl:text>替換: </xsl:text>
          <xsl:value-of select="@替換" />
          <xsl:value-of select="$newline" />

        </xsl:if>
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="comment()">
    <xsl:text># </xsl:text><xsl:value-of select="." />
    <xsl:value-of select="$newline" />
  </xsl:template>

  <xsl:template name="generate-規則">
    <xsl:param name="param_count" select="@參數個數" />
    <xsl:text>({運算=</xsl:text>
    <xsl:value-of select="@運算" />
    <xsl:text>}</xsl:text>
      <xsl:for-each select="(//node())[$param_count >= position()]"> .</xsl:for-each>
    <xsl:text>)</xsl:text>
  </xsl:template>
</xsl:stylesheet>

