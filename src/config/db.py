from abc import ABC, abstractmethod
import os
from typing import Generator
from sqlalchemy import URL, create_engine, text
from sqlalchemy.exc import ArgumentError, OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

## -- Crear función para obtener la URL de la base de datos desde entorno -- ##
## Retorna un objeto URL que contiene la información necesaria para conectarse a la base de datos
## drivername: Nombre del driver a utilizar (postgresql+psycopg2)
## username: Usuario de la base de datos (admin)
## password: Contraseña del usuario de la base de datos (root)
## host: Dirección IP o nombre del host de la base de datos (localhost)
## port: Puerto de la base de datos (5432)
## database: Nombre de la base de datos (hoteleria)

def get_url_db() -> URL:
    """Retorna la URL de conexión validando credenciales dinámicas."""
    return URL.create(
        drivername=os.getenv("DB_DRIVER", "postgresql+psycopg2"),
        username=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASSWORD", "root"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME", "hoteleria"),
    )


## -- Clase Abstracta para la conexión de diferentes bases de datos -- ##
## Una clase abstracta es una clase que no se puede instanciar
## -- get_engine: Método que retorna un objeto Engine que permite la conexión con la base de datos
## -- get_session: Método que retorna un objeto Session que permite la comunicación con la base de datos
## -- check_connection: Método que verifica la conexión con la base de datos
class AbstractDatabaseConnection(ABC):

    @abstractmethod
    def get_engine(self):
        pass

    @abstractmethod
    def get_session(self) -> Session:
        pass

    @abstractmethod
    def check_connection(self) -> bool:
        pass



## -- Conexión concreta a PostgreSQL -- #
## -- get_engine: Método que retorna un objeto Engine que permite la conexión con la base de datos
## -- get_session: Método que retorna un objeto Session que permite la comunicación con la base de datos
## -- check_connection: Método que verifica la conexión con la base de datos
class PostgreSQLConnection(AbstractDatabaseConnection):

    def __init__(self):
        ## -- Variables de instancia (encapsuladas por objeto) -- ##
        # _engine: Objeto Engine que permite la conexión con la base de datos
        # _session_factory: Objeto Session que permite la comunicación con la base de datos
        self._engine = None
        self._session_factory = None

    ## -- Generar un Engine que permita la conexión con la DB de PostgreSQL
    def get_engine(self):
        """Crea el Engine con manejo de errores de inicialización."""
        if self._engine is None:
            try:
                self._engine = create_engine(
                    get_url_db(),
                    echo=False,
                    pool_size=10,  # Límite de conexiones simultáneas
                    max_overflow=20,  # Conexiones adicionales para picos
                    pool_pre_ping=True,  # Detecta si la DB se desconectó antes de consultar
                    pool_recycle=1800,  # Recicla conexiones cada 30 min para evitar cierres de socket
                )
            except ArgumentError as e:
                print(f" Error en la configuración de la URL de la DB: {e}")
                raise
            except Exception as e:
                print(f" Error crítico creando el engine de la DB: {e}")
                raise
        return self._engine

    ## -- Generador de Sessiones
    ## -- Especializado en generar sessiones de PostgreSQL y utilizar sessionmaker para configurar la sesión
    def _get_session_factory(self):
        """Inicializa la fábrica de sesiones (sessionmaker)."""
        if self._session_factory is None:
            engine = self.get_engine()
            self._session_factory = sessionmaker(
                autocommit=False, autoflush=False, bind=engine
            )
        return self._session_factory

    ## -- Obtener la session para empezar a trabajar con la DB
    def get_session(self) -> Session:
        """Retorna una sesión activa lista para interactuar."""
        try:
            factory = self._get_session_factory()
            return factory()
        except SQLAlchemyError as e:
            print(f" Error al crear la sesión en PostgreSQL: {e}")
            raise

    ## -- Verificar conexión a la DB
    ## -- Permite verificar si la DB está viva antes de realizar operaciones críticas
    def check_connection(self) -> bool:
        """Prueba si PostgreSQL está vivo antes de realizar operaciones críticas."""
        try:
            engine = self.get_engine()
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except OperationalError:
            print(" No se pudo establecer conexión con PostgreSQL (Server Down / Red).")
            return False
        except Exception as e:
            print(f" Error inesperado al validar la conexión: {e}")
            return False



## -- Fábricas (Factory Method) de PostgreSQL -- ##
class DatabaseConnectionFactory(ABC):
    """Fabrica abstracta de conexiones a bases de datos."""
    @abstractmethod
    def create_connection(self) -> AbstractDatabaseConnection:
        """Crea y retorna una instancia de AbstractDatabaseConnection."""
        pass



class PostgreSQLConnectionFactory(DatabaseConnectionFactory):
    """Fabrica concreta de PostgreSQL que retorna una instancia de PostgreSQLConnection."""
    def create_connection(self) -> PostgreSQLConnection:
        """Retorna una instancia de PostgreSQLConnection."""
        return PostgreSQLConnection()

# Instanciamos la fábrica una sola vez
db_factory = PostgreSQLConnectionFactory()
db_connection = db_factory.create_connection()


# Inyector de Dependencia seguro para FastAPI
## -- get_db: Función que retorna un objeto Session
## -- lo que permite la comunicación con la base de datos
def get_db() -> Generator[Session, None, None]:
    session = db_connection.get_session()
    try:
        yield session
    except SQLAlchemyError as e:
        session.rollback()  # Revierte la transacción si la consulta falló
        raise e
    finally:
        session.close()  # CIERRA la conexión obligatoriamente al terminar la petición HTTP