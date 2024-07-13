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
    all_blocks = game_map.all_blocks
    
    nearby_zombies = all_blocks[(all_blocks['type'] == 'zombie') | (all_blocks['type'] == 'enemy_base')]
    
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

def prioritize_threats(threats, game_map):
    def threat_level(threat, game_map):
        base, zombie, x, y = threat
        all_bases = game_map.player_bases
        enemy_bases = game_map.all_blocks[game_map.all_blocks['type'] == 'enemy_base']
        main_enemy_base = enemy_bases[enemy_bases['isHead']]
        # Прямые угрозы
        if is_direct_threat(zombie, base):
            return 6

        # Главная база противника
        for _, enemy_base in main_enemy_base.iterrows():
            if is_within_attack_range(base, enemy_base['x'], enemy_base['y']):
                return 5

        # Второстепенные базы противника
        for _, enemy_base in enemy_bases.iterrows():
            if is_within_attack_range(base, enemy_base['x'], enemy_base['y']):
                return 4

        # Опасные зомби (liner)
        if zombie['type'] == 'liner':
            return 3

        # Зомби (bomber, juggernaut)
        if zombie['type'] in ['bomber', 'juggernaut']:
            return 2

        # Все остальные зомби
        return 1
    return sorted(threats, key=lambda x: (threat_level(x, game_map), -math.sqrt((x[0]['x'] - x[2]) ** 2 + (x[0]['y'] - x[3]) ** 2) , -x[1]['health']), reverse=True)

def decide_actions(game_map, next = True):
    threats = analyze_threats(game_map)
    attack_commands = []
    bases_attacked = set()

    prioritized_threats = prioritize_threats(threats, game_map)
    zombie_health = {}
    all_blocks = game_map.all_blocks
    for _, zombie in all_blocks[(all_blocks['type'] == 'zombie') | (all_blocks['type'] == 'enemy_base')].iterrows():
        
        zombie_health[zombie['id']] = zombie['health']

    for base, zombie, next_x, next_y in prioritized_threats:
        if base['id'] not in bases_attacked:
            current_health = zombie_health.get(zombie['id'], 0)
            if current_health > 0:
                attack_commands.append({
                    "blockId": base['id'],
                    "target":{
                    "x": zombie['x'] if next else next_x,  # Атакуем текущую позицию зомби
                    "y": zombie['y'] if next else next_y}  # Атакуем текущую позицию зомби
                })
                current_health -= base['attack']
                if current_health <= 0:
                    del zombie_health[zombie['id']]
                else:
                    zombie_health[zombie['id']] = current_health
                bases_attacked.add(base['id'])

    return attack_commands

