<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
    xmlns:xsl = "http://www.w3.org/1999/XSL/Transform">

  <!-- 
  
  maxe/xslt/gather-xsl-output.xslt: a built-in XSLT to collect <xsl:output>
  elements from an XSLT stylesheet. 

  Copyright (C) 2020 Mikhail Edoshin.

  This file is part of Maxe.

  Maxe is free software: you can redistribute it and/or modify it under the 
  terms of the GNU General Public License as published by the Free Software 
  Foundation, either version 3 of the License, or (at your option) any later 
  version.

  Maxe is distributed in the hope that it will be useful, but WITHOUT ANY
  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS 
  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more 
  details.

  You should have received a copy of the GNU General Public License along with
  Maxe.  If not, see <https://www.gnu.org/licenses/>.

  -->

  <xsl:template match="/">
    <result>
      <xsl:apply-templates />
    </result>
  </xsl:template>

  <!-- * -->
  <xsl:template match="* | text()"  />

  <!-- xsl:stylesheet -->
  <xsl:template match="xsl:stylesheet | xsl:transform">
    <xsl:apply-templates />
  </xsl:template>

  <!-- xsl:import | xsl:include -->
  <xsl:template match="xsl:import | xsl:include">
    <xsl:apply-templates select="document(@href)/*" />
  </xsl:template>

  <!-- xsl:output-->
  <xsl:template match="xsl:output">
    <xsl:copy-of select="." />
  </xsl:template>

</xsl:stylesheet>
