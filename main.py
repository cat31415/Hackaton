import requests
import json

# Установите ваш токен аутентификации
AUTH_TOKEN = '6690ca5ad88f26690ca5ad88f6'
BASE_URL = 'https://games-test.datsteam.dev/'

# Заголовки для аутентификации
headers = {
    'Content-Type': 'application/json',
    'X-Auth-Token': AUTH_TOKEN
}

# Функция для регистрации на раунд
def register_for_round():
    url = f'{BASE_URL}/play/zombidef/participate'
    response = requests.put(url, headers=headers)
    if response.status_code == 200:
        print("Successfully registered for the round.")
    else:
        print(f"Failed to register: {response.status_code} {response.text}")

# Функция для отправки команд на строительство и атаку
def send_commands(build_commands, attack_commands):
    url = f'{BASE_URL}/play/zombidef/command'
    commands = {
        "build": build_commands,
        "attack": attack_commands
    }
    response = requests.post(url, headers=headers, data=json.dumps(commands))
    if response.status_code == 200:
        print("Commands sent successfully.")
    else:
        print(f"Failed to send commands: {response.status_code} {response.text}")

# Пример команд на строительство и атаку
build_commands = [
    {"x": 5, "y": 5},
    {"x": 5, "y": 6}
]

attack_commands = [
    {"x": 10, "y": 10},
    {"x": 11, "y": 10}
]

# Регистрация на раунд
register_for_round()

# Отправка команд
#send_commands(build_commands, attack_commands)
