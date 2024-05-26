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
          <xsl:value-of select="$newline" />

            <xsl:value-of select="$intent" />
            <xsl:value-of select="$intent" />
            <xsl:value-of select="$intent" />
            <xsl:text>運算: </xsl:text>
            <xsl:text>"</xsl:text>
            <xsl:value-of select="@運算" />
            <xsl:text>"</xsl:text>
            <xsl:value-of select="$newline" />

            <xsl:value-of select="$intent" />
            <xsl:value-of select="$intent" />
            <xsl:value-of select="$intent" />
            <xsl:text>參數個數: </xsl:text>
            <xsl:value-of select="@參數個數" />
            <xsl:value-of select="$newline" />

          <xsl:value-of select="$intent" />
          <xsl:value-of select="$intent" />
          <xsl:text>替換: </xsl:text>
          <xsl:text>"</xsl:text>
          <xsl:call-template name="yamlescape">
            <xsl:with-param name="str" select="@替換" />
          </xsl:call-template>
          <xsl:text>"</xsl:text>
          <xsl:value-of select="$newline" />

        </xsl:if>
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="comment()">
    <xsl:text># </xsl:text><xsl:value-of select="." />
    <xsl:value-of select="$newline" />
  </xsl:template>

  <xsl:template name="yamlescape">
   <xsl:param name="str" select="."/>
    <xsl:choose>
      <xsl:when test="contains($str, '\')">
        <xsl:value-of select="concat(substring-before($str, '\'), '\\' )"/>
        <xsl:call-template name="yamlescape">
          <xsl:with-param name="str" select="substring-after($str, '\')"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
          <xsl:value-of select="$str"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
</xsl:stylesheet>

