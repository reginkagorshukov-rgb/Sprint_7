import allure
import pytest
import requests
from ..api_helpers import *
from ..helpers import *
from ..data import ERROR_MESSAGES
from ..urls import Urls

@allure.feature('Создание курьера')
class TestCreateCourier:
    
    @allure.title('Проверка, что можно создать курьера')
    def test_create_courier_success(self, created_courier):
        
        auth_response = requests.post(
            f'{Urls.BASE_URL+Urls.LOGIN}',
            data={"login": created_courier['login'], "password": created_courier['password']}
        )
        assert auth_response.status_code == 200
    
    @allure.title('Проверка, что нельзя создать двух одинаковых курьеров')
    def test_create_duplicate_courier(self, created_courier):
        payload = {
            "login": created_courier['login'],
            "password": created_courier['password'],
            "firstName": created_courier['first_name']
        }
        response = requests.post(f'{Urls.BASE_URL+Urls.COURIER}', data=payload)
        
        assert response.status_code == 409
        assert ERROR_MESSAGES['login_already_exists'] in response.text
    
    @allure.title('Проверка, что для создания курьера нужны все обязательные поля')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_create_courier_missing_fields(self, missing_field, created_courier):
        payload = {
            "login": created_courier['login'],
            "password": created_courier['password'],
            "firstName": created_courier['first_name']
        }
        del payload[missing_field]
        
        response = requests.post(f'{Urls.BASE_URL+Urls.COURIER}', data=payload)
        assert response.status_code == 400

    @allure.title('Проверка, что запрос возвращает правильный код ответа')
    def test_request_returns_correct_code(self, created_courier):
        auth_response = requests.post(
            f'{Urls.BASE_URL+Urls.LOGIN}',
            data={"login": created_courier['login'], "password": created_courier['password']}
        )
        assert auth_response.status_code == 200
    
    @allure.title('Проверка, что успешный запрос возвращает {{"ok": true}}')
    def test_request_returns_ok_true(self):
        login, password, first_name = generate_courier_data()
    
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post(f'{Urls.BASE_URL+Urls.COURIER}', data=payload)
    
   
        assert response.status_code == 201
        assert response.json() == {'ok': True}

        auth_response = requests.post(
            f'{Urls.BASE_URL+Urls.LOGIN}',
            data={"login": login, "password": password}
        )
        if auth_response.status_code == 200:
            courier_id = auth_response.json().get('id')
            if courier_id:
                requests.delete(f'{Urls.BASE_URL+Urls.COURIER}/{courier_id}')
    
    @allure.title('Проверка, что если одного из полей нет, запрос возвращает ошибку')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_create_courier_missing_fields_error(self, missing_field, created_courier):
        payload = {
            "login": created_courier['login'],
            "password": created_courier['password'],
            "firstName": created_courier['first_name']
        }
        del payload[missing_field]
        
        response = requests.post(f'{Urls.BASE_URL+Urls.COURIER}', data=payload)
        assert response.status_code == 400
        assert ERROR_MESSAGES['missing_fields'] in response.text

    @allure.title('Проверка, что если создать пользователя с логином, который уже есть, возвращается ошибка')
    def test_create_courier_existing_login(self, created_courier):
        new_password = generate_random_string(10)
        new_first_name = generate_random_string(10)
        
        payload = {
            "login": created_courier['login'],
            "password": new_password,
            "firstName": new_first_name
        }
        response = requests.post(f'{Urls.BASE_URL+Urls.COURIER}', data=payload)
        
        assert response.status_code == 409
        assert ERROR_MESSAGES['login_already_exists'] in response.text