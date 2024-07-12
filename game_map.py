import pandas as pd

class Block:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class StaticBlock(Block):
    def __init__(self, x: int, y: int, type: str):
        super().__init__(x, y)
        self.type = type  # "wall" или "default"

class Base(Block):
    def __init__(self, id: int, x: int, y: int, health: int, attack: int, range: int, isHead: bool = 0):
        super().__init__(x, y)
        self.id = id
        self.health = health
        self.attack = attack
        self.range = range
        self.isHead = isHead

class PlayerBase(Base):
    def __init__(self, id: int, x: int, y: int, health: int, attack: int, range: int, isHead: bool):
        super().__init__(id, x, y, health, attack, range, isHead)

class EnemyBase(Base):
    def __init__(self, x: int, y: int, health: int, attack: int, range: int, isHead: bool):
        super().__init__(0, x, y, health, attack, range, isHead)

class Zombie(Block):
    def __init__(self, id: int, x: int, y: int, health: int, attack: int, type: str, speed: int, waitTurns: int, direction: str):
        super().__init__(x, y)
        self.id = id
        self.health = health
        self.attack = attack
        self.type = type
        self.speed = speed
        self.waitTurns = waitTurns
        self.direction = direction 

class GameMap:
    def __init__(self):
        self.static_blocks = pd.DataFrame(columns=['x', 'y', 'type'])
        self.player_bases = pd.DataFrame(columns=['id', 'x', 'y', 'health', 'attack', 'range', 'isHead'])
        self.enemy_bases = pd.DataFrame(columns=['id', 'x', 'y', 'health', 'attack', 'range', 'isHead'])
        self.zombies = pd.DataFrame(columns=['id', 'x', 'y', 'health', 'attack', 'type', 'speed', 'waitTurns', 'direction'])

    def add_static_block(self, x: int, y: int, type: str):
        self.static_blocks = self.static_blocks.append({'x': x, 'y': y, 'type': type}, ignore_index=True)

    def add_player_base(self, id: int, x: int, y: int, health: int, attack: int, range: int, isHead: bool):
        self.player_bases = self.player_bases.append({'id': id, 'x': x, 'y': y, 'health': health, 'attack': attack, 'range': range, 'isHead': isHead}, ignore_index=True)

    def add_enemy_base(self, id: int, x: int, y: int, health: int, attack: int, range: int, isHead: bool):
        self.enemy_bases = self.enemy_bases.append({'id': id, 'x': x, 'y': y, 'health': health, 'attack': attack, 'range': range, 'isHead': isHead}, ignore_index=True)

    def add_zombie(self, id: int, x: int, y: int, health: int, attack: int, type: str, speed: int, waitTurns: int, direction: str):
        self.zombies = self.zombies.append({'id': id, 'x': x, 'y': y, 'health': health, 'attack': attack, 'type': type, 'speed': speed, 'waitTurns': waitTurns, 'direction': direction}, ignore_index=True)

    def get_all_blocks(self) -> pd.DataFrame:
        all_blocks = pd.concat([
            self.static_blocks.assign(type='static'),
            self.player_bases.assign(type='player_base'),
            self.enemy_bases.assign(type='enemy_base'),
            self.zombies.assign(type='zombie')
        ], ignore_index=True)
        return all_blocks

    def get_blocks_by_coordinates(self, x: int, y: int) -> pd.DataFrame:
        all_blocks = self.get_all_blocks()
        return all_blocks[(all_blocks['x'] == x) & (all_blocks['y'] == y)]

    def get_nearby_blocks(self, x: int, y: int, radius: int) -> pd.DataFrame:
        all_blocks = self.get_all_blocks()
        return all_blocks[((all_blocks['x'] - x) ** 2 + (all_blocks['y'] - y) ** 2) ** 0.5 <= radius]

    def load_static_blocks(self, json_data):
        for block in json_data['zpots']:
            self.add_static_block(block['x'], block['y'], block['type'])

    def load_dynamic_blocks(self, json_data):
        if json_data['base']:
            for block in json_data['base']:
                self.add_player_base(block['id'], block['x'], block['y'], block['health'], block['attack'], block['range'], block['isHead']if 'isHead' in block else False)
        if json_data['enemyBlocks']:
            for block in json_data['enemyBlocks']:
                self.add_enemy_base(0, block['x'], block['y'], block['health'], block['attack'], 8 if 'isHead' in block else 5, block['isHead']if 'isHead' in block else False)
        if json_data['zombies']: 
            for block in json_data['zombies']:
                self.add_zombie(block['id'], block['x'], block['y'], block['health'], block['attack'], block['type'], block['speed'], block['waitTurns'], block['direction'])
