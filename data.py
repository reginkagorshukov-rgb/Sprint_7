import random

ERROR_MESSAGES = {
    'missing_fields': 'Недостаточно данных для создания учетной записи',
    'login_already_exists': 'Этот логин уже используется.',
    'auth_failed': 'Учетная запись не найдена',
    'missing_login_or_password': 'Недостаточно данных для входа'
}

CORRECT_LOGIN = "Test"
CORRECT_PASSWORD = "1234"

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