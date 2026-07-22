from sqlalchemy import Column, Integer, String, Date, ForeignKey

from sqlalchemy.orm import relationship

from app.database.database import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(120),
        unique=True,
        nullable=False,
        index=True
    )

    phone = Column(
        String(20),
        nullable=False
    )

    aadhaar_number = Column(
        String(12),
        unique=True,
        nullable=False,
        index=True
    )

    move_in_date = Column(
        Date,
        nullable=False
    )

    agreement_end_date = Column(
        Date,
        nullable=False
    )

    house_id = Column(
        Integer,
        ForeignKey("houses.id"),
        unique=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True
    )

    house = relationship(
        "House",
        back_populates="tenants"
    )

    user = relationship(
        "User",
        back_populates="tenant"
    )

    payments = relationship(
        "Payment",
        back_populates="tenant",
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<Tenant {self.name}>"