from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.reservation import Reservation  # Импортируем модель Reservation
from app.schemas.reservation import ReservationCreate  # Импортируем схему ReservationCreate
from fastapi import HTTPException, status

def is_conflict(db: Session, table_id: int, start_time: datetime, duration: int) -> bool:
    """
    Проверяет, есть ли пересечения по времени для заданного столика.
    """
    end_time = start_time + timedelta(minutes=duration)

    overlapping_reservations = db.query(Reservation).filter(
        Reservation.table_id == table_id,
        and_(
            Reservation.reservation_time < end_time,
            (Reservation.reservation_time + timedelta(minutes=Reservation.duration_minutes)) > start_time
        )
    ).first()

    return overlapping_reservations is not None

def create_reservation(db: Session, reservation: ReservationCreate) -> Reservation:
    if is_conflict(db, reservation.table_id, reservation.reservation_time, reservation.duration_minutes):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Столик уже забронирован на указанное время"
        )

    db_reservation = Reservation(**reservation.dict())  # Создание бронирования
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    
    # Убедись, что возвращается объект с id
    return db_reservation


def get_reservations(db: Session):
    return db.query(Reservation).all()  # Используем модель Reservation

def delete_reservation(db: Session, reservation_id: int):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Бронь не найдена")
    db.delete(reservation)
    db.commit()
