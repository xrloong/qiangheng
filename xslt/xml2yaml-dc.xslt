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
      <xsl:apply-templates select="重設字符集"/>
      <xsl:apply-templates select="字符集"/> 
    </root>
  </xsl:template>
 
  <xsl:template match="重設字符集">
    <xsl:text>重設字符集: </xsl:text>
    <xsl:value-of select="$newline" />
    <xsl:for-each select="字符|comment()">
      <xsl:value-of select="$intent" />
      <xsl:value-of select="$itemmark" />
      <xsl:text>"</xsl:text>
      <xsl:value-of select="@名稱" />
      <xsl:text>"</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
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

          <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
          <xsl:text>編碼資訊: </xsl:text>
          <xsl:value-of select="$newline" />

          <xsl:for-each select="編碼資訊">
            <xsl:for-each select="編碼/@*">
              <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
              <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
              <xsl:value-of select="name()"/> 
              <xsl:text>: </xsl:text>
              <xsl:value-of select="." />
              <xsl:value-of select="$newline" />
            </xsl:for-each>

            <xsl:for-each select="./@*">
              <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
              <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
              <xsl:value-of select="name()"/> 
              <xsl:text>: </xsl:text>
              <xsl:value-of select="." />
              <xsl:value-of select="$newline" />
            </xsl:for-each>

            <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
            <xsl:value-of select="$intent" /> <xsl:value-of select="$itemmark" />
            <xsl:text>資訊表示式: </xsl:text>
            <xsl:value-of select="$newline" />
            <xsl:for-each select="筆劃組">
              <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
              <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
              <xsl:value-of select="$intent" /> <xsl:value-of select="$itemmark" />
              <xsl:text>筆劃組: </xsl:text>
              <xsl:value-of select="$newline" />
              <xsl:for-each select="筆劃">
                <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
                <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
                <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
                <xsl:value-of select="$itemmark" />
                <xsl:text>"</xsl:text>
                <xsl:value-of select="@筆劃資訊"/> 
                <xsl:text>"</xsl:text>
                <xsl:value-of select="$newline" />
              </xsl:for-each>
              <xsl:if test="@名稱">
                <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
                <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
                <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
                <xsl:text>名稱: </xsl:text>
                <xsl:value-of select="@名稱"/> 
                <xsl:value-of select="$newline" />
              </xsl:if>

            <xsl:if test="補充範圍">
              <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
              <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
              <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
              <xsl:text>補充範圍: </xsl:text>
              <xsl:value-of select="$newline" />

              <xsl:for-each select="補充範圍">
                <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
                <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
                <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
                <xsl:value-of select="$intent" /> <xsl:value-of select="$itemmark" />
                <xsl:text>{</xsl:text>
                <xsl:text>名稱: </xsl:text>
                <xsl:text>"</xsl:text>
                <xsl:value-of select="@名稱"/> 
                <xsl:text>"</xsl:text>
                <xsl:text>, </xsl:text>
                <xsl:text>範圍: </xsl:text>
                <xsl:value-of select="幾何/@範圍"/> 
                <xsl:text>}</xsl:text>
                <xsl:value-of select="$newline" />
              </xsl:for-each>
            </xsl:if>
            </xsl:for-each>

          </xsl:for-each>
        </xsl:if>
    </xsl:for-each>
  </xsl:template>
 
  <xsl:template match="comment()">
    <xsl:text># </xsl:text><xsl:value-of select="." />
    <xsl:value-of select="$newline" />
  </xsl:template>
</xsl:stylesheet>
