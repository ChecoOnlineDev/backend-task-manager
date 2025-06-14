import json
from datetime import date
import os # Necesario para verificar si el archivo JSON existe

from app.schemas.task import Task # Importamos el modelo Task desde su nueva ubicación
from app.db.database import DatabaseManager # Importamos DatabaseManager desde su nueva ubicación


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "151107", 
    "database": "task_manager_db"
}

# Nombre del archivo donde se exportarán e importarán las tareas JSON
TASKS_JSON_FILE = "tasks.json"


db_manager = DatabaseManager(**DB_CONFIG)

def connect_and_setup_db():
    """
    Establece la conexión a la base de datos y se asegura de que la tabla 'tasks' exista.
    Si la conexión falla, la aplicación mostrará un error y saldrá, ya que la DB es crucial.
    """
    print("Intentando conectar y configurar la base de datos...")
    db_manager.connect() # Establecer la conexión a la base de datos
    if not db_manager.connection or not db_manager.connection.is_connected(): # Si la conexión es None o no está activa
        print("Error: No se pudo establecer una conexión activa con la base de datos. Por favor, revisa tu configuración (host, usuario, contraseña, base de datos) y que el servidor MySQL esté en ejecución.")
        exit(1) # Salir con un código de error

    db_manager.create_tasks_table()

def check_db_connection_status():
    """
    Verifica si la conexión a la base de datos está activa y notifica al usuario si no lo está.
    """
    if not db_manager.connection or not db_manager.connection.is_connected():
        print("Advertencia: No hay una conexión activa a la base de datos. Por favor, reinicia la aplicación o verifica tu configuración.")
        return False
    return True








"""Apartir de aqui me apoye mucho en la IA porque no he llegado a la parte de exportar tareas a formato json"""

