"""Módulo de abstracción base para operaciones CRUD.

Proporciona la interfaz abstracta `CRUDModel`, definiendo el contrato estricto
que deben cumplir todas las subclases encargadas de gestionar la persistencia 
y consulta de recursos en la base de datos con SQLAlchemy.
"""

from abc import ABC, abstractmethod
from typing import Any
from sqlalchemy.orm import Session
from models.base import Base


class CRUDModel(ABC):
    """Clase base abstracta (ABC) para la implementación de patrones CRUD.

    Establece los contratos de métodos requeridos para gestionar modelos ORM
    de SQLAlchemy en la aplicación.

    Attributes:
        _model (type[Base] | None): Referencia a la clase del modelo ORM asociad.
    """

    _model: type[Base] | None = None

    @classmethod
    @property
    def model(cls) -> type[Base] | None:
        """Obtiene la clase del modelo ORM asignada al CRUD.

        Returns:
            type[Base] | None: Modelo de SQLAlchemy registrado en la subclase.
        """
        return cls._model

    @classmethod
    @abstractmethod
    def get_all(
        cls,
        db: Session,
        fields: dict[str, Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Any]:
        """Obtiene una lista de registros filtrada o paginada desde la BD.

        Args:
            db (Session): Sesión activa de SQLAlchemy.
            fields (dict[str, Any] | None): Diccionario clave-valor con filtros para la consulta.
            limit (int | None): Límite máximo de registros a retornar.
            offset (int | None): Desplazamiento inicial para paginación.

        Returns:
            list[Any]: Colección de instancias del modelo ORM recuperadas.
        """
        pass

    @classmethod
    @abstractmethod
    def get_by_id(cls, db: Session, id: int) -> Any:
        """Obtiene un único registro por su clave primaria.

        Args:
            db (Session): Sesión activa de SQLAlchemy.
            id (int): Identificador único del recurso.

        Returns:
            Any: Instancia del modelo ORM correspondiente al ID.
        """
        pass

    @classmethod
    @abstractmethod
    def create(cls, db: Session, data: dict[str, Any] | None = None) -> Any:
        """Crea y persiste un nuevo registro en la base de datos.

        Args:
            db (Session): Sesión activa de SQLAlchemy.
            data (dict[str, Any] | None): Diccionario con los atributos del nuevo registro.

        Returns:
            Any: Instancia del modelo ORM recién creado.
        """
        pass

    @classmethod
    @abstractmethod
    def update(cls, db: Session, id: int, data: dict[str, Any]) -> Any:
        """Actualiza completamente un registro existente en la base de datos.

        Args:
            db (Session): Sesión activa de SQLAlchemy.
            id (int): Identificador del registro a actualizar.
            data (dict[str, Any]): Diccionario con los nuevos valores.

        Returns:
            Any: Instancia del modelo ORM actualizado.
        """
        pass

    @classmethod
    @abstractmethod
    def patch(cls, db: Session, id: int, data: dict[str, Any]) -> Any:
        """Actualiza parcialmente un registro existente en la base de datos.

        Args:
            db (Session): Sesión activa de SQLAlchemy.
            id (int): Identificador del registro a modificar.
            data (dict[str, Any]): Diccionario con los campos específicos a modificar.

        Returns:
            Any: Instancia del modelo ORM modificado.
        """
        pass

    @classmethod
    @abstractmethod
    def delete(cls, db: Session, id: int) -> None:
        """Elimina un registro de la base de datos por su identificador.

        Args:
            db (Session): Sesión activa de SQLAlchemy.
            id (int): Identificador del registro a eliminar.

        Returns:
            None
        """
        pass