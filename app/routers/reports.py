from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.house import HouseStatus

from app.services.report_service import ReportService

from app.utils.roles import (
    require_admin_or_owner
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/houses")
def search_houses(
    search: str | None = None,
    house_type: str | None = None,
    status: HouseStatus | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_owner)
):

    return ReportService.search_houses(
        db=db,
        search=search,
        house_type=house_type,
        status=status,
        page=page,
        limit=limit
    )


@router.get("/statistics")
def house_statistics(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_owner)
):

    return ReportService.get_house_statistics(db)


@router.get("/tenant/{tenant_id}/payments")
def payment_history(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_owner)
):

    return ReportService.get_tenant_payment_history(
        db,
        tenant_id
    )


@router.get("/payments/overdue")
def overdue_payments(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_owner)
):

    return ReportService.get_overdue_payments(
        db=db,
        page=page,
        limit=limit
    )


@router.get("/dashboard")
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_owner)
):

    return ReportService.dashboard_summary(
        db
    )