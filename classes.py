from typing import List, Tuple

class Block:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class StaticBlock(Block):
    def __init__(self, x: int, y: int, block_type: str):
        super().__init__(x, y)
        self.block_type = block_type  # "wall" или "zombie_spawn"

class Base(Block):
    def __init__(self, id: int, x: int, y: int, health: int, strength: int, is_main: bool):
        super().__init__(x, y)
        self.id = id
        self.health = health
        self.strength = strength
        self.is_main = is_main

class PlayerBase(Base):
    def __init__(self, id: int, x: int, y: int, health: int, strength: int, is_main: bool):
        super().__init__(id, x, y, health, strength, is_main)

class EnemyBase(Base):
    def __init__(self, id: int, x: int, y: int, health: int, strength: int, is_main: bool):
        super().__init__(id, x, y, health, strength, is_main)

class Zombie(Block):
    def __init__(self, id: int, x: int, y: int, health: int, strength: int, zombie_type: str, direction: str):
        super().__init__(x, y)
        self.id = id
        self.health = health
        self.strength = strength
        self.zombie_type = zombie_type  # например, "walker", "runner"
        self.direction = direction  # например, "north", "south"

import pandas as pd
from typing import List

class GameMap:
    def __init__(self):
        self.static_blocks = pd.DataFrame(columns=['x', 'y', 'block_type'])
        self.player_bases = pd.DataFrame(columns=['id', 'x', 'y', 'health', 'strength', 'is_main'])
        self.enemy_bases = pd.DataFrame(columns=['id', 'x', 'y', 'health', 'strength', 'is_main'])
        self.zombies = pd.DataFrame(columns=['id', 'x', 'y', 'health', 'strength', 'zombie_type', 'direction'])

    def add_static_block(self, x: int, y: int, block_type: str):
        self.static_blocks = self.static_blocks.append({'x': x, 'y': y, 'block_type': block_type}, ignore_index=True)

    def add_player_base(self, id: int, x: int, y: int, health: int, strength: int, is_main: bool):
        self.player_bases = self.player_bases.append({'id': id, 'x': x, 'y': y, 'health': health, 'strength': strength, 'is_main': is_main}, ignore_index=True)

    def add_enemy_base(self, id: int, x: int, y: int, health: int, strength: int, is_main: bool):
        self.enemy_bases = self.enemy_bases.append({'id': id, 'x': x, 'y': y, 'health': health, 'strength': strength, 'is_main': is_main}, ignore_index=True)

    def add_zombie(self, id: int, x: int, y: int, health: int, strength: int, zombie_type: str, direction: str):
        self.zombies = self.zombies.append({'id': id, 'x': x, 'y': y, 'health': health, 'strength': strength, 'zombie_type': zombie_type, 'direction': direction}, ignore_index=True)

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

