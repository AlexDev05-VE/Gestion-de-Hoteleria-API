from sqlalchemy import inspect, select, UniqueConstraint
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.base import Base


class Validator:
    """Clase utilitaria de validación para operaciones del CRUD con SQLAlchemy y FastAPI.

    Proporciona métodos genéricos de inspección de modelos para verificar la
    existencia de atributos, limpiar valores nulos y prevenir duplicados
    basados en restricciones únicas (UniqueConstraints).
    """

    @classmethod
    def exists_fields(cls, model: type[Base], fields: dict[str, any]) -> bool:
        """Valida que todas las llaves enviadas en un diccionario correspondan a

        atributos/columnas válidos del modelo ORM y que no contengan valores
        None.

        Args:
            model (type[Base]): Clase del modelo ORM de SQLAlchemy a
              inspeccionar.
            fields (dict[str, any]): Diccionario con los nombres de campos y sus
              valores.

        Returns:
            bool: True si todos los campos son válidos y no nulos.

        Raises:
            HTTPException (400): Si un campo no existe en el modelo o si contiene
            un valor None.
            HTTPException (500): Ante cualquier error inesperado de inspección.
        """
        try:
            # Inspeccionar la estructura del modelo ORM
            ins = inspect(model)

            # Obtener lista de todos los atributos/propiedades válidos reconocidos por el ORM
            orm_descriptors = list(ins.all_orm_descriptors.keys())

            # Iterar cada llave recibida en la petición/payload
            for field in fields.keys():
                # 1. Validar si el campo existe en la definición del modelo
                if field not in orm_descriptors:
                    raise HTTPException(
                        status_code=400,
                        detail=f"El campo '{field}' no existe en el modelo.",
                    )

                # 2. Validar que el campo no sea nulo (útil para búsquedas estrictas)
                if fields[field] is None:
                    raise HTTPException(
                        status_code=400,
                        detail=f"El campo '{field}' no puede ser nulo para la búsqueda.",
                    )

            return True

        except HTTPException:
            # Re-lanzar excepciones HTTP previas sin alterarlas
            raise
        except Exception as e:
            # Capturar errores de servidor inesperados
            raise HTTPException(status_code=500, detail=str(e))

    @classmethod
    def depuration_fields_none(cls, fields: dict[str, any]) -> dict[str, any]:
        """Filtra y elimina las llaves con valor None de un diccionario.

        Args:
            fields (dict[str, any]): Diccionario original a depurar.

        Returns:
            dict[str, any]: Nuevo diccionario con únicamente las llaves que
            poseen valores distintos de None.
        """
        try:
            # Comprensión de diccionario: conserva solo entradas con valor definido
            return {
                key: value for key, value in fields.items() if value is not None
            }

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @classmethod
    def exists_unique_constraints(
        cls, db: Session, model: type[Base], fields: dict[str, any]
    ) -> bool:
        """Inspecciona los campos con restricción UNIQUE del modelo y verifica si

        alguno de los valores enviados en 'fields' ya existe registrado en la
        Base de Datos.

        Soporta restricciones asignadas individualmente en la columna (unique=True)
        y restricciones compuestas a nivel de tabla (UniqueConstraint en __table_args__).

        Args:
            db (Session): Sesión activa de SQLAlchemy para consultar la BD.
            model (type[Base]): Clase del modelo ORM a validar.
            fields (dict[str, any]): Datos recibidos para la creación/edición de
              un recurso.

        Returns:
            bool: True si se detecta que al menos un valor único ya existe en la
            BD, False si no hay coincidencias duplicadas.
        """
        try:
            mapper = inspect(model)
            unique_fields = set()

            # --- PASO 1: Identificar columnas individuales marcadas con unique=True ---
            for col in mapper.columns:
                if col.unique:
                    # Guardar la clave (key) del atributo ORM
                    unique_fields.add(col.key)

            # --- PASO 2: Identificar restricciones UniqueConstraint declaradas a nivel de Tabla ---
            for constraint in mapper.mapped_table.constraints:
                if isinstance(constraint, UniqueConstraint):
                    for col in constraint.columns:
                        # Extraer la clave del atributo ORM mapeado para cada columna de la restricción
                        unique_fields.add(col.key)

            # --- PASO 3: Consultar la BD solo para aquellos campos que sean ÚNICOS ---
            for field, value in fields.items():
                if field in unique_fields and value is not None:
                    # Validar si el atributo existe físicamente en la clase del modelo
                    if hasattr(model, field):
                        column_attr = getattr(model, field)

                        # Armar la consulta dinámica: SELECT * FROM model WHERE column == value
                        stmt = select(model).where(column_attr == value)

                        # Si db.scalar retorna un registro, significa que el valor ya está registrado
                        if db.scalar(stmt) is not None:
                            return True  # Registro duplicado encontrado

            # Si ningún campo único coincidió en la base de datos
            return False

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))