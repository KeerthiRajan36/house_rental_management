from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.payment import (
    PaymentCreate,
    PaymentUpdate,
    PaymentResponse
)

from app.services.payment_service import PaymentService

from app.utils.roles import require_admin_or_owner

router = APIRouter(
    prefix="/payments",
    tags=["Payment Management"]
)


@router.post(
    "",
    response_model=PaymentResponse,
    status_code=201
)
def create_payment(
    request: PaymentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_owner)
):
    return PaymentService.create_payment(
        db,
        request
    )


@router.get("")
def get_all_payments(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_owner)
):
    return PaymentService.get_all_payments(
        db=db,
        page=page,
        limit=limit
    )


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse
)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_owner)
):
    return PaymentService.get_payment(
        db,
        payment_id
    )


@router.put(
    "/{payment_id}",
    response_model=PaymentResponse
)
def update_payment(
    payment_id: int,
    request: PaymentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_owner)
):
    return PaymentService.update_payment(
        db,
        payment_id,
        request
    )


@router.delete("/{payment_id}")
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_owner)
):
    return PaymentService.delete_payment(
        db,
        payment_id
    )