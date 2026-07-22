from sqlalchemy import Column, Integer, Float, String, Date, Enum, ForeignKey

from sqlalchemy.orm import relationship

import enum

from app.database.database import Base


class PaymentStatus(str, enum.Enum):
    PENDING = "Pending"
    PAID = "Paid"
    OVERDUE = "Overdue"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id")
    )

    payment_month = Column(
        String(20),
        nullable=False
    )

    amount = Column(
        Float,
        nullable=False
    )

    payment_date = Column(
        Date,
        nullable=False
    )

    payment_method = Column(
        String(30),
        nullable=False
    )

    payment_status = Column(
        Enum(PaymentStatus),
        nullable=False
    )

    tenant = relationship(
        "Tenant",
        back_populates="payments"
    )

    def __repr__(self):
        return f"<Payment {self.payment_month}>"