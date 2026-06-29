import pytest
import requests
from .new_user_generator import *

@pytest.fixture
def created_courier():
    login, password, first_name = register_new_courier_and_return_login_password()
    if not login:
        pytest.fail("Не удалось создать курьера")
    
    yield {"login": login, "password": password, "first_name": first_name}
    
    delete_courier(login, password)

def delete_courier(login, password):
    BASE_URL = 'https://qa-scooter.praktikum-services.ru'
    
    response = requests.post(
        f'{BASE_URL}/api/v1/courier/login',
        data={"login": login, "password": password}
    )
    
    if response.status_code == 200:
        courier_id = response.json().get('id')
        if courier_id:
            requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')
