from sqlalchemy.orm import Session
from src.models.categories import Category
from src.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryPatch
from src.crud.crud import GetModel


"""
Este modulo esta pensado para abstraer toda la logica de CRUD para utilizarlo en los src\routers, usando la logicas de CRUD en la API REST, cada uno correspondiendo al metodo de HTTP
"""

"""
Categories 
- Metodo GET: 
"""

class GetCategoriesModel(GetModel):
    """Clase para manejar la logica de GET para categorias"""
    """
    - db: Session: Sesion de la base de datos
    - model: Category: Modelo de la base de datos
    - Retorna: List[Category]: Lista de categorias

    Validaciones:
    1. Verificar si la sesion es valida - Instancias
    2. Verificar si el modelo es una instancia de Category
    """
    @classmethod
    def get_all(cls, db: Session, model: Category):

        """Metodo que se va a encargar de obtener todas las categorias"""
        if not isinstance(db, Session):
            raise ValueError("db debe ser una sesion de SQLAlchemy")
        if not isinstance(model, Category):
            raise ValueError("model debe ser una instancia de Category")

        return db.scalars(select(model)).all()
    
    """
    - db: Session: Sesion de la base de datos
    - id: int: ID de la categoria a obtener
    - model: Category: Modelo de la base de datos
    - Retorna: Category: Categoria

    Validaciones:
    1. Verificar si la sesion es valida - Instancias
    2. Verificar si el modelo es una instancia de Category
    3. Verificar si el ID es un entero
    4. Verificar si el ID es mayor a 0
    """

    @classmethod
    def get_by_id(cls, db: Session, id: int, model: Category):
        
        """Metodo que se va a encargar de obtener una categoria por ID"""
        if not isinstance(db, Session):
            raise ValueError("db debe ser una sesion de SQLAlchemy")
        if not isinstance(model, Category):
            raise ValueError("model debe ser una instancia de Category")
        if not isinstance(id, int):
            raise ValueError("id debe ser un entero")
        if id <= 0:
            raise ValueError("id debe ser mayor a 0")

        return db.scalars(select(model).filter(model.category_id == id)).all()
    
    """
    - db: Session: Sesion de la base de datos
    - model: Category: Modelo de la base de datos
    - Retorna: List[Category]: Lista de categorias

    Validaciones:
    1. Verificar si la sesion es valida - Instancias
    2. Verificar si el modelo es una instancia de Category
    3. Verificar si el campo existe en el modelo
    """
    @classmethod
    def get_by_field(cls, db: Session, model: Category):
        """Metodo que se va a encargar de obtener categorias por campo"""
        return db.scalars(select(model)).all()
