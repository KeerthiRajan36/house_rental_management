from datetime import date

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from app.models.payment import PaymentStatus


class PaymentCreate(BaseModel):

    tenant_id: int

    payment_month: str

    amount: float = Field(gt=0)

    payment_date: date

    payment_method: str

    payment_status: PaymentStatus


class PaymentUpdate(BaseModel):

    amount: float | None = Field(default=None, gt=0)

    payment_date: date | None = None

    payment_method: str | None = None

    payment_status: PaymentStatus | None = None


class PaymentResponse(BaseModel):

    id: int

    tenant_id: int

    payment_month: str

    amount: float

    payment_date: date

    payment_method: str

    payment_status: PaymentStatus

    model_config = ConfigDict(from_attributes=True)