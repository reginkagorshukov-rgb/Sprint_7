import allure
import random
import string
import requests
from .urls import Urls

@allure.step('Генерация случайной строки')
def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

@allure.step('Генерация данных курьера')
def generate_courier_data():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    return login, password, first_name

@allure.step('Отмена заказа по треку track')
def cancel_order(track):
    response = requests.put(
        f'{Urls.BASE_URL+Urls.CANCEL}',
        json={"track": track}
    )
    return response

@allure.step('Генерация данных заказа')
def generate_order_data(color=None):
    first_names = ["Алексей", "Мария", "Иван", "Елена", "Дмитрий"]
    last_names = ["Иванов", "Петрова", "Сидоров", "Козлова", "Смирнов"]
    addresses = ["ул. Ленина 1", "пр. Мира 2", "ул. Гагарина 3"]
    
    data = {
        "firstName": random.choice(first_names),
        "lastName": random.choice(last_names),
        "address": random.choice(addresses),
        "metroStation": random.randint(1, 20),
        "phone": f"+7{random.randint(9000000000, 9999999999)}",
        "rentTime": random.randint(1, 7),
        "deliveryDate": "2026-07-01",
        "comment": "Тестовый заказ"
    }
    
    if color:
        data["color"] = color if isinstance(color, list) else [color]
    
    return data