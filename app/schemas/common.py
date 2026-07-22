from pydantic import BaseModel
from pydantic import ConfigDict


class MessageResponse(BaseModel):

    message: str

    model_config = ConfigDict(from_attributes=True)


class PaginationResponse(BaseModel):

    page: int

    limit: int

    total: int

    model_config = ConfigDict(from_attributes=True)