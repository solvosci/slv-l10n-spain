Este módulo cubre una implementación base del Documento Electrónico de Control
Administrativo (DeCA).

En esta implementación se cubren las siguientes funcionalidades:

* Se proporciona la generación del DeCA a partir de un albarán de entrega
  completado y firmado cualquiera.
* Para este albarán, se genera un hash único, que será el usado en la URL
  que lo enlazará a través de un código QR.
* El DeCA es almacenado como un documento adjunto al albarán, protegido
  para que no se borre. Este es el documento que se recupera a través de la URL
  provista por el QR.
* Se permite regenerar el DeCA, manteniendo la URL para poder seguir siendo
  descargado desde el PDF/impreso original.
* Cualquier acceso a un documento DeCA manipulando la URL (cambiado el hash
  identificativo) llevará a una pantalla de error.
* La generación de DeCA es completamente manual, pero se puede hacer por
  lotes desde el listado de albaranes.
* Se guarda la trazabilidad completa de la generación y posteriores
  regeneraciones del documento.
* Se añade el código QR al formato estándar de albarán de entrega, pero si
  se dispone de un formato distinto de impreso en el que usarlo, se puede
  seleccionar en la configuración por empresa uno distinto.
* También a nivel de empresa se puede establecer una URL prefijo de
  publicación (p.ej. https://deca.miempresa.com/) para encapusular el acceso
  al resto de Odoo publicado.

En esta implementación se incluye un mixin que permitiría generar y administrar
el DeCA desde otras figuras que no fuesen un albarán (stock.picking), si fuese
necesario.

También se preparan ciertos métodos para poder generar más de un documento de
control (p.ej. para eCMR) mediante la herencia de este módulo.
