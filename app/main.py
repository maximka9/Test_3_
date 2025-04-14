from fastapi import FastAPI
from app.routers import table, reservation

app = FastAPI(
    title="Restaurant Reservation API",
    version="1.0.0"
)

app.include_router(table.router)
app.include_router(reservation.router)
