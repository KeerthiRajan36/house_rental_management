from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from app.models.house import HouseStatus


class HouseCreate(BaseModel):

    house_name: str

    address: str

    rent_amount: float = Field(gt=0)

    house_type: str

    availability_status: HouseStatus = HouseStatus.AVAILABLE


class HouseUpdate(BaseModel):

    house_name: str | None = None

    address: str | None = None

    rent_amount: float | None = Field(default=None, gt=0)

    house_type: str | None = None

    availability_status: HouseStatus | None = None


class HouseResponse(BaseModel):

    id: int

    house_name: str

    address: str

    rent_amount: float

    house_type: str

    availability_status: HouseStatus

    model_config = ConfigDict(from_attributes=True)