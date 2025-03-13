from pydantic import BaseModel, Field
from typing import Optional

class CompanyCreate(BaseModel):
    nit: str = Field(...)
    name_company: str = Field(...)
    sector: str
    class Config:
        from_attributes = True

class CompanyResponse(BaseModel):
    nit: str
    name_company: str
    sector: Optional[str]

    class Config:
        from_attributes = True