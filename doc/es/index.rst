===========================
Stock. Herramientas albarán
===========================

El módulo de herramientas dispone de un nuevo modelo para gestionar albaranes y
realizar nuevas acciones según el estado del albarán.

El botón "Siguiente" llama el método: "next_STATE" (STATE es el código del estado del albarán).

En un módulo personalizado puede crear nuevos métodos según el estado y realizar
acciones en el proceso del albarán, por ejemplo:

- Enviar el albarán a una impresora.
- Enviar el albarán a un transportista.
- Cambiar de estado.
- ...

Dispone de dos nuevos menús para las herramientas:

- Todos. Muestra todos los albaranes que se han gestionado sin el filtro empleado.
  Acceso mediante grupo "Administrador herramienta stock".
- Defecto. Muestro todos los albaranes que se han gestionado según empleado actual (preferencias usuario).
  Acceso mediante grupo "Herramienta stock".
