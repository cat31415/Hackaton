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

def get_static_blocks() -> dict:
    url = f"{BASE_URL}/play/zombidef/world"
    return api_get_request(url)

def get_dynamic_blocks() -> dict:
    url = f"{BASE_URL}/play/zombidef/units"
    return api_get_request(url)

def api_get_request(url: str) -> dict:
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"API request error: {e}")
        return {}


def register_for_round():
    url = f'{BASE_URL}/play/zombidef/participate'
    response = requests.put(url, headers=HEADERS)
    if response.status_code == 200:
        print("Successfully registered for the round.")
        return response.json()
    else:
        print(f"Failed to register: {response.status_code} {response.text}")
        return -1

def send_action_commands(attack_commands: list, build_commands: list, move_base_command: dict):
    url = f'{BASE_URL}/play/zombidef/command'
    commands = {
        "attack": attack_commands,
        "build": build_commands,
        "moveBase": move_base_command
    }
    api_post_request(url, commands)

def api_put_request(url: str):
    try:
        response = requests.put(url, headers=HEADERS)
        response.raise_for_status()
        print("Successfully registered for the round.")
    except requests.RequestException as e:
        print(f"Failed to register: {e}")

def api_post_request(url: str, data: dict):
    try:
        response = requests.post(url, headers=HEADERS, json=data)
        response.raise_for_status()
        print("Commands sent successfully.")
    except requests.RequestException as e:
        print(f"Failed to send commands: {e}")