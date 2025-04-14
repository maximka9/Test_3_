from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.table import Table  # Импортируем модель Table из app.models.table
from app.schemas.table import TableCreate, TableRead  # Импортируем схемы TableCreate и TableRead

def create_table(db: Session, table: TableCreate) -> Table:  # Используем Table напрямую
    db_table = Table(**table.dict())  # Создаем экземпляр модели Table
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

def get_tables(db: Session):
    return db.query(Table).all()  # Используем Table напрямую

def delete_table(db: Session, table_id: int):
    table = db.query(Table).filter(Table.id == table_id).first()  # Используем Table напрямую
    if not table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Столик не найден")

    db.delete(table)
    db.commit()
