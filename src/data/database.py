import os
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.exc

class DatabaseManager:
    def __init__(self, host=None, port=None, user=None, password=None, dbname=None, logger=None):
        self.host = host or os.getenv("DB_HOST", "localhost")
        self.port = port or os.getenv("DB_PORT", "5432")
        self.user = user or os.getenv("DB_USER", "bot_discord")
        self.password = password or os.getenv("DB_PASSWORD", "bot")
        self.dbname = dbname or os.getenv("DB_NAME", "discord")
        self.logger = logger
        self.engine = None
        self.session = None
        self.create_database()  # Auto-connect à l'initialisation

    def __connect(self, dbname=None, auto_commit=False):
        if self.logger:
            self.logger.debug(f"Connecting to database {dbname or self.dbname} at {self.host}:{self.port} as {self.user}")
        if self.engine:
            return
        db_url = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{dbname or self.dbname}"
        self.engine = sqlalchemy.create_engine(db_url, isolation_level="AUTOCOMMIT" if auto_commit else None)

    def create_database(self):
        if self.logger:
            self.logger.debug(f"Creating database {self.dbname} if it does not exist.")
        self.__connect("postgres", auto_commit=True)
        if not self.engine:
            raise RuntimeError("Database engine is not initialized.")
        with self.engine.connect() as connection:
            query = f"SELECT 1 FROM pg_database WHERE datname = '{self.dbname}';"
            result = connection.execute(sqlalchemy.text(query))
            db_exists = result.scalar() is not None
            if not db_exists:
                query = f"CREATE DATABASE {self.dbname};"
                connection.execute(sqlalchemy.text(query))
                connection.commit()
        self.close()
        self.__connect()

    def create_schema(self, name, Base):
        if self.logger:
            self.logger.debug(f"Creating schema {name} in database {self.dbname}.")
        self.__connect()
        if not self.engine:
            raise RuntimeError("Database engine is not initialized.")
        with self.engine.connect() as connection:
            query = f"CREATE SCHEMA IF NOT EXISTS {name};"
            connection.execute(sqlalchemy.text(query))
            connection.commit()
        Base.metadata.create_all(self.engine)
        self.session = sqlalchemy.orm.sessionmaker(bind=self.engine)()
    
    def select(self, model, **kwargs):
        """
        Sélectionne des instances du modèle spécifié avec les critères donnés.
        """
        if self.logger:
            self.logger.debug(f"Selecting instances of {model} with criteria {kwargs}.")
        if not self.session:
            raise RuntimeError("Database session is not initialized.")
        query = self.session.query(model)
        for key, value in kwargs.items():
            query = query.filter(getattr(model, key) == value)
        return query.all()

    def commit(self):
        """
        Commit les transactions en cours.
        """
        if self.logger:
            self.logger.debug("Committing the current session.")
        if self.session:
            self.session.commit()

    def close(self):
        """
        Ferme la session et l'engine.
        """
        if self.logger:
            self.logger.debug("Closing the database session and engine.")
        if self.session:
            self.session.close()
        self.session = None
        if self.engine:
            self.engine.dispose()
        self.engine = None

    def __del__(self):
        """
        Ferme la session et l'engine lors de la destruction de l'objet.
        """
        if self.logger:
            self.logger.debug("Destroying Database instance, closing session and engine.")
        self.close()

class Database(DatabaseManager):
    """
    Classe de base pour la gestion de la base de données.
    Hérite de Database pour ajouter des fonctionnalités spécifiques.
    """
    def __init__(self, host=None, port=None, user=None, password=None, dbname=None, logger=None):
        super().__init__(host, port, user, password, dbname, logger)

    def add(self, instance: object):
        if self.logger:
            self.logger.debug(f"Adding instance {instance} to the database.")
        if not self.session:
            raise RuntimeError("Database session is not initialized.")
        try:
            self.session.add(instance)
        except sqlalchemy.exc.SQLAlchemyError as e:
            if self.logger:
                self.logger.error(f"Error adding instance {instance}: {e}")
            self.session.rollback()
            raise
        try:
            self.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            if self.logger:
                self.logger.error(f"Error committing instance {instance}: {e}")
            self.session.rollback()
            raise

    def update(self, instance: object):
        """
        Met à jour une instance de la base de données.
        """
        if self.logger:
            self.logger.debug(f"Updating instance {instance} in the database.")
        if not self.session:
            raise RuntimeError("Database session is not initialized.")
        try:
            self.session.merge(instance)
            self.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            if self.logger:
                self.logger.error(f"Error updating instance {instance}: {e}")
            self.session.rollback()
            raise

    def delete(self, instance: object):
        """
        Supprime une instance de la base de données.
        """
        if self.logger:
            self.logger.debug(f"Deleting instance {instance} from the database.")
        if not self.session:
            raise RuntimeError("Database session is not initialized.")
        try:
            self.session.delete(instance)
            self.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            if self.logger:
                self.logger.error(f"Error deleting instance {instance}: {e}")
            self.session.rollback()
            raise

    def get_all(self, model):
        """
        Récupère toutes les instances du modèle spécifié.
        """
        if self.logger:
            self.logger.debug(f"Getting all instances of {model}.")
        if not self.session:
            raise RuntimeError("Database session is not initialized.")
        return self.session.query(model).all()

    def get_one(self, model, **kwargs):
        """
        Récupère une seule instance du modèle spécifié avec les critères donnés.
        """
        if self.logger:
            self.logger.debug(f"Getting one instance of {model} with criteria {kwargs}.")
        if not self.session:
            raise RuntimeError("Database session is not initialized.")
        query = self.session.query(model)
        for key, value in kwargs.items():
            query = query.filter(getattr(model, key) == value)
        return query.one_or_none()

    def get_filtered(self, model, **kwargs):
        """
        Récupère des instances du modèle spécifié avec les critères donnés.
        """
        if self.logger:
            self.logger.debug(f"Getting filtered instances of {model} with criteria {kwargs}.")
        if not self.session:
            raise RuntimeError("Database session is not initialized.")
        query = self.session.query(model)
        for key, value in kwargs.items():
            query = query.filter(getattr(model, key) == value)
        return query.all()
