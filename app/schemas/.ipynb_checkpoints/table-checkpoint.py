from pydantic import BaseModel, Field


class TableBase(BaseModel):
    name: str = Field(..., example="Table 1")
    seats: int = Field(..., gt=0, example=4)
    location: str = Field(..., example="зал у окна")


class TableCreate(TableBase):
    pass


class TableRead(TableBase):
    id: int

    class Config:
        orm_mode = True
