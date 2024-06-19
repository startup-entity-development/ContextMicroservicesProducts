import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists


db_name = os.environ['DB_NAME']
db_password = os.environ['DB_PASSWORD']
db_user = os.environ['DB_USER']
db_uri = os.environ['DB_URI']
pool_recycle = int(os.environ['POOL_RECYCLE'])
pool_size = int(os.environ['POOL_SIZE'])
max_overflow = int(os.environ['MAX_OVERFLOW'])

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_uri}/{db_name}", pool_recycle=pool_recycle,
                       echo=False, pool_size=pool_size, max_overflow=max_overflow, client_encoding="utf8")


# Engine connect
# Declarative base model to create models tables and classes
Base = declarative_base()
Base.metadata.bind = engine  # Bind engine to metadata of the base class

# Create models session_msg object
db_session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
Base.query = db_session.query_property()  # Used by graphql to execute queries

# if not database_exists(engine.url) or True:
#    from setup_db import create_all_models
#    create_all_models(interactive=False)

