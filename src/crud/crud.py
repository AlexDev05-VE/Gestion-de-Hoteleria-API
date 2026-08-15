
from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase

"""
Este modulo esta pensando exclusivamente para abstraer la logica de CRUD, el cual se va a encargar de todas las interaciones con la base de datos pero para usar clases abstractas para la herencia y reutilizar logica CRUD en los diferentes CRUD individuales
"""

"""
Clases Abstractas para manejar la logica de GET
- get_all: Metodo que se va a encargar de obtener todos los registros de un modelo
- get_by_id: Metodo que se va a encargar de obtener un registro por ID
- get_by_field: Metodo que se va a encargar de obtener registros por campo
"""

class GetModel(ABC):

    """Clase Abstracta para manejar la logica de GET"""
    """
    - db: Session: Sesion de la base de datos
    - model: DeclarativeBase: Modelo de la base de datos
    - Retorna: List[DeclarativeBase]: Lista de registros
    - Falta implementacion - Implementar LIMIT y OFSET para paginacion y validacion de errores
    """
    @classmethod
    @abstractmethod
    def getAllResources(cls, db: Session, model: DeclarativeBase):
        pass

    """
    - db: Session: Sesion de la base de datos
    - id: int: ID del registro a obtener
    - model: DeclarativeBase: Modelo de la base de datos
    - Retorna: DeclarativeBase: Registro
    - Falta implementacion - Falta implementacion - Implementar LIMIT y OFSET para paginacion y validacion de errores
    """
    @classmethod
    @abstractmethod
    def getById(cls, db: Session, id: int, model: DeclarativeBase):
        pass

    """
    - db: Session: Sesion de la base de datos
    - model: DeclarativeBase: Modelo de la base de datos
    - Retorna: List[DeclarativeBase]: Lista de registros
    - Falta implementacion - Implementar validacion de campos y filtros, para obtener campos especificos y ordenar los registros
    """
    @classmethod
    @abstractmethod
    def getByField(cls, db: Session, model: DeclarativeBase):
        pass

class PostModel(ABC):

    """Clase Abstracta para manejar la logica de POST"""
    """
    - db: Session: Sesion de la base de datos
    - model: DeclarativeBase: Modelo de la base de datos
    - Retorna: DeclarativeBase: Registro creado
    """
    @classmethod
    @abstractmethod
    def post_resource(cls, db: Session, model: DeclarativeBase):
        pass