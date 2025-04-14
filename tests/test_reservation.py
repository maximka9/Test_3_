
from datetime import datetime, timedelta


def test_create_reservation(client):
    # Создаем столик
    table_resp = client.post("/tables/", json={
        "name": "Reserved",
        "seats": 2,
        "location": "зал"
    })
    table_id = table_resp.json()["id"]
    print(table_resp.json())  # Добавьте эту строку для отладки

    reservation_time = datetime.utcnow()

    response = client.post("/reservations/", json={
        "customer_name": "Иван",
        "table_id": table_id,
        "reservation_time": reservation_time.isoformat(),  # передаем строку ISO
        "duration_minutes": 60
    })
    print(response.json())  # Для отладки
    # Проверяем статус код
    assert response.status_code == 201

    # Проверяем наличие id в ответе
    assert "id" in response.json()
    assert response.json()["customer_name"] == "Иван"




def test_reservation_conflict(client):
    table_resp = client.post("/tables/", json={
        "name": "Conflict",
        "seats": 2,
        "location": "зал"
    })
    table_id = table_resp.json()["id"]

    # Правильное время
    reservation_time = datetime.utcnow().replace(microsecond=0)

    # Первая бронь
    client.post("/reservations/", json={
        "customer_name": "Алексей",
        "table_id": table_id,
        "reservation_time": reservation_time.isoformat(),  # передаем строку ISO
        "duration_minutes": 90
    })

    # Вторая бронь с пересечением
    response = client.post("/reservations/", json={
        "customer_name": "Олег",
        "table_id": table_id,
        "reservation_time": reservation_time.isoformat(),  # передаем строку ISO
        "duration_minutes": 30
    })

    assert response.status_code == 409
    assert "Столик уже забронирован" in response.json()["detail"]



def test_delete_reservation(client):
    table_resp = client.post("/tables/", json={
        "name": "DelReserve",
        "seats": 2,
        "location": "зал"
    })
    table_id = table_resp.json()["id"]

    reservation_time = datetime.utcnow().isoformat()
    res_resp = client.post("/reservations/", json={
        "customer_name": "Сергей",
        "table_id": table_id,
        "reservation_time": reservation_time,
        "duration_minutes": 45
    })

    res_id = res_resp.json()["id"]

    delete_resp = client.delete(f"/reservations/{res_id}")
    assert delete_resp.status_code == 204
