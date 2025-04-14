
def test_create_table(client):
    response = client.post("/tables/", json={
        "name": "Table 3",
        "seats": 4,
        "location": "зал у двери"
    })
    print(response.json())  # Добавим вывод для анализа ошибки
    assert response.status_code == 201
    assert response.json()["name"] == "Table 3"


def test_get_tables(client):
    response = client.get("/tables/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_table(client):
    # Сначала создаём столик
    create_resp = client.post("/tables/", json={
        "name": "ToDelete",
        "seats": 2,
        "location": "терраса"
    })
    table_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/tables/{table_id}")
    assert delete_resp.status_code == 204

    get_resp = client.get("/tables/")
    assert all(t["id"] != table_id for t in get_resp.json())

