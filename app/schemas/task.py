from datetime import date
from pydantic import BaseModel, Field, validator

class Task(BaseModel):
    """
    Modelo Pydantic para la entidad 'Task'.
    Define los campos esperados para una tarea y sus reglas de validación.
    """
    title: str = Field(..., min_length=1, description="Titulo de la tarea")
    description: str = Field(..., description="descripcion de la tarea")
    status: str = Field("pending", description="estado actual de la tarea")
    due_date: date = Field(..., description="fecha de vencimiento de la tarea (Año-Mes-Dia)")
    #el campo field lo usamos para agregar metadatos a los campos, como descripciones y validaciones
    #por ejemplo min_length para el titulo quiere decir que por lo menos el titulo debe tener un caracter

    @validator('status')
    def validate_status(cls, v):
        """
        validador personalizado para aceptar los cambios de estado de las tareas en español 
        """
        valid_statuses = ["pendiente", "en progreso", "completada"]
        if v not in valid_statuses:
            raise ValueError(f"El estado debe ser uno de: {', '.join(valid_statuses)}")
        return v

#cls abreviatura de clase y v abreviatura de valor, se usan como practica estandar al usar pydantic

