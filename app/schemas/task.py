from datetime import date
from pydantic import BaseModel, Field, validator

class Task(BaseModel):
    """
    Clase task que hereda de basemodel de pydantic,definimos los campos que tendrá la tarea
    y sus validaciones. Esta clase representa una tarea con atributos como título, descripción,
    estado y fecha de vencimiento. Utiliza Pydantic para la validación de datos.
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
        Validador personalizado para el campo estatus,y como manejar si no se da un valor 
        válido. Asegura que el estado de la tarea sea uno de los valores permitidos.
        """
        valid_statuses = ["pendiente", "en progreso", "completada"]
        if v not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
        return v

#cls abreviatura de clase y v abreviatura de valor, se usan como practica estandar al usar pydantic