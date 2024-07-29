from typing import Optional
from sqlmodel import SQLModel, Field


class Advertisement(SQLModel, table=True):
    ad_id: int = Field(default=None, primary_key=True, unique=True)
    title: str
    author: str
    view_count: int
    position: int


class AdvertisementUpdate(SQLModel):
    title: Optional[str] = None
    ad_id: Optional[int] = None
    author: Optional[str] = None
    view_count: Optional[int] = None
    position: Optional[int] = None
