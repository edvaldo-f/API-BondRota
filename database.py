import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Adicionar SSL para conexões remotas (Render)
if DATABASE_URL and DATABASE_URL.startswith("postgresql"):
    # Para PostgreSQL remoto, adicionar SSL
    engine = create_engine(
        DATABASE_URL,
        connect_args={"sslmode": "require"},
        pool_pre_ping=True,  # Verifica a conexão antes de usar
        pool_recycle=3600,   # Recicla conexões a cada 1 hora
    )
else:
    # Para desenvolvimento local
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
