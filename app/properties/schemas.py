from pydantic import BaseModel
from typing import List


class PropertyBase(BaseModel):
    title: str
    description: str
    price: int
    location: str
    area: int
    beds: int


class PropertyCreate(PropertyBase):
    pass


class PropertyResponse(PropertyBase):
    id: int

    class Config:
        from_attributes = True
        
class PropertyUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    location: str | None = None
    area: int | None = None
    beds: int | None = None
    
    # Pagination response
class PropertyListResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: List[PropertyResponse]