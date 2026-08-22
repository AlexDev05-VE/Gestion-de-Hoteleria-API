"""Módulo de operaciones CRUD para la entidad Categoría.

Define la clase `CategoriesModel`, que extiende la funcionalidad base de
`CRUDModel` e implementa las consultas, validaciones y modificaciones
en la base de datos para las categorías del sistema.
"""

from typing import Any
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from crud.crud import CRUDModel
from models.categories import Category
from schemas.category import CategoryCreate, CategoryResponse
from validators.validation import Validator


class CategoriesModel(CRUDModel):
    """Clase encargada de ejecutar las operaciones de persistencia y consulta

    para el modelo de Categoría (`Category`). Hereda la interfaz genérica de
    `CRUDModel`.
    """

    _model: type[Category] = Category

    @classmethod
    def get_all(
        cls,
        db: Session,
        fields: dict[str, Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Category]:
        """Obtiene una lista de categorías desde la base de datos.

        Permite aplicar filtros dinámicos basados en un diccionario de campos
        y soporta paginación opcional mediante límite y desplazamiento.

        Args:
            db (Session): Sesión activa de SQLAlchemy.
            fields (dict[str, Any] | None): Diccionario clave-valor con campos
              y valores para filtrar con cláusula WHERE.
            limit (int | None): Número máximo de registros a recuperar.
            offset (int | None): Número de registros a omitir para paginación.

        Returns:
            list[Category]: Lista de objetos ORM del modelo `Category`.

        Raises:
            HTTPException (404): Si la tabla está vacía o si ningún registro
              coincide con los filtros provistos.
            HTTPException (400): Si alguno de los campos de filtro no existe en el modelo.
            HTTPException (500): Ante un error inesperado en el servidor.
        """
        try:
            # Verificar si existe al menos un registro registrado en la tabla
            has_records = db.scalar(
                select(select(cls._model.category_id).exists())
            )
            if not has_records:
                raise HTTPException(
                    status_code=404, detail="No se encontraron registros."
                )

            # Caso 1: Consulta con filtros aplicados
            if fields is not None:
                # Validar la existencia de las columnas en el modelo ORM
                Validator.exists_fields(cls._model, fields)

                # Construcción y ejecución de la consulta filtrada
                query = select(cls._model).filter_by(**fields)
                results = db.execute(query).scalars().all()

                if not results:
                    raise HTTPException(
                        status_code=404,
                        detail=f"No se encontraron registros con los filtros: {fields}",
                    )

                return results

            # Caso 2: Consulta general sin filtros
            return db.execute(select(cls._model)).scalars().all()

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @classmethod
    def get_by_id(cls, db: Session, id: int) -> Category:
        """Recupera un registro de categoría único según su clave primaria.

        Args:
            db (Session): Sesión activa de la base de datos.
            id (int): Identificador único (`category_id`) a consultar.

        Returns:
            Category: Instancia del modelo ORM correspondiente al ID.

        Raises:
            HTTPException (404): Si no existe una categoría asociada al ID.
            HTTPException (500): Ante un error inesperado en la ejecución.
        """
        try:
            stmt = select(cls._model).where(cls._model.category_id == id)
            result = db.scalar(stmt)

            if not result:
                raise HTTPException(
                    status_code=404,
                    detail=f"category_id: {id} - Categoría no encontrada.",
                )
            return result

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @classmethod
    def create(cls, db: Session, data: dict[str, Any] | None = None) -> Category:
        """Crea y persiste un nuevo registro de categoría en la base de datos.

        Aplica validaciones previas de integridad:
        1. Comprueba la recepción de datos.
        2. Verifica que las llaves pertenezcan a las columnas de la tabla.
        3. Valida restricciones de unicidad (evita duplicados).

        Args:
            db (Session): Sesión activa de la base de datos.
            data (dict[str, Any] | None): Diccionario con los datos a insertar.

        Returns:
            Category: Instancia ORM recién persistida con su ID generado.

        Raises:
            HTTPException (400): Si no hay datos, si los campos no existen o
              si se rompe una restricción UNIQUE.
            HTTPException (500): Si ocurre un fallo en la persistencia (aplica rollback).
        """
        try:
            if data is None:
                raise HTTPException(
                    status_code=400,
                    detail="No se enviaron datos para crear el recurso.",
                )

            # Validar existencia de los atributos en el modelo
            Validator.exists_fields(cls._model, data)

            # Validar restricciones de duplicidad (UniqueConstraints)
            if Validator.exists_unique_constraints(db, cls._model, data):
                category_name = data.get("category", "especificada")
                raise HTTPException(
                    status_code=400,
                    detail=f"La categoría '{category_name}' ya existe en la base de datos.",
                )

            # Instanciar e insertar en la BD
            db_obj = cls._model(**data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

            return db_obj

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))