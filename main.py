import requests
import json
import os
def read_json_file():
    file_name = "exampleMap.json"
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, file_name)
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data
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


# Функция для выполнения действий: атака, строительство, перемещение базы
def send_action_commands(attack_commands, build_commands, move_base_command):
    url = f'{BASE_URL}/play/zombidef/command'
    commands = {
        "attack": attack_commands,
        "build": build_commands,
        "moveBase": move_base_command
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
        return base_info
    else:
        print(f"Failed to retrieve base information: {response.status_code} {response.text}")
        return 0

def get_units_info():
    url = f'{BASE_URL}/play/zombidef/units'
    response = requests.get(url, headers=headers)
    print(f"Request URL: {url}")
    print(f"Request Headers: {headers}")
    print(f"Response Status Code: {response.status_code}")
    if response.status_code == 200:
        base_info = response.json()
        print("Units retrieved successfully.")
        print(json.dumps(base_info, indent=4))
        return base_info
    else:
        print(f"Failed to retrieve units information: {response.status_code} {response.text}")

def work_with_base(map_info):
    bases = {}

    # Сохранение информации о базах в словарь
    if map_info and 'base' in map_info:
        for zpot in map_info['base']:
            base_id = zpot.get('id')  # Предполагается, что у каждой базы есть уникальный идентификатор 'id'
            bases[base_id] = {
                'x': zpot['x'],
                'y': zpot['y'],
            }
    print("\n" + bases)

# Регистрация на раунд
#register_for_round()

# Отправка команд
#send_action_commands(attack_commands, build_commands, move_base_command)

#register_for_round()
get_map_info()
map_info = get_units_info()
work_with_base(map_info)
#get_units_info()
#send_action_commands(attack_commands, build_commands, move_base_command)