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
    <root>
      <xsl:apply-templates select="範本集"/>
    </root>
  </xsl:template>

  <xsl:template match="範本集">
    <xsl:text>範本集: </xsl:text>
    <xsl:value-of select="$newline" />
    <xsl:for-each select="範本|comment()">
        <xsl:if test="self::範本">
          <xsl:value-of select="$intent" />
          <xsl:value-of select="$itemmark" />
          <xsl:text>名稱: </xsl:text>
          <xsl:text>"</xsl:text>
          <xsl:value-of select="@名稱" />
          <xsl:text>"</xsl:text>
          <xsl:value-of select="$newline" />

          <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
          <xsl:text>參數列: </xsl:text>
          <xsl:text>[</xsl:text>
          <xsl:for-each select="參數列/參數">
            <xsl:text>"</xsl:text>
            <xsl:value-of select="@名稱" />
            <xsl:text>"</xsl:text>
<!--
            <xsl:if test="position()!=last()">
              <xsl:text>, </xsl:text>
            </xsl:if>
-->
              <xsl:text>, </xsl:text>
          </xsl:for-each>
          <xsl:text>]</xsl:text>
          <xsl:value-of select="$newline" />

          <xsl:value-of select="$intent" />
          <xsl:value-of select="$intent" />
          <xsl:text>比對: </xsl:text>
          <xsl:call-template name="generate-比對" />

          <xsl:if test="組字結構/組字">
            <xsl:call-template name="generate-結構-top-組字" />
            <xsl:call-template name="generate-模式-top-組字">
              <xsl:with-param name="params" select="參數列"/>
            </xsl:call-template>
          </xsl:if>
        </xsl:if>
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="comment()">
    <xsl:text># </xsl:text><xsl:value-of select="." />
    <xsl:value-of select="$newline" />
  </xsl:template>

  <xsl:template name="generate-比對">
    <xsl:text>({運算=</xsl:text>
    <xsl:value-of select="@名稱" />
    <xsl:text>}</xsl:text>
    <xsl:text> </xsl:text>

    <xsl:for-each select="參數列/參數">
      <xsl:text>.</xsl:text>
      <xsl:if test="position()!=last()">
        <xsl:text> </xsl:text>
      </xsl:if>
    </xsl:for-each>
    <xsl:text>)</xsl:text>
    <xsl:value-of select="$newline" />
  </xsl:template>

  <xsl:template name="generate-結構-top-組字">
    <xsl:for-each select="組字結構/組字">
      <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
      <xsl:text>結構: </xsl:text>
      <xsl:text>"</xsl:text>
      <xsl:call-template name="generate-結構-組字" />
      <xsl:text>"</xsl:text>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="generate-結構-組字">
      <xsl:param name="params" />

      <xsl:text>(</xsl:text>
      <xsl:if test="@運算">
        <xsl:text>{</xsl:text>
        <xsl:text>運算=</xsl:text>
        <xsl:value-of select="@運算" />
        <xsl:text>}</xsl:text>
        <xsl:for-each select="字根|組字">
          <xsl:if test="name()='組字'">
            <xsl:call-template name="generate-結構-組字" />
          </xsl:if>
          <xsl:if test="name()='字根'">
            <xsl:call-template name="generate-結構-字根" />
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

  <xsl:template name="generate-模式-top-組字">
      <xsl:param name="params" />
    <xsl:for-each select="組字結構/組字">
      <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
      <xsl:text>模式: </xsl:text>
      <xsl:call-template name="generate-模式-組字">
        <xsl:with-param name="params" select="$params"/>
      </xsl:call-template>
      <xsl:value-of select="$newline" />
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="generate-模式-組字">
      <xsl:param name="params" />

      <xsl:if test="@運算">
        <xsl:text>(</xsl:text>
        <xsl:value-of select="@運算" />
        <xsl:text> </xsl:text>
        <xsl:for-each select="字根|組字">
          <xsl:if test="name()='組字'">
            <xsl:call-template name="generate-模式-組字">
              <xsl:with-param name="params" select="$params"/>
            </xsl:call-template>
          </xsl:if>
          <xsl:if test="name()='字根'">
            <xsl:call-template name="generate-模式-字根">
              <xsl:with-param name="params" select="$params"/>
            </xsl:call-template>
          </xsl:if>

          <xsl:if test="position()!=last()">
            <xsl:text> </xsl:text>
          </xsl:if>
        </xsl:for-each>
        <xsl:text>)</xsl:text>
      </xsl:if>
  </xsl:template>

  <xsl:template name="generate-模式-字根">
    <xsl:param name="params" />

    <xsl:variable name="name" select="@置換" />

    <xsl:variable name="position">
      <xsl:call-template name="find-position-and-replace">
        <xsl:with-param name="target" select="@置換"/>
        <xsl:with-param name="params" select="$params"/>
      </xsl:call-template>
    </xsl:variable>

    <xsl:choose>
      <xsl:when test="exsl:node-set($position)/result">
        <xsl:value-of select="exsl:node-set($position)/result" />
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$name" />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>


  <xsl:template name="find-position-and-replace">
    <xsl:param name="target" />
    <xsl:param name="params" />

    <xsl:for-each select="exsl:node-set($params)/參數">
      <xsl:if test="starts-with($target, @名稱)">
        <xsl:variable name='s'><xsl:text>\</xsl:text><xsl:number value="position()" /></xsl:variable>
        <result><xsl:call-template name="replace-string">
          <xsl:with-param name="text" select="$target"/>
          <xsl:with-param name="replace" select="@名稱" />
          <xsl:with-param name="with" select="$s"/>
        </xsl:call-template></result>
      </xsl:if>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="replace-string">
    <xsl:param name="text"/>
    <xsl:param name="replace"/>
    <xsl:param name="with"/>
    <xsl:choose>
      <xsl:when test="contains($text,$replace)">
        <xsl:value-of select="substring-before($text,$replace)"/>
        <xsl:value-of select="$with"/>
        <xsl:call-template name="replace-string">
          <xsl:with-param name="text" select="substring-after($text,$replace)"/>
          <xsl:with-param name="replace" select="$replace"/>
          <xsl:with-param name="with" select="$with"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$text"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
</xsl:stylesheet>

