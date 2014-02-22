<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="xml" encoding="UTF-8" indent="yes"/>
  <xsl:strip-space elements="*"/>
  <xsl:variable name="list" select="'一 丁 丂 七 丄 丅 丆 万 丈 三 上 下 丌 不 与 丏 丐 丑 丒 专 且 丕 世 丗 丘 丙 业 丛 东 丝 丞 丟 丠 人 亻 亼 亽 亾 从 刀 刁 刂 刃 刄 刅 勹 北 卨 卩 卪 卫 卬 卵 卶 口 句 吉 呆 哆 哆 土 士 壬 壭 夕 多 够 夠 夡 子 孚 孵 工 忄 懈 攵 敏 敶 木 東 柬 槑 殳 段 毈 水 氵 氶 氷 永 氺 洀 海 湎 爫 牛 牜 舟 般 見 角 解 阜 阝 陳 面 靣 靦 齒 齟 齣'" />

  <xsl:template match="/">
    <xsl:apply-templates select="瑲珩"/>
  </xsl:template>

  <xsl:template match="瑲珩">
    <xsl:copy>
      <xsl:attribute name="版本號">
        <xsl:value-of select="@版本號" />
      </xsl:attribute>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="範本集">
<!--
    <xsl:copy-of select="." />
-->
  </xsl:template>

  <xsl:template match="字符集">
    <xsl:copy>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="comment()">
    <xsl:comment><xsl:value-of select="."/></xsl:comment>
  </xsl:template>

  <xsl:template match="字符">
    <xsl:variable name="k" select="@名稱" />
    <xsl:if test="contains( 
    concat(' ', $list, ' '),
    concat(' ', $k, ' ')
  )">
      <xsl:copy-of select="." />
    </xsl:if>
  </xsl:template>

  <xsl:template match="組字">
    <xsl:copy-of select="." />
  </xsl:template>

  <xsl:template match="套用範本">
    <組字>
      <xsl:attribute name="運算">
        <xsl:value-of select="@範本名稱" />
      </xsl:attribute>
      <xsl:attribute name="範本">是</xsl:attribute>
      <xsl:apply-templates select="引數列/引數"/>
    </組字>
  </xsl:template>

  <xsl:template match="引數">
    <字根>
      <xsl:attribute name="名稱">
        <xsl:value-of select="@名稱" />
      </xsl:attribute>
    </字根>
  </xsl:template>

</xsl:stylesheet>

