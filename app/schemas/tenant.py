from datetime import date

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import field_validator


class TenantCreate(BaseModel):

    name: str

    email: EmailStr

    phone: str

    aadhaar_number: str

    house_id: int

    user_id: int

    move_in_date: date

    agreement_end_date: date

    @field_validator("aadhaar_number")
    @classmethod
    def validate_aadhaar(cls, value):

        if len(value) != 12:
            raise ValueError("Aadhaar must contain exactly 12 digits")

        if not value.isdigit():
            raise ValueError("Aadhaar must contain only digits")

        return value

    @field_validator("agreement_end_date")
    @classmethod
    def validate_dates(cls, value, info):

        move_in = info.data.get("move_in_date")

        if move_in and value <= move_in:
            raise ValueError(
                "Agreement end date must be after move-in date"
            )

        return value


class TenantUpdate(BaseModel):

    name: str | None = None

    phone: str | None = None

    house_id: int | None = None

    move_in_date: date | None = None

    agreement_end_date: date | None = None


class TenantResponse(BaseModel):

    id: int

    name: str

    email: EmailStr

    phone: str

    aadhaar_number: str

    house_id: int

    move_in_date: date

    agreement_end_date: date

    model_config = ConfigDict(from_attributes=True)