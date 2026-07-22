from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.models.tenant import Tenant
from app.models.payment import PaymentStatus

from app.schemas.payment import PaymentCreate
from app.schemas.payment import PaymentUpdate
from app.exceptions.custom_exceptions import (
    ResourceNotFoundException,
    DuplicatePaymentException,
    ValidationException
)


class PaymentService:

    @staticmethod
    def create_payment(
        db: Session,
        request: PaymentCreate
    ):

        
        tenant = (
            db.query(Tenant)
            .filter(
                Tenant.id == request.tenant_id
            )
            .first()
        )

        if tenant is None:
            raise ResourceNotFoundException(
                "Tenant not found."
            )

        
        if request.amount <= 0:
            raise ValidationException(
                "Amount must be greater than zero."
            )

        
        payment_exists = (
            db.query(Payment)
            .filter(
                Payment.tenant_id == request.tenant_id,
                Payment.payment_month == request.payment_month
            )
            .first()
        )

        if payment_exists:
            raise DuplicatePaymentException(
                "Payment already exists for this month."
            )

        payment = Payment(
            tenant_id=request.tenant_id,
            payment_month=request.payment_month,
            amount=request.amount,
            payment_date=request.payment_date,
            payment_method=request.payment_method,
            payment_status=request.payment_status
        )

        db.add(payment)

        db.commit()

        db.refresh(payment)

        return payment

    @staticmethod
    def get_payment(
        db: Session,
        payment_id: int
    ):

        payment = (
            db.query(Payment)
            .filter(
                Payment.id == payment_id
            )
            .first()
        )

        if payment is None:
            raise ResourceNotFoundException(
                "Payment not found."
            )

        return payment

    @staticmethod
    def get_all_payments(
        db: Session,
        page: int = 1,
        limit: int = 10
    ):

        query = db.query(Payment)

        total = query.count()

        payments = (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "data": payments
        }

    @staticmethod
    def update_payment(
        db: Session,
        payment_id: int,
        request: PaymentUpdate
    ):

        payment = (
            db.query(Payment)
            .filter(
                Payment.id == payment_id
            )
            .first()
        )

        if payment is None:
            raise ResourceNotFoundException(
                "Payment not found."
            )

        update_data = request.model_dump(
            exclude_unset=True
        )

        if (
            "amount" in update_data
            and update_data["amount"] <= 0
        ):
            raise ValidationException(
                "Amount must be greater than zero."
            )

        for key, value in update_data.items():
            setattr(payment, key, value)

        db.commit()

        db.refresh(payment)

        return payment

    @staticmethod
    def delete_payment(
        db: Session,
        payment_id: int
    ):

        payment = (
            db.query(Payment)
            .filter(
                Payment.id == payment_id
            )
            .first()
        )

        if payment is None:
            raise ResourceNotFoundException(
                "Payment not found."
            )

        db.delete(payment)

        db.commit()

        return {
            "message":
            "Payment deleted successfully."
        }

    @staticmethod
    def mark_payment_paid(
        db: Session,
        payment_id: int
    ):

        payment = (
            db.query(Payment)
            .filter(
                Payment.id == payment_id
            )
            .first()
        )

        if payment is None:
            raise ResourceNotFoundException(
                "Payment not found."
            )

        payment.payment_status = (
            PaymentStatus.PAID
        )

        db.commit()

        db.refresh(payment)

        return payment

    @staticmethod
    def mark_payment_overdue(
        db: Session,
        payment_id: int
    ):

        payment = (
            db.query(Payment)
            .filter(
                Payment.id == payment_id
            )
            .first()
        )

        if payment is None:
            raise ResourceNotFoundException(
                "Payment not found."
            )

        payment.payment_status = (
            PaymentStatus.OVERDUE
        )

        db.commit()

        db.refresh(payment)

        return payment