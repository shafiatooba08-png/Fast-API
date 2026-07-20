from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List
from enum import Enum


# Allowed customer statuses
class CustomerStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    blocked = "blocked"


# Common fields
class CustomerBase(BaseModel):

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Customer full name"
    )

    email: EmailStr

    phone: str = Field(
        ...,
        min_length=10,
        max_length=15,
        description="Customer phone number"
    )

    status: CustomerStatus = CustomerStatus.active


# Used when creating customer
class CustomerCreate(CustomerBase):
    pass


# Used for partial updates (PATCH)
class CustomerUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    email: EmailStr | None = None

    phone: str | None = Field(
        default=None,
        min_length=10,
        max_length=15
    )

    status: CustomerStatus | None = None


# Response schema
class CustomerResponse(CustomerBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


# Pagination response
class CustomerListResponse(BaseModel):

    total: int
    page: int
    limit: int
    data: List[CustomerResponse]