from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func, ForeignKey, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.authentication_module.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"


Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

def add_user(username, email, password_hash):
    new_user = User(username=username, email=email, password_hash=password_hash)
    session.add(new_user)
    session.commit()
    print(f"User {username} added to the database.")

def get_all_users():
    return session.query(User).all()

if __name__ == "__main__":
    # Example usage: Adding a new user
    add_user('admin2', 'admin2@gimmick.com', 'admin1234')
    # Example usage: Retrieving all users
    users = get_all_users()

    for user in users:
        print(user)
