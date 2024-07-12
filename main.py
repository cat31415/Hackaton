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
    }
    response = requests.post(url, headers=headers, data=json.dumps(commands))
    print(f"Request URL: {url}")
    print(f"Request Headers: {headers}")
    print(f"Request Data: {json.dumps(commands)}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    if response.status_code == 200:
        print("Commands sent successfully.")
    else:
        print(f"Failed to send commands: {response.status_code} {response.text}")


def get_map_info():
    url = f'{BASE_URL}/play/zombidef/world'
    response = requests.get(url, headers=headers)
    print(f"Request URL: {url}")
    print(f"Request Headers: {headers}")
    print(f"Response Status Code: {response.status_code}")
    if response.status_code == 200:
        base_info = response.json()
        print("Base information retrieved successfully.")
        print(json.dumps(base_info, indent=4))
    else:
        print(f"Failed to retrieve base information: {response.status_code} {response.text}")

def get_units_info():
    url = f'{BASE_URL}/play/zombidef/units'
    response = requests.get(url, headers=headers)
    print(f"Request URL: {url}")
    print(f"Request Headers: {headers}")
    print(f"Response Status Code: {response.status_code}")
    if response.status_code == 200:
        base_info = response.json()
        print("Base information retrieved successfully.")
        print(json.dumps(base_info, indent=4))
    else:
        print(f"Failed to retrieve base information: {response.status_code} {response.text}")


# Пример команд на строительство и атаку
build_commands = [
    {"x": 1, "y": 1}
]

attack_commands = [
    {"x": 10, "y": 10}
]

# Регистрация на раунд
#register_for_round()

# Отправка команд
get_map_info()
get_units_info()