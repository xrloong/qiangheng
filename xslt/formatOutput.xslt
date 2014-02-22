<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <!--
	Python 的 ElementTree 目前的 XML 輸出沒有很好，
	所以使用此 XSLT 轉換成較好的格式。
   -->

  <xsl:output method="xml" encoding="UTF-8" indent="yes"/>
  <xsl:strip-space elements="*"/>

  <xsl:template match="/">
    <xsl:copy-of select="." />
  </xsl:template>

</xsl:stylesheet>

