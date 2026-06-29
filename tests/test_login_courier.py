import allure
import pytest
import requests
from ..new_user_generator import *
from ..data import ERROR_MESSAGES, CORRECT_LOGIN, CORRECT_PASSWORD

BASE_URL = 'https://qa-scooter.praktikum-services.ru'

@allure.feature('Логин курьера')
class TestLoginCourier:
    
    @allure.title('Проверка, что курьер может авторизоваться')
    def test_login_courier_success(self):
        login, password, first_name = register_new_courier_and_return_login_password()
        
        response = requests.post(
            f'{BASE_URL}/api/v1/courier/login',
            data={"login": login, "password": password}
        )
        
        assert response.status_code == 200
        
        courier_id = response.json().get('id')
        if courier_id:
            requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')
    
    @allure.title('Проверка, что для авторизации нужно передать все обязательные поля')
    @pytest.mark.parametrize('missing_field', [
                            {'login': '', 'password': CORRECT_PASSWORD},
                            {'login': CORRECT_LOGIN, 'password': ''},
                            ])
    def test_login_missing_fields(self, missing_field):
        
        response = requests.post(
            f'{BASE_URL}/api/v1/courier/login',
            data=missing_field
        )
        
        assert response.status_code == 400
        
        auth_response = requests.post(
            f'{BASE_URL}/api/v1/courier/login',
            data={"login": CORRECT_LOGIN, "password": CORRECT_PASSWORD}
        )
        if auth_response.status_code == 200:
            courier_id = auth_response.json().get('id')
            if courier_id:
                requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')
    
    @allure.title('Прверка, что система вернёт ошибку, если неправильно указать логин или пароль')
    @pytest.mark.parametrize('wrong_field', ['login', 'password'])
    def test_login_wrong_credentials(self, wrong_field):
        login, password, first_name = register_new_courier_and_return_login_password()
        
        if wrong_field == 'login':
            wrong_login = generate_random_string(10)
            response = requests.post(
                f'{BASE_URL}/api/v1/courier/login',
                data={"login": wrong_login, "password": password}
            )
        else:
            wrong_password = generate_random_string(10)
            response = requests.post(
                f'{BASE_URL}/api/v1/courier/login',
                data={"login": login, "password": wrong_password}
            )
        
        assert response.status_code == 404
        assert ERROR_MESSAGES['auth_failed'] in response.text
        

        auth_response = requests.post(
            f'{BASE_URL}/api/v1/courier/login',
            data={"login": login, "password": password}
        )
        if auth_response.status_code == 200:
            courier_id = auth_response.json().get('id')
            if courier_id:
                requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')

    @allure.title('Проверка, что если какого-то поля нет, запрос возвращает ошибку')
    @pytest.mark.parametrize('missing_field', [
                            {'login': '', 'password': CORRECT_PASSWORD},
                            {'login': CORRECT_LOGIN, 'password': ''},
                            ])
    def test_login_not_fields(self, missing_field):
        
        response = requests.post(
            f'{BASE_URL}/api/v1/courier/login',
            data=missing_field
        )
        
        assert ERROR_MESSAGES['missing_login_or_password'] in response.text
        
        auth_response = requests.post(
            f'{BASE_URL}/api/v1/courier/login',
            data={"login": CORRECT_LOGIN, "password": CORRECT_PASSWORD}
        )
        if auth_response.status_code == 200:
            courier_id = auth_response.json().get('id')
            if courier_id:
                requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')
    
    @allure.title('проверка, что если авторизоваться под несуществующим пользователем, запрос возвращает ошибку')
    def test_login_nonexistent_user(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        
        response = requests.post(
            f'{BASE_URL}/api/v1/courier/login',
            data={"login": login, "password": password}
        )
        
        assert response.status_code == 404
        assert ERROR_MESSAGES['auth_failed'] in response.text

    @allure.title('Проверка, что курьер может авторизоваться')
    def test_request_returns_id(self):
        login, password, first_name = register_new_courier_and_return_login_password()
        
        response = requests.post(
            f'{BASE_URL}/api/v1/courier/login',
            data={"login": login, "password": password}
        )
        
        assert 'id' in response.json()
        
        courier_id = response.json().get('id')
        if courier_id:
            requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')