def export_tasks_to_json():
    print("\n--- Exportando Tareas a JSON ---")
    if not check_db_connection_status():
        return

    tasks_data = db_manager.get_all_tasks()
    if not tasks_data:
        print("No se encontraron tareas en la base de datos para exportar.")
        return

    # Preparar los datos para JSON: convertir objetos 'date' a formato de cadena 'YYYY-MM-DD'
    serializable_tasks = []
    for task_dict in tasks_data:
        task_copy = task_dict.copy()
        if isinstance(task_copy.get('due_date'), date):
            task_copy['due_date'] = task_copy['due_date'].isoformat()
        serializable_tasks.append(task_copy)

    try:
        with open(TASKS_JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(serializable_tasks, f, indent=4)
        print(f"Todas las {len(serializable_tasks)} tareas se exportaron exitosamente a '{TASKS_JSON_FILE}'.")
    except IOError as e:
        print(f"Error al exportar tareas al archivo JSON: {e}")

def import_tasks_from_json():
    """
    Lee tareas desde un archivo JSON y las inserta en la base de datos.
    """
    print("\n--- Importando Tareas desde JSON ---")
    if not check_db_connection_status():
        return

    if not os.path.exists(TASKS_JSON_FILE):
        print(f"Error: El archivo '{TASKS_JSON_FILE}' no fue encontrado. Asegúrate de que existe en el mismo directorio que main.py.")
        return

    try:
        with open(TASKS_JSON_FILE, 'r', encoding='utf-8') as f:
            tasks_to_import = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON desde '{TASKS_JSON_FILE}': {e}. Por favor, verifica el formato del archivo.")
        return
    except IOError as e:
        print(f"Error al leer '{TASKS_JSON_FILE}': {e}")
        return

    if not tasks_to_import:
        print(f"No se encontraron tareas dentro de '{TASKS_JSON_FILE}' para importar.")
        return

    print(f"Intentando importar {len(tasks_to_import)} tareas...")
    imported_count = 0
    for task_data in tasks_to_import:
        try:
            # Pydantic automáticamente validará los datos y convertirá 'due_date' (string a date)
            task = Task(**task_data)
            db_manager.insert_task(task)
            imported_count += 1
        except ValueError as e:
            print(f"Saltando datos de tarea inválidos: {task_data}. Error de validación: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado al importar la tarea: {task_data}. Error: {e}")
    print(f"Se importaron {imported_count} tareas exitosamente.")
    
    """ Hasta esta parte que tiene que ver con json fue estructurado con bastante apoyo de IA""" 
    
    
    
    

def add_new_task():
    """
    Interfaz de ingreso de datos 
    """
    print("\n--- Añadir Nueva Tarea ---")
    if not check_db_connection_status():
        return

    title = input("Introduce el título de la tarea: ")
    description = input("Introduce la descripción de la tarea: ")
    
    status = input("Introduce el estado de la tarea (pendiente, en progreso, completada) [pendiente]: ") or "pendiente"
    due_date_str = input("Introduce la fecha de vencimiento (AAAA-MM-DD): ")

    try:
        # Convertimos la cadena de fecha a un objeto date
        due_date = date.fromisoformat(due_date_str)
        # Creamos una instancia de Task. Pydantic validará los tipos y el estado.
        task = Task(title=title, description=description, status=status, due_date=due_date)
        db_manager.insert_task(task) # Insertamos la tarea validada en la base de datos
    except ValueError as e:
        print(f"Error al crear la tarea: {e}. Por favor, verifica el formato de tu entrada (ej. AAAA-MM-DD para la fecha) o el estado de la tarea.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def view_all_tasks():
    """
    Recupera todas las tareas de la base de datos y las muestra en un formato legible
    en la consola.
    """
    print("\n--- Todas las Tareas ---")
    if not check_db_connection_status():
        return

    tasks = db_manager.get_all_tasks()
    if not tasks:
        print("No se encontraron tareas en la base de datos.")
        return

    for task in tasks:
        # Accedemos a los campos del diccionario de la tarea
        # Convertimos la fecha a string ISO para una visualización consistente
        print(f"ID: {task.get('id')}")
        print(f"  Título: {task.get('title')}")
        print(f"  Descripción: {task.get('description')}")
        print(f"  Estado: {task.get('status')}")
        print(f"  Fecha de Vencimiento: {task.get('due_date').isoformat() if isinstance(task.get('due_date'), date) else task.get('due_date')}\n")

def view_upcoming_tasks():
    """
    Recupera las tareas cuya fecha de vencimiento es en los próximos 3 días (incluyendo hoy)
    y las muestra en la consola.
    """
    print("\n--- Tareas Próximas (Próximos 3 Días) ---")
    if not check_db_connection_status():
        return

    # Llamamos al método del gestor de DB para obtener tareas próximas
    tasks = db_manager.get_upcoming_tasks(days=3)
    if not tasks:
        print("No se encontraron tareas próximas para los siguientes 3 días.")
        return

    for task in tasks:
        print(f"ID: {task.get('id')}")
        print(f"  Título: {task.get('title')}")
        print(f"  Descripción: {task.get('description')}")
        print(f"  Estado: {task.get('status')}")
        print(f"  Fecha de Vencimiento: {task.get('due_date').isoformat() if isinstance(task.get('due_date'), date) else task.get('due_date')}\n")


def display_menu():
    """
    Muestra el menú principal de opciones de la aplicación Task Manager en la consola,
    facilitando la interacción del usuario.
    """
    print("\n" + "="*30)
    print("      Menú del Gestor de Tareas")
    print("="*30)
    print("1. Añadir Nueva Tarea")
    print("2. Ver Todas las Tareas")
    print("3. Ver Tareas Próximas (Próximos 3 Días)")
    print("4. Exportar Tareas a JSON")
    print("5. Importar Tareas desde JSON")
    print("6. Salir")
    print("="*30)

def main():
    """
    Función principal de la aplicación.
    Se encarga de inicializar la base de datos y de ejecutar el bucle
    principal del menú, permitiendo al usuario interactuar con la aplicación.
    """
    connect_and_setup_db() # Conectar a la DB y asegurar que la tabla exista

    while True:
        display_menu()
        choice = input("Introduce tu opción: ")

        if choice == '1':
            add_new_task()
        elif choice == '2':
            view_all_tasks()
        elif choice == '3':
            view_upcoming_tasks()
        elif choice == '4':
            export_tasks_to_json()
        elif choice == '5':
            import_tasks_from_json()
        elif choice == '6':
            print("Saliendo del Gestor de Tareas. ¡Adiós!")
            break # Sale del bucle y termina la aplicación
        else:
            print("Opción inválida. Por favor, introduce un número entre 1 y 6.")

    db_manager.close() # Asegurarse de cerrar la conexión a la base de datos al finalizar

if __name__ == "__main__":
    main()
