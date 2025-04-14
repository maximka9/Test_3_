from datetime import datetime
from pydantic import BaseModel, Field


class ReservationBase(BaseModel):
    customer_name: str = Field(..., example="Иван Иванов")
    table_id: int = Field(..., example=1)
    reservation_time: datetime = Field(..., example="2025-04-14T19:00:00")
    duration_minutes: int = Field(..., gt=0, example=90)


class ReservationCreate(ReservationBase):
    pass


class ReservationRead(ReservationBase):
    id: int

    class Config:
        orm_mode = True
