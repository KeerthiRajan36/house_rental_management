from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
import enum

from app.database.database import Base


class UserRole(str, enum.Enum):
    ADMIN = "Admin"
    OWNER = "Owner"
    TENANT = "Tenant"


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    full_name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(120),
        unique=True,
        nullable=False,
        index=True
    )

    password = Column(
        String(255),
        nullable=False
    )

    role = Column(
        Enum(UserRole),
        nullable=False
    )

    tenant = relationship(
        "Tenant",
        back_populates="user",
        uselist=False
    )

    def __repr__(self):
        return f"<User {self.email}>"