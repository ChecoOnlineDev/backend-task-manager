import mysql.connector
from mysql.connector import Error
from datetime import date, timedelta
from typing import List, Dict, Union
from app.schemas.task import Task # Importamos el modelo Task desde su nueva ubicación en schemas

class DatabaseManager:
    """
    Gestiona la conexión y las operaciones CRUD (Crear, Leer, Actualizar, Borrar)
    con la base de datos MySQL para las tareas.
    """
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """
        Intenta establecer una conexión con la base de datos MySQL utilizando
        los detalles de configuración proporcionados. Imprime un mensaje de éxito
        o un error si la conexión falla.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Conexión satisfactoria a la base de datos.")
        except Error as e:
            print(f"Error de conexión a la base de datos MySQL: {e}")
            self.connection = None # Asegura que la conexión sea None si hay un error

    def close(self):
        """
        Cierra la conexión activa a la base de datos si existe y está abierta.
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión a la base de datos cerrada.")

    def create_tasks_table(self):
        """
        Crea la tabla 'tasks' en la base de datos si aún no existe.
        Define la estructura de l
        """
        if not self.connection:
            print("No conectado a la base de datos. No se puede crear la tabla.")
            return

        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    status VARCHAR(50) NOT NULL,
                    due_date DATE NOT NULL
                )
            """)
            self.connection.commit() # Confirma la creación de la tabla en la base de datos
            print("Tabla 'tasks' verificada/creada exitosamente.")
        except Error as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            cursor.close()

    def insert_task(self, task: Task) -> Union[int, None]:
        """
        Inserta una nueva tarea en la tabla 'tasks'.
        Recibe un objeto 'Task' y extrae sus atributos
        para insertarlos en las columnas correspondientes de la tabla.
        Retorna el ID de la tarea recién insertada o None si ocurrió un error.
        """
        if not self.connection:
            print(" No se puede insertar la tarea.")
            return None

        cursor = self.connection.cursor()
        try:
            sql = "INSERT INTO tasks (title, description, status, due_date) VALUES (%s, %s, %s, %s)"
            # Los valores se extraen directamente del objeto Task
            val = (task.title, task.description, task.status, task.due_date)
            cursor.execute(sql, val)
            self.connection.commit() # Guarda los cambios en la base de datos
            print(f"Tarea '{task.title}' insertada exitosamente con ID: {cursor.lastrowid}")
            return cursor.lastrowid
        except Error as e:
            print(f"Error al insertar la tarea: {e}")