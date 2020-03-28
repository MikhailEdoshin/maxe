<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl  = "http://www.w3.org/1999/XSL/Transform"
    xmlns:mext = "urn:onegasoft:Maxe/Ext"
    extension-element-prefixes="mext">

  <!-- test 'mext:read-text'. -->

  <xsl:template match="/">
    <xsl:variable name="text">Sample ``rst`` file
-------------------

Sample paragraph with some *inline* styling.</xsl:variable>
    <result>
      <xsl:copy-of select="mext:read-text($text, '.rst')" />
    </result>
  </xsl:template>
</xsl:stylesheet>
