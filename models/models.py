from sqlalchemy import Column, ForeignKey, Integer, String

from session import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)

    def dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
        }


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey(column="users.id", ondelete="cascade"), primary_key=True
    )
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    status = Column(String)

    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
        }


