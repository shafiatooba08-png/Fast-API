from pydantic import BaseModel
from typing import List


class PropertyNested(BaseModel):
    id: int
    title: str
    price: int
    location: str

    class Config:
        from_attributes = True


class CustomerNested(BaseModel):
    id: int
    name: str
    email: str
    phone: str

    class Config:
        from_attributes = True


class LeadBase(BaseModel):
    status: str
    property_id: int
    customer_id: int


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    status: str | None = None
    property_id: int | None = None
    customer_id: int | None = None


class LeadResponse(LeadBase):
    id: int

    class Config:
        from_attributes = True


class LeadDetailResponse(BaseModel):
    id: int
    status: str
    property: PropertyNested
    customer: CustomerNested

    class Config:
        from_attributes = True
class LeadListResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: List[LeadResponse]