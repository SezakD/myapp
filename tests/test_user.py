from fastapi.testclient import TestClient
from src.main import app
client = TestClient(app)
# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]
def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]
def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    # Отправляем email, которого нет в списке users
    response = client.get("/api/v1/user", params={'email': 'unknown@mail.com'})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {
        "name": "Sidor Sidorov",
        "email": "s.sidorov@mail.com"
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    # Проверяем, что вернулся ID (целое число)
    assert isinstance(response.json(), int)
def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    # Берем email уже существующего Ивана
    invalid_user = {
        "name": "Double Ivan",
        "email": users[0]['email']
    }
    response = client.post("/api/v1/user", json=invalid_user)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}
def test_delete_user():
    '''Удаление пользователя'''
    # Удаляем Петра
    target_email = users[1]['email']
    response = client.delete("/api/v1/user", params={'email': target_email})
    assert response.status_code == 204   
    # Проверяем, что он действительно удален (теперь должен быть 404)
    check_response = client.get("/api/v1/user", params={'email': target_email})
    assert check_response.status_code == 404

