<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format">
  <xsl:output method="text"/>
  
  <xsl:key name="service-group-key" match="top/response/result/service-group/entry/members" use="../@name"/>
  <xsl:key name="address-group-key" match="top/response/result/address-group/entry/static" use="../@name"/>
  <xsl:key name="application-group-key" match="top/response/result/application-group/entry/members" use="../@name"/>
  
  <xsl:param name="vpnname" />
  
  
  
  <xsl:template match="top/response/result/security/rules">
    
    
    
    {"Result": [
    <xsl:for-each select="entry">
      
      <xsl:if test="from/member='SSLVPN' or from/member='GP-ASADI'">
        <xsl:if test="source/member=$vpnname">{"Origen":{<xsl:for-each select="source/member">"<xsl:value-of select="."/>":["<xsl:for-each select="key('address-group-key',.)">
              <xsl:value-of select="normalize-space(.)"/>
              
            </xsl:for-each>"]<xsl:if test="position() != last()"><xsl:text>,</xsl:text></xsl:if>
          </xsl:for-each>},
          "Zona_destino": [<xsl:for-each select="to/member">"<xsl:value-of select="."/>"<xsl:if test="position() != last()"><xsl:text>, </xsl:text></xsl:if></xsl:for-each>],
          "Destino": [<xsl:for-each select="destination/member">"<xsl:value-of select="."/>"<xsl:if test="position() != last()"><xsl:text>, </xsl:text></xsl:if></xsl:for-each>],
          "GP_ASADI": ["<xsl:value-of select="from/member"/>"],
          "Grupo_AD": [<xsl:for-each select="source-user/member">"<xsl:value-of select="."/>"<xsl:if test="position() != last()"><xsl:text>, </xsl:text></xsl:if></xsl:for-each>],
          "Puertos": {<xsl:for-each select="service/member"><xsl:choose><xsl:when test=".='defaultVPN_ports'">"<xsl:value-of select="."/>": ["<xsl:for-each select="key('service-group-key',.)">
                  <xsl:value-of select="normalize-space(.)"/></xsl:for-each>"]<xsl:if test="position() != last()">
                  <xsl:text>,</xsl:text></xsl:if>
              </xsl:when>
              <xsl:when test=".='SAP_ports'">"<xsl:value-of select="."/>": ["<xsl:for-each select="key('service-group-key',.)">
                  <xsl:value-of select="normalize-space(.)"/></xsl:for-each>"]<xsl:if test="position() != last()">
                  <xsl:text>,</xsl:text>
                </xsl:if>
              </xsl:when>
              <xsl:when test=".='defaultVPN_ports_old'">"<xsl:value-of select="."/>": ["<xsl:for-each select="key('service-group-key',.)">
                  <xsl:value-of select="normalize-space(.)"/></xsl:for-each>"]<xsl:if test="position() != last()">
                  <xsl:text>,</xsl:text>
                </xsl:if>
              </xsl:when>
              <xsl:otherwise>
                "<xsl:value-of select="."/>": "<xsl:value-of select="."/>"<xsl:if test="position() != last()"><xsl:text>,</xsl:text>
                </xsl:if>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:for-each>},
          "Destinoaux": {<xsl:for-each select="destination/member">"<xsl:value-of select="."/>": ["<xsl:for-each select="key('address-group-key',.)">
              <xsl:value-of select="normalize-space(.)"/></xsl:for-each>"]<xsl:if test="position() != last()">
              <xsl:text>,</xsl:text></xsl:if>
            
          </xsl:for-each>},
          "Applicationaux": {<xsl:for-each select="application/member">"<xsl:value-of select="."/>": ["<xsl:for-each select="key('application-group-key',.)">
              <xsl:value-of select="normalize-space(.)"/></xsl:for-each>"]<xsl:if test="position() != last()">
              <xsl:text>,</xsl:text></xsl:if>
            
          </xsl:for-each>},
          
          "Aplicacion": [<xsl:for-each select="application/member">"<xsl:value-of select="."/>"<xsl:if test="position() != last()"><xsl:text>, </xsl:text>
            </xsl:if>
          </xsl:for-each>],
          "Accion": ["<xsl:value-of select="action"/>"],
          "Descripcion":["<xsl:value-of select="description"/>"],
          "Negatedestination": ["<xsl:value-of select="negate-destination"/>"],
          "Disabled": ["<xsl:value-of select="disabled"/>"]
          }<xsl:if test="position() != (last()-2)"><xsl:text>,</xsl:text></xsl:if>
        </xsl:if>
        
      </xsl:if>
    </xsl:for-each>]}
  </xsl:template>
  <xsl:template match="text()"/>
</xsl:stylesheet>
