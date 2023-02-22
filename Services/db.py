from Database.database import Base, engine, session_local


def create_database():
    return Base.metadata.create_all(bind=engine)

