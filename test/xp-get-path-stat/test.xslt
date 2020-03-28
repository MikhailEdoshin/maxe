<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl  = "http://www.w3.org/1999/XSL/Transform"
    xmlns:mext = "urn:onegasoft:Maxe/Ext"
    extension-element-prefixes="mext">

  <!-- test 'mext:get-path-stat'. -->

  <xsl:template match="/">
    <result>
      <xsl:copy-of select="mext:get-path-stat('test')" />
    </result>
  </xsl:template>
</xsl:stylesheet>
 
