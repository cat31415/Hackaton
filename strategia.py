import time
from api_client import get_static_blocks, get_dynamic_blocks, register_for_round, send_action_commands
from game_map import GameMap
import math

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

def predict_next_position_chaos_knight(zombie):
    direction = zombie['direction']
    x, y = zombie['x'], zombie['y']
    
    if direction == 'up':
        return [(x + 1, y - 2), (x - 1, y - 2)]
    elif direction == 'down':
        return [(x + 1, y + 2), (x - 1, y + 2)]
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

def is_direct_threat(zombie, base):
    next_x, next_y = predict_next_position(zombie)
    return next_x == base['x'] and next_y == base['y']

def analyze_threats(game_map):
    all_bases = game_map.player_bases
    nearby_zombies = game_map.get_all_blocks()[game_map.get_all_blocks()['type'] == 'zombie']
    
    threats = []
    for _, base in all_bases.iterrows():
        for _, zombie in nearby_zombies.iterrows():
            next_positions = []
            if zombie['type'] == 'fast':
                next_positions.append(predict_next_position_fast(zombie))
            elif zombie['type'] == 'chaos_knight':
                next_positions.extend(predict_next_position_chaos_knight(zombie))
            else:
                next_positions.append(predict_next_position(zombie))
            
            for next_x, next_y in next_positions:
                if is_within_attack_range(base, next_x, next_y):
                    threats.append((base, zombie, next_x, next_y))
    
    return threats

def will_attack_base(zombie, base):
    if zombie['waitTurns'] > 1:
        return False  # Зомби не сможет атаковать на следующем ходу
    if zombie['x'] == base['x'] and zombie['y'] == base['y']:
        return True  # Зомби уже на базе, будет атаковать
    if zombie['type'] == 'bomber':
        if abs(zombie['x'] - base['x']) <= 1 and abs(zombie['y'] - base['y']) <= 1:
            return True  # Зомби типа "bomber" атакует все клетки в радиусе 1
    if zombie['type'] == 'liner':
        if abs(zombie['x'] - base['x']) <= 1 and abs(zombie['y'] - base['y']) <= 1:
            return True  # Зомби типа "liner" атакует все клетки рядом с базой
    return False

def prioritize_threats(threats, game_map):
    def threat_level(zombie, game_map):
        all_bases = game_map.player_bases
        for _, base in all_bases.iterrows():
            if will_attack_base(zombie, base):
                return 5 
            if zombie['type'] in ['juggernaut', 'bomber']:
                return 4
            elif zombie['type'] in ['liner', 'chaos_knight']:
                return 3
            elif zombie['type'] in ['normal', 'fast']:
                return 2
            return 1

    return sorted(threats, key=lambda x: (threat_level(x[1], game_map), -x[1]['health'], -math.sqrt((x[0]['x'] - x[2]) ** 2 + (x[0]['y'] - x[3]) ** 2)), reverse=True)

def decide_actions(game_map):
    threats = analyze_threats(game_map)
    attack_commands = []

    prioritized_threats = prioritize_threats(threats, game_map)

    for base, zombie, next_x, next_y in prioritized_threats:
        if base['isHead']:
            attack_commands.append({
                "id": base['id'],
                "x": next_x,
                "y": next_y
            })

    for base, zombie, next_x, next_y in prioritized_threats:
        if not base['isHead']:
            if is_within_attack_range(base, next_x, next_y):
                if zombie['health'] <= base['attack']:
                    attack_commands.append({
                        "x": next_x,
                        "y": next_y
                    })
                elif zombie['health'] > base['attack'] and is_within_attack_range(game_map.player_bases[game_map.player_bases['isHead']].iloc[0], next_x, next_y):
                    attack_commands.append({
                        "x": next_x,
                        "y": next_y
                    })

    return attack_commands


