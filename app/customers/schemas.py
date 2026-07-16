from pydantic import BaseModel
from typing import List


class CustomerBase(BaseModel):
    name: str
    email: str
    phone: str
    status: str   # new field


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    status: str | None = None   # new field


class CustomerResponse(CustomerBase):
    id: int

    class Config:
        from_attributes = True

class CustomerListResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: List[CustomerResponse]