<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl = "http://www.w3.org/1999/XSL/Transform">

  <!-- Sample XSLT to test XML verified with DTD (that must enable the 'id()' 
       function to work). -->

  <xsl:template match="/">
    <result>
      <xsl:copy-of select="id('a')" />
    </result>
  </xsl:template>

</xsl:stylesheet>
 
