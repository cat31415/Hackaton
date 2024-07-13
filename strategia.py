import time
from api_client import get_static_blocks, get_dynamic_blocks, register_for_round, send_action_commands
from game_map import GameMap
import math

# Функция для предсказания следующей позиции зомби
def predict_next_position(zombie):
    direction = zombie['direction']
    x, y = zombie['x'], zombie['y']
    
    if direction == 'up':
        y -= 1
    elif direction == 'down':
        y += 1
    elif direction == 'left':
        x -= 1
    elif direction == 'right':
        x += 1

    return x, y

# Функция для предсказания следующей позиции fast зомби
def predict_next_position_fast(zombie):
    direction = zombie['direction']
    x, y = zombie['x'], zombie['y']
    
    if direction == 'up':
        y -= 2
    elif direction == 'down':
        y += 2
    elif direction == 'left':
        x -= 2
    elif direction == 'right':
        x += 2

    return x, y

# Функция для предсказания следующих позиций chaos_knight зомби
def predict_next_position_chaos_knight(zombie):
    direction = zombie['direction']
    x, y = zombie['x'], zombie['y']
    
    if direction == 'up':
        return [(x + 1, y + 2), (x - 1, y + 2)]
    elif direction == 'down':
        return [(x + 1, y - 2), (x - 1, y - 2)]
    elif direction == 'right':
        return [(x + 2, y + 1), (x + 2, y - 1)]
    elif direction == 'left':
        return [(x - 2, y + 1), (x - 2, y - 1)]
    return []

def is_within_attack_range(base, target_x, target_y):
    range_x = abs(base['x'] - target_x)
    range_y = abs(base['y'] - target_y)
    distance = math.sqrt(range_x ** 2 + range_y ** 2)
    return distance <= base['range']

def analyze_threats(game_map):
    all_bases = game_map.player_bases
    nearby_zombies = game_map.get_all_blocks()[game_map.get_all_blocks()['type'] == 'zombie']
    
    threats = []
    for _, base in all_bases.iterrows():
        for _, zombie in nearby_zombies.iterrows():
            next_positions = []
            if zombie['zombie_type'] == 'fast':
                next_positions.append(predict_next_position_fast(zombie))
            elif zombie['zombie_type'] == 'chaos_knight':
                next_positions.extend(predict_next_position_chaos_knight(zombie))
            else:
                next_positions.append(predict_next_position(zombie))
            
            for next_x, next_y in next_positions:
                if is_within_attack_range(base, next_x, next_y):
                    threats.append((base, zombie, next_x, next_y))
    
    return threats

def prioritize_threats(threats):
    def threat_level(zombie):
        if zombie['zombie_type'] in ['juggernaut', 'bomber']:
            return 3
        elif zombie['zombie_type'] in ['liner', 'chaos_knight']:
            return 2
        elif zombie['zombie_type'] in ['normal', 'fast']:
            return 1
        return 0

    return sorted(threats, key=lambda x: (threat_level(x[1]), -x[1]['health'], -math.sqrt((x[0]['x'] - x[2]) ** 2 + (x[0]['y'] - x[3]) ** 2)), reverse=True)

def decide_actions(game_map, threats):
    attack_commands = []

    prioritized_threats = prioritize_threats(threats)

    for base, zombie, next_x, next_y in prioritized_threats:
        if base['is_main']:
            attack_commands.append({
                "id": zombie['id'],
                "x": next_x,
                "y": next_y
            })

    for base, zombie, next_x, next_y in prioritized_threats:
        if not base['is_main']:
            if is_within_attack_range(base, next_x, next_y):
                if zombie['health'] <= base['strength']:
                    attack_commands.append({
                        "id": zombie['id'],
                        "x": next_x,
                        "y": next_y
                    })
                elif zombie['health'] > base['strength'] and is_within_attack_range(game_map.player_bases[game_map.player_bases['is_main']].iloc[0], next_x, next_y):
                    attack_commands.append({
                        "id": zombie['id'],
                        "x": next_x,
                        "y": next_y
                    })

    return attack_commands

def main():
    register_for_round()
    game_map = GameMap()

    while True:
        static_blocks = get_static_blocks()
        game_map.load_static_blocks(static_blocks)

        dynamic_blocks = get_dynamic_blocks()
        game_map.load_dynamic_blocks(dynamic_blocks)

        threats = analyze_threats(game_map)
        attack_commands = decide_actions(game_map, threats)

        send_action_commands(attack_commands, [], [])

        time.sleep(2)

if __name__ == "__main__":
    main()
