import requests
from config import BASE_URL, HEADERS
import json
import os

def read_json_file_Stat():
    file_name = "StaticBlocks.json"
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, file_name)
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def read_json_file_Not_Stat():
    file_name = "NotStaticBlocks.json"
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, file_name)
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def get_static_blocks():
    url = f"{BASE_URL}/play/zombidef/world"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get static blocks: {response.status_code} - {response.text}")
        return []

def get_dynamic_blocks():
    url = f"{BASE_URL}/play/zombidef/units"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get dynamic blocks: {response.status_code} - {response.text}")
        return {}

# Функция для регистрации на раунд
def register_for_round():
    url = f'{BASE_URL}/play/zombidef/participate'
    response = requests.put(url, headers=HEADERS)
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
    response = requests.post(url, headers=HEADERS, data=json.dumps(commands))
    if response.status_code == 200:
        print("Commands sent successfully.")
    else:
        print(f"Failed to send commands: {response.status_code} {response.text}")