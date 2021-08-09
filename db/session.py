from sqlalchemy import create_engine, schema, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from core import config

# Creating database if not available
try:
    engine1 = create_engine(config.SQLALCHEMY_DATABASE_URI +
                            config.DATABASE_NAME + '?sslmode=prefer', echo=True)
    conn = engine1.connect()
    conn.close()
    engine1.dispose()
except OperationalError:
    engine2 = create_engine(config.DEFAULT_DATABSE_URI, echo=True)
    conn = engine2.connect()
    conn.execute("commit")
    conn.execute("create database " + config.DATABASE_NAME)
    conn.close()
    engine2.dispose()


# Creating engine & Session
engine = create_engine(config.SQLALCHEMY_DATABASE_URI +
                       config.DATABASE_NAME + '?sslmode=prefer', echo=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
schema_name = config.SCHEMA_NAME


# Creating schemas in database
if not engine.dialect.has_schema(engine, schema_name):
    engine.execute(schema.CreateSchema(schema_name))


# Creating Declarative Base to use it in ORMs
metadata = MetaData(schema=schema_name)
Base = declarative_base(metadata=metadata)


# Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
