import requests
import time

BASE_URL = "https://games-test.datsteam.dev/"
AUTH_TOKEN = "your_auth_token_here"
HEADERS = {
    "X-Auth-Token": AUTH_TOKEN,
    "Content-Type": "application/json"
}

def register_for_round():
    url = f"{BASE_URL}/play/zombidef/participate"
    response = requests.put(url, headers=HEADERS)
    if response.status_code == 200:
        print("Successfully registered for the round.")
    else:
        print(f"Failed to register: {response.status_code} - {response.text}")

def send_commands(build_commands, attack_commands):
    url = f"{BASE_URL}/play/zombidef/command"
    payload = {
        "build": build_commands,
        "attack": attack_commands
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        print("Commands successfully sent.")
    else:
        print(f"Failed to send commands: {response.status_code} - {response.text}")

def build_base(x, y):
    # Пример команды строительства базы на координатах (x, y)
    build_commands = [{"x": x, "y": y}]
    send_commands(build_commands, [])

def attack_zombie(x, y):
    # Пример команды атаки зомби на координатах (x, y)
    attack_commands = [{"x": x, "y": y}]
    send_commands([], attack_commands)

if __name__ == "__main__":
    register_for_round()
    time.sleep(5)  # Ожидание перед началом основного этапа раунда
    
    # Основной игровой цикл
    while True:
        # Пример автоматизированных действий
        build_base(1, 1)
        attack_zombie(2, 2)
        
        # Ожидание завершения хода (примерное время хода 2 секунды)
        time.sleep(2)
