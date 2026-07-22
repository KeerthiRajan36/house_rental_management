from sqlalchemy.orm import Session

from app.models.tenant import Tenant
from app.models.house import House
from app.models.house import HouseStatus

from app.schemas.tenant import TenantCreate ,TenantUpdate

from app.exceptions.custom_exceptions import (
    ResourceNotFoundException,
    DuplicateRecordException,
    HouseOccupiedException,
    TenantAlreadyAssignedException,
    ValidationException
)


class TenantService:

    @staticmethod
    def create_tenant(
        db: Session,
        request: TenantCreate
    ):

        
        email_exists = (
            db.query(Tenant)
            .filter(Tenant.email == request.email)
            .first()
        )

        if email_exists:
            raise DuplicateRecordException(
                "Email already exists."
            )

        
        aadhaar_exists = (
            db.query(Tenant)
            .filter(
                Tenant.aadhaar_number ==
                request.aadhaar_number
            )
            .first()
        )

        if aadhaar_exists:
            raise DuplicateRecordException(
                "Aadhaar already exists."
            )


        house = (
            db.query(House)
            .filter(
                House.id == request.house_id
            )
            .first()
        )

        if house is None:
            raise ResourceNotFoundException(
                "House not found."
            )

        if house.availability_status != HouseStatus.AVAILABLE:
            raise HouseOccupiedException(
                "Selected house is not available."
            )

        assigned = (
            db.query(Tenant)
            .filter(
                Tenant.user_id ==
                request.user_id
            )
            .first()
        )

        if assigned:
            raise TenantAlreadyAssignedException(
                "Tenant already assigned to a house."
            )


        if (
            request.agreement_end_date
            <= request.move_in_date
        ):
            raise ValidationException(
                "Agreement end date must be after move-in date."
            )

  
        tenant = Tenant(
            name=request.name,
            email=request.email,
            phone=request.phone,
            aadhaar_number=request.aadhaar_number,
            house_id=request.house_id,
            user_id=request.user_id,
            move_in_date=request.move_in_date,
            agreement_end_date=request.agreement_end_date
        )

        db.add(tenant)


        house.availability_status = (
            HouseStatus.OCCUPIED
        )

        db.commit()

        db.refresh(tenant)

        return tenant

    @staticmethod
    def get_tenant(
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

        return tenant

    @staticmethod
    def get_all_tenants(
        db: Session,
        page: int = 1,
        limit: int = 10
    ):

        query = db.query(Tenant)

        total = query.count()

        tenants = (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "data": tenants
        }

    @staticmethod
    def update_tenant(
        db: Session,
        tenant_id: int,
        request: TenantUpdate
    ):

        tenant = (
            db.query(Tenant)
            .filter(Tenant.id == tenant_id)
            .first()
        )

        if tenant is None:
            raise ResourceNotFoundException(
                "Tenant not found."
            )

        update_data = request.model_dump(
            exclude_unset=True
        )

        # -----------------------------
        # House Transfer
        # -----------------------------
        if "house_id" in update_data:

            new_house = (
                db.query(House)
                .filter(
                    House.id == update_data["house_id"]
                )
                .first()
            )

            if new_house is None:
                raise ResourceNotFoundException(
                    "New house not found."
                )

            if (
                new_house.availability_status
                != HouseStatus.AVAILABLE
            ):
                raise HouseOccupiedException(
                    "Selected house is occupied."
                )

            old_house = (
                db.query(House)
                .filter(
                    House.id == tenant.house_id
                )
                .first()
            )

            if old_house:
                old_house.availability_status = (
                    HouseStatus.AVAILABLE
                )

            new_house.availability_status = (
                HouseStatus.OCCUPIED
            )

        # -----------------------------
        # Agreement Validation
        # -----------------------------
        move_in = update_data.get(
            "move_in_date",
            tenant.move_in_date
        )

        agreement = update_data.get(
            "agreement_end_date",
            tenant.agreement_end_date
        )

        if agreement <= move_in:
            raise ValidationException(
                "Agreement end date must be after move-in date."
            )

        # -----------------------------
        # Update Fields
        # -----------------------------
        for key, value in update_data.items():
            setattr(tenant, key, value)

        db.commit()

        db.refresh(tenant)

        return tenant


    @staticmethod
    def delete_tenant(
        db: Session,
        tenant_id: int
    ):

        tenant = (
            db.query(Tenant)
            .filter(Tenant.id == tenant_id)
            .first()
        )

        if tenant is None:
            raise ResourceNotFoundException(
                "Tenant not found."
            )

        house = (
            db.query(House)
            .filter(
                House.id == tenant.house_id
            )
            .first()
        )

        if house:

            house.availability_status = (
                HouseStatus.AVAILABLE
            )

        db.delete(tenant)

        db.commit()

        return {
            "message":
            "Tenant removed successfully."
        }