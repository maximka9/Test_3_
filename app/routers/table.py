from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas import table  # Импортируем из app.schemas.table
from app import services
from app.db.session import get_db

router = APIRouter(prefix="/tables", tags=["Tables"])


@router.get("/", response_model=List[table.TableRead])  # Используем table.TableRead
def read_tables(db: Session = Depends(get_db)):
    return services.table.get_tables(db)


@router.post("/", response_model=table.TableRead, status_code=status.HTTP_201_CREATED)  # Используем table.TableRead
def create_table(table: table.TableCreate, db: Session = Depends(get_db)):  # Используем table.TableCreate
    return services.table.create_table(db, table)


@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_table(table_id: int, db: Session = Depends(get_db)):
    services.table.delete_table(db, table_id)
    return
