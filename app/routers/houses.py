from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.house import (
    HouseCreate,
    HouseUpdate,
    HouseResponse
)

from app.services.house_service import HouseService

from app.utils.roles import require_admin_or_owner

from app.models.house import HouseStatus

router = APIRouter(
    prefix="/houses",
    tags=["House Management"]
)


@router.post(
    "",
    response_model=HouseResponse
)
def create_house(
    request: HouseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_owner)
):
    return HouseService.create_house(
        db,
        request
    )


@router.get("")
def get_houses(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = None,
    house_type: str | None = None,
    status: HouseStatus | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_owner)
):
    return HouseService.get_all_houses(
        db=db,
        page=page,
        limit=limit,
        search=search,
        house_type=house_type,
        status=status
    )


@router.get(
    "/{house_id}",
    response_model=HouseResponse
)
def get_house(
    house_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_owner)
):
    return HouseService.get_house(
        db,
        house_id
    )


@router.put(
    "/{house_id}",
    response_model=HouseResponse
)
def update_house(
    house_id: int,
    request: HouseUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_owner)
):
    return HouseService.update_house(
        db,
        house_id,
        request
    )


@router.delete("/{house_id}")
def delete_house(
    house_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_owner)
):
    return HouseService.delete_house(
        db,
        house_id
    )