<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="text"/>
  <xsl:variable name='intent'><xsl:text>  </xsl:text></xsl:variable>
  <xsl:variable name='itemmark'><xsl:text>- </xsl:text></xsl:variable>
  <xsl:variable name='comment'><xsl:text># </xsl:text></xsl:variable>
  <xsl:variable name='tab'><xsl:text>	</xsl:text></xsl:variable>
  <xsl:variable name='newline'><xsl:text>
</xsl:text></xsl:variable>

  <xsl:template match="/瑲珩">
    <root>
      <xsl:apply-templates select="字符集"/>
    </root>
  </xsl:template>

  <xsl:template match="字符集">
    <xsl:text>字符集: </xsl:text>
    <xsl:value-of select="$newline" />
    <xsl:for-each select="字符|comment()">
        <xsl:value-of select="$intent" />
        <xsl:if test="self::comment()">
          <xsl:value-of select="$comment" />
          <xsl:value-of select="." />
          <xsl:value-of select="$newline" />
        </xsl:if>
        <xsl:if test="self::字符">
          <xsl:value-of select="$itemmark" />
          <xsl:text>名稱: </xsl:text>
          <xsl:text>"</xsl:text>
          <xsl:value-of select="@名稱" />
          <xsl:text>"</xsl:text>
          <xsl:value-of select="$newline" />

          <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
          <xsl:text>註記: </xsl:text>
          <xsl:text>"</xsl:text>
          <xsl:value-of select="@註記" />
          <xsl:text>"</xsl:text>
          <xsl:value-of select="$newline" />

          <xsl:if test="組字">
            <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
            <xsl:text>結構集:</xsl:text>
            <xsl:value-of select="$newline" />
            <xsl:call-template name="generate-結構-top-字根"/>
          </xsl:if>
        </xsl:if>
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="comment()">
    <xsl:text># </xsl:text><xsl:value-of select="." />
    <xsl:value-of select="$newline" />
  </xsl:template>

  <xsl:template name="generate-結構-top-字根">
    <xsl:for-each select="組字">
      <xsl:value-of select="$intent" />
      <xsl:value-of select="$intent" />
      <xsl:value-of select="$itemmark" />

      <xsl:text>{</xsl:text>
      <xsl:text>結構: </xsl:text>
      <xsl:text>"</xsl:text>
        <xsl:call-template name="generate-結構-組字"/>
      <xsl:text>"</xsl:text>

      <xsl:if test="@字體">
        <xsl:text>, </xsl:text>
        <xsl:text>字體: </xsl:text>
        <xsl:text>"</xsl:text>
          <xsl:value-of select="@字體" />
        <xsl:text>"</xsl:text>
      </xsl:if>

      <xsl:text>}</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="generate-結構-組字">
    <xsl:text>(</xsl:text>
      <xsl:if test="@運算">
        <xsl:text>{</xsl:text>
        <xsl:text>運算=</xsl:text>
        <xsl:value-of select="@運算" />
        <xsl:text>}</xsl:text>
        <xsl:for-each select="字根|組字">
          <xsl:if test="name()='組字'">
            <xsl:call-template name="generate-結構-組字"/>
          </xsl:if>
          <xsl:if test="name()='字根'">
            <xsl:call-template name="generate-結構-字根"/>
          </xsl:if>
        </xsl:for-each>
      </xsl:if>
    <xsl:text>)</xsl:text>
  </xsl:template>

  <xsl:template name="generate-結構-字根">
    <xsl:text>(</xsl:text>
    <xsl:text>{</xsl:text>
    <xsl:text>置換=</xsl:text>
    <xsl:value-of select="@置換" />
    <xsl:text>}</xsl:text>
    <xsl:text>)</xsl:text>
  </xsl:template>
</xsl:stylesheet>

