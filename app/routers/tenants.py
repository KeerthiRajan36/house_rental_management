from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.tenant import (
    TenantCreate,
    TenantUpdate,
    TenantResponse
)

from app.services.tenant_service import TenantService

from app.utils.roles import require_admin_or_owner

router = APIRouter(
    prefix="/tenants",
    tags=["Tenant Management"]
)


@router.post(
    "",
    response_model=TenantResponse,
    status_code=201
)
def create_tenant(
    request: TenantCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_owner)
):
    return TenantService.create_tenant(
        db,
        request
    )


@router.get("")
def get_all_tenants(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_owner)
):
    return TenantService.get_all_tenants(
        db=db,
        page=page,
        limit=limit
    )


@router.get(
    "/{tenant_id}",
    response_model=TenantResponse
)
def get_tenant(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_owner)
):
    return TenantService.get_tenant(
        db,
        tenant_id
    )


@router.put(
    "/{tenant_id}",
    response_model=TenantResponse
)
def update_tenant(
    tenant_id: int,
    request: TenantUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_owner)
):
    return TenantService.update_tenant(
        db,
        tenant_id,
        request
    )


@router.delete("/{tenant_id}")
def delete_tenant(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_owner)
):
    return TenantService.delete_tenant(
        db,
        tenant_id
    )