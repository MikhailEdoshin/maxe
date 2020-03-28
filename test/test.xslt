<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl = "http://www.w3.org/1999/XSL/Transform">

  <!-- Sample XSLT to test maxe. Wraps everything into 'result'. Accepts a 
       parameter. Has an unusual encoding to test files and pipes. -->

  <xsl:output encoding="ascii" />
  <xsl:param name="a" />

  <xsl:template match="/">
    <result a="{$a}">
      <xsl:copy-of select="*" />
    </result>
  </xsl:template>
</xsl:stylesheet>
 
