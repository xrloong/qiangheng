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
      <xsl:value-of select="版本號" />
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
          <xsl:value-of select="$newline" />

          <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
          <xsl:text>名稱: </xsl:text>
          <xsl:text>"</xsl:text>
          <xsl:value-of select="@名稱" />
          <xsl:text>"</xsl:text>
          <xsl:value-of select="$newline" />

          <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
          <xsl:text>註記: </xsl:text>
          <xsl:value-of select="@註記" />
          <xsl:value-of select="$newline" />

          <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
          <xsl:text>編碼資訊: </xsl:text>
          <xsl:value-of select="$newline" />


    <xsl:for-each select="編碼資訊">
          <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
          <xsl:value-of select="$itemmark" />
          <xsl:value-of select="$newline" />

          <xsl:apply-templates select="組字"/> 
          <xsl:if test="編碼/@資訊表示式">
            <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
            <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
            <xsl:text>資訊表示式: </xsl:text>
            <xsl:value-of select="編碼/@資訊表示式" />
            <xsl:value-of select="$newline" />
          </xsl:if>

          <xsl:if test="@類型">
            <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
            <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
            <xsl:text>類型: </xsl:text>
            <xsl:value-of select="@類型" />
            <xsl:value-of select="$newline" />
          </xsl:if>

          <xsl:if test="@字符碼">
            <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
            <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
            <xsl:text>字符碼: </xsl:text>
            <xsl:value-of select="@字符碼" />
            <xsl:value-of select="$newline" />
          </xsl:if>

          <xsl:if test="@字根碼">
            <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
            <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
            <xsl:text>字根碼: </xsl:text>
            <xsl:value-of select="@字根碼" />
            <xsl:value-of select="$newline" />
          </xsl:if>

          <xsl:if test="@補充資訊">
            <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
            <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
            <xsl:text>補充資訊: </xsl:text>
            <xsl:value-of select="編碼/@補充資訊" />
            <xsl:value-of select="$newline" />
          </xsl:if>
    </xsl:for-each>

        </xsl:if>
    </xsl:for-each>
<!--
    <xsl:for-each select="字符">
    </xsl:for-each>
-->
  </xsl:template>
 
  <xsl:template match="comment()">
    <xsl:text># </xsl:text><xsl:value-of select="." />
    <xsl:value-of select="$newline" />
  </xsl:template>

  <xsl:template match="組字">
    <xsl:text>(</xsl:text>
    <xsl:value-of select="@運算" />
      <xsl:if test="組字|字根">
        <xsl:text> </xsl:text>
      </xsl:if>
      <xsl:for-each select="組字|字根">
        <xsl:if test="self::組字">
          <xsl:apply-templates select="self::組字"/> 
        </xsl:if>
        <xsl:if test="self::字根">
          <xsl:apply-templates select="self::字根"/> 
        </xsl:if>
      </xsl:for-each>
    <xsl:text>)</xsl:text>
  </xsl:template>

  <xsl:template match="字根">
    <xsl:value-of select="@名稱" />
  </xsl:template>
</xsl:stylesheet>


