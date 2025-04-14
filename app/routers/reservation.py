from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.reservation import ReservationRead, ReservationCreate  # ← здесь
from app.services import table  # Правильный импорт для файла table.py
from app.services import reservation  # Импорт для файла reservation.py
from app.db.session import get_db

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.get("/", response_model=List[ReservationRead])
def read_reservations(db: Session = Depends(get_db)):
    return services.reservation.get_reservations(db)


@router.post("/", response_model=ReservationRead, status_code=status.HTTP_201_CREATED)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    return services.reservation.create_reservation(db, reservation)


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    services.reservation.delete_reservation(db, reservation_id)
    return
