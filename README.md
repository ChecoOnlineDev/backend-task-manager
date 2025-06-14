# Backend Task Manager

Este repositorio contiene una aplicación de backend simple para la **gestión de tareas**. Fue desarrollada como parte de una prueba técnica para demostrar habilidades en:

* **Programación Orientada a Objetos (POO)** en Python.
* **Validación de datos** medianamente decente utilizando **Pydantic**.
* **Conexión e interacción con una base de datos MySQL**.
* **Manipulación y filtrado de datos** (ej. tareas próximas a vencer).

* **Lectura y exportación de datos en formato JSON**. (bloque de codigo realizado casi completamente con IA)
* **Uso de GIT** para control de versiones con los mensajes commit requeridos, desde la estructura en requerida en el proyecto, la implementacion del modelo en task.py y la logica de interactuar con la base de datos en database.py.
Hasta la implementacion del main.py en el cual se realizan las conexiones necesarias usando un diccionario para las credenciales reales, y se implementa en si la interfaz de la app".

* **Documentación** reutilize el mismo formato de la prueba para la documentacion del readme.md .

---

## 🎯 Objetivos Clave Cumplidos

* **Uso correcto de POO**: Implementación de clases como `Task` a través de Pydantic y `DatabaseManager` para encapsular lógica y datos, siguiendo principios de modularidad.

* **Validación con Pydantic**: Asegura la integridad de los datos de la tarea mediante esquemas Pydantic dedicados, ahora organizados en la carpeta `app/schemas`.

* **Lógica y claridad del código**: Código bien estructurado, comentado y fácil de entender, con una clara separación de responsabilidades.

* **Conexión a MySQL**: Funcionalidad completa para establecer conexión, crear la tabla, insertar, consultar y filtrar tareas en MySQL, encapsulada en la carpeta `app/db`.

* **Exportación/Importación JSON**: Permite guardar y cargar tareas desde/hacia un archivo `tasks.json` de manera robusta, manejando la conversión de tipos de datos como las fechas.

* **Uso de Git con mensajes claros**: El historial de commits debe reflejar las etapas de desarrollo (`init project structure`, `add task model and DB logic`, `implement JSON export/import`).

* **README bien estructurado**: Documentación completa para la configuración y ejecución del proyecto, así como una explicación de las decisiones técnicas.

* **Código limpio y organizado**: Adherencia mediana a una estructura modular en proyectos y buenas practicas de programacion.





---

