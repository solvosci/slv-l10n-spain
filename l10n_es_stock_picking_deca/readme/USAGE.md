Se requiere una configuración mínima para poner en funcionamiento el módulo.
En *Ajustes*, sección "DeCA":

* Activar la funcionalidad. Eso implica activar automáticamente la firma de
  albaranes.
* Cubrir una URL base para los documentos DeCA.
* Seleccionar el impreso que se generará como documento DeCA asociado al
  albarán. Se puede seleccionar un informe cualquiera viculado a
  `stock.picking`, aunque esta implementación solo trae el QR incluido para
  el denominado "Albarán de entrega".

A partir de ese momento, para aquellos albaranes disponibles, se puede operar:

* Un albarán listo para que DeCA se pueda generar es uno de entrega,
  finalizado y firmado.
* Se puede (re)generar la documentación DeCA desde el formulario de un albarán
  dado, o bien con una acción múltiple desde la lista de albaranes. En este
  último caso la generación fallará si la lista contiene albaranes no
  firmables, informándose de cuáles no han podido firmarse.
* Para un albarán con DeCA generado se puede consultar en la pestaña "DeCA"
  toda la información detallada. Asimismo, se pueden filtrar los albaranes para
  determinar cuáles ya tiene un DeCA asociado.
