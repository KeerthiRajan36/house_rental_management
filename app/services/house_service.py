from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.house import House
from app.models.house import HouseStatus
from app.models.tenant import Tenant

from app.schemas.house import (
    HouseCreate,
    HouseUpdate
)

from app.exceptions.custom_exceptions import (
    ResourceNotFoundException,
    ValidationException
)


class HouseService:

    @staticmethod
    def create_house(
        db: Session,
        request: HouseCreate
    ):

        if request.rent_amount <= 0:
            raise ValidationException(
                "Rent amount must be greater than 0"
            )

        house = House(
            house_name=request.house_name,
            address=request.address,
            rent_amount=request.rent_amount,
            house_type=request.house_type,
            availability_status=request.availability_status
        )

        db.add(house)
        db.commit()
        db.refresh(house)

        return house

    @staticmethod
    def get_house(
        db: Session,
        house_id: int
    ):

        house = (
            db.query(House)
            .filter(House.id == house_id)
            .first()
        )

        if not house:
            raise ResourceNotFoundException(
                "House not found"
            )

        return house

    @staticmethod
    def get_all_houses(
        db: Session,
        page: int = 1,
        limit: int = 10,
        search: str = None,
        house_type: str = None,
        status: HouseStatus = None
    ):

        query = db.query(House)

        if search:

            query = query.filter(
                House.address.ilike(f"%{search}%")
            )

        if house_type:

            query = query.filter(
                House.house_type == house_type
            )

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
            "total": total,
            "page": page,
            "limit": limit,
            "data": houses
        }

    @staticmethod
    def update_house(
        db: Session,
        house_id: int,
        request: HouseUpdate
    ):

        house = (
            db.query(House)
            .filter(House.id == house_id)
            .first()
        )

        if house is None:
            raise ResourceNotFoundException(
                "House not found"
            )

        if (
            request.rent_amount is not None
            and request.rent_amount <= 0
        ):
            raise ValidationException(
                "Rent amount must be greater than 0"
            )

        # Prevent manual status change while occupied
        active_tenant = (
            db.query(Tenant)
            .filter(Tenant.house_id == house.id)
            .first()
        )

        if (
            active_tenant
            and request.availability_status == HouseStatus.AVAILABLE
        ):
            raise ValidationException(
                "Cannot mark an occupied house as Available."
            )

        update_data = request.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(house, key, value)

        db.commit()
        db.refresh(house)

        return house

    @staticmethod
    def delete_house(
        db: Session,
        house_id: int
    ):

        house = (
            db.query(House)
            .filter(House.id == house_id)
            .first()
        )

        if house is None:
            raise ResourceNotFoundException(
                "House not found"
            )

        active_tenant = (
            db.query(Tenant)
            .filter(Tenant.house_id == house.id)
            .first()
        )

        if active_tenant:
            raise ValidationException(
                "Cannot delete a house that has an active tenant."
            )

        db.delete(house)
        db.commit()

        return {
            "message": "House deleted successfully."
        }

    @staticmethod
    def mark_under_maintenance(
        db: Session,
        house_id: int
    ):

        house = (
            db.query(House)
            .filter(House.id == house_id)
            .first()
        )

        if house is None:
            raise ResourceNotFoundException(
                "House not found"
            )

        active_tenant = (
            db.query(Tenant)
            .filter(Tenant.house_id == house.id)
            .first()
        )

        if active_tenant:
            raise ValidationException(
                "Occupied houses cannot be marked as under maintenance."
            )

        house.availability_status = (
            HouseStatus.UNDER_MAINTENANCE
        )

        db.commit()
        db.refresh(house)

        return house

    @staticmethod
    def mark_available(
        db: Session,
        house_id: int
    ):

        house = (
            db.query(House)
            .filter(House.id == house_id)
            .first()
        )

        if house is None:
            raise ResourceNotFoundException(
                "House not found"
            )

        active_tenant = (
            db.query(Tenant)
            .filter(Tenant.house_id == house.id)
            .first()
        )

        if active_tenant:
            raise ValidationException(
                "House still has an active tenant."
            )

        house.availability_status = (
            HouseStatus.AVAILABLE
        )

        db.commit()
        db.refresh(house)

        return house