from sqlalchemy import Column, Integer, String, Float, Enum
from sqlalchemy.orm import relationship
import enum

from app.database.database import Base


class HouseStatus(str, enum.Enum):
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    UNDER_MAINTENANCE = "Under Maintenance"


class House(Base):
    __tablename__ = "houses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    house_name = Column(
        String(100),
        nullable=False
    )

    address = Column(
        String(300),
        nullable=False,
        index=True
    )

    rent_amount = Column(
        Float,
        nullable=False
    )

    house_type = Column(
        String(50),
        nullable=False,
        index=True
    )

    availability_status = Column(
        Enum(HouseStatus),
        nullable=False,
        default=HouseStatus.AVAILABLE
    )

    tenants = relationship(
        "Tenant",
        back_populates="house",
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<House {self.house_name}>"