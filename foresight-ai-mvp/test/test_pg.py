from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://christiangiron@localhost:5432/foresight"
)

with engine.connect() as conn:
    print("Connected to PostgreSQL")