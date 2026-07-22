from sqlalchemy.orm import Session
from sqlalchemy import or_ , func

from app.models.payment import Payment
from app.models.payment import PaymentStatus
from app.models.house import House
from app.models.house import HouseStatus
from app.models.tenant import Tenant

from app.exceptions.custom_exceptions import (
    ResourceNotFoundException
)


class ReportService:

    @staticmethod
    def search_houses(
        db: Session,
        search: str = None,
        house_type: str = None,
        status: HouseStatus = None,
        page: int = 1,
        limit: int = 10
    ):

        query = db.query(House)

        # Search by address or house name
        if search:

            query = query.filter(
                or_(
                    House.address.ilike(f"%{search}%"),
                    House.house_name.ilike(f"%{search}%")
                )
            )

        # Filter by house type
        if house_type:

            query = query.filter(
                House.house_type == house_type
            )

        # Filter by availability
        if status:

            query = query.filter(
                House.availability_status == status
            )

        total = query.count()

        houses = (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "data": houses
        }

    @staticmethod
    def get_house_statistics(
        db: Session
    ):

        total = db.query(House).count()

        available = (
            db.query(House)
            .filter(
                House.availability_status ==
                HouseStatus.AVAILABLE
            )
            .count()
        )

        occupied = (
            db.query(House)
            .filter(
                House.availability_status ==
                HouseStatus.OCCUPIED
            )
            .count()
        )

        maintenance = (
            db.query(House)
            .filter(
                House.availability_status ==
                HouseStatus.UNDER_MAINTENANCE
            )
            .count()
        )

        return {
            "total_houses": total,
            "available": available,
            "occupied": occupied,
            "under_maintenance": maintenance
        }

    @staticmethod
    def get_tenant_payment_history(
        db: Session,
        tenant_id: int
    ):

        tenant = (
            db.query(Tenant)
            .filter(
                Tenant.id == tenant_id
            )
            .first()
        )

        if tenant is None:
            raise ResourceNotFoundException(
                "Tenant not found."
            )

        payments = (
            db.query(Payment)
            .filter(
                Payment.tenant_id == tenant_id
            )
            .order_by(
                Payment.payment_date.desc()
            )
            .all()
        )

        return {
            "tenant": tenant,
            "payments": payments
        }

    @staticmethod
    def get_overdue_payments(
        db: Session,
        page: int = 1,
        limit: int = 10
    ):

        query = (
            db.query(Payment)
            .join(
                Tenant,
                Payment.tenant_id == Tenant.id
            )
            .filter(
                Payment.payment_status ==
                PaymentStatus.OVERDUE
            )
        )

        total = query.count()

        records = (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "data": records
        }

    @staticmethod
    def dashboard_summary(
        db: Session
    ):

        total_houses = (
            db.query(House).count()
        )

        total_tenants = (
            db.query(Tenant).count()
        )

        total_payments = (
            db.query(Payment).count()
        )

        paid = (
            db.query(Payment)
            .filter(
                Payment.payment_status ==
                PaymentStatus.PAID
            )
            .count()
        )

        pending = (
            db.query(Payment)
            .filter(
                Payment.payment_status ==
                PaymentStatus.PENDING
            )
            .count()
        )

        overdue = (
            db.query(Payment)
            .filter(
                Payment.payment_status ==
                PaymentStatus.OVERDUE
            )
            .count()
        )

        revenue = (
            db.query(
                func.sum(
                    Payment.amount
                )
            )
            .filter(
                Payment.payment_status ==
                PaymentStatus.PAID
            )
            .scalar()
        )

        return {
            "total_houses": total_houses,
            "total_tenants": total_tenants,
            "total_payments": total_payments,
            "paid_payments": paid,
            "pending_payments": pending,
            "overdue_payments": overdue,
            "total_revenue": revenue or 0
        }