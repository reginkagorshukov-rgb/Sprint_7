import allure
import requests

BASE_URL = 'https://qa-scooter.praktikum-services.ru'

@allure.feature('Список заказов')
class TestOrdersList:
    
    @allure.title('Проверка, что тело ответа возвращается список заказов')
    def test_orders_list_returns_list(self):
        response = requests.get(f'{BASE_URL}/api/v1/orders')
        
        assert response.status_code == 200
        response_json = response.json()
        assert 'orders' in response_json
        assert isinstance(response_json['orders'], list)