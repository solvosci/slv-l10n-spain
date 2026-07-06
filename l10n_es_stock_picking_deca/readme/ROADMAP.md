* **Esta es una versión de mínimos** y basada en el estándar de gestión de
  inventario de Odoo (módulo `stock`), por lo que se pueden echar en falta datos
  que deberían ser incorporados mediante algunos otros módulos.
  En general, si dichos módulos añaden tales datos al impreso de albarán de
  entrega (o el escogido por configuración), no haría falta mayor integración
  con este módulo.
  Datos que actualmente se pueden echar en falta:
  * Datos de transportista.
  * Datos del conductor.
  * Matrículas del transporte.
* La página de rechazo de acceso a una URL no válida podría ser mejorable
  (actualmente da un error 403 - Forbidden).
* La generación del DeCA es completamente manual, pero podría ser automatizada
  tras la firma del mismo y de acuerdo a criterios de generación (p.ej. por
  contacto, tipo de operación de entrega, etc.).
* Este módulo solo cubre órdenes de entrega. Si la empresa que lo usa tiene
  obligación de generar documentos como cargador contractual, al menos pasar
  a cubrir albaranes de entrega (y que estén incompletos) parece a priori
  necesario. Este módulo no lo cubre.

Cualquier contribución es bienvenida para añadir esos datos de forma integrada
a este módulo.

