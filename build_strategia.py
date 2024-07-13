# build_strategia.py
from game_map import GameMap
from typing import Tuple, Set
import pandas as pd

def find_connected_blocks(game_map: GameMap) -> Set[Tuple[int, int]]:
    """Find all blocks connected to the main block."""
    main_block = game_map.player_bases[game_map.player_bases['isHead'] == True].iloc[0]
    connected_blocks = set([(main_block['x'], main_block['y'])])
    to_visit = [(main_block['x'], main_block['y'])]

    while to_visit:
        x, y = to_visit.pop()
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        for nx, ny in neighbors:
            if (nx, ny) in connected_blocks:
                continue
            block = game_map.get_blocks_by_coordinates(nx, ny)
            if not block.empty and block.iloc[0]['type'] == 'player_base':
                connected_blocks.add((nx, ny))
                to_visit.append((nx, ny))

    return connected_blocks

def find_restricted_positions(game_map: GameMap) -> Set[Tuple[int, int]]:
    """Find all positions where building is not allowed."""
    restricted_positions = set()

    # Add enemy bases and their surrounding area (no diagonal placement allowed)
    for _, enemy_base in game_map.enemy_bases.iterrows():
        sx, sy = enemy_base['x'], enemy_base['y']
        restricted_positions.update([(sx, sy), (sx-1, sy), (sx+1, sy), (sx, sy-1), (sx, sy+1),
                                     (sx-1, sy-1), (sx+1, sy-1), (sx-1, sy+1), (sx+1, sy+1)])
    
    # Add walls and zombie spawn points and their surrounding area (diagonal placement allowed)
    for _, static_block in game_map.static_blocks.iterrows():
        ex, ey = static_block['x'], static_block['y']
        restricted_positions.update([(ex, ey), (ex-1, ey), (ex+1, ey), (ex, ey-1), (ex, ey+1)])
    
    # Add positions with zombies
    for _, zombie in game_map.zombies.iterrows():
        zx, zy = zombie['x'], zombie['y']
        restricted_positions.add((zx, zy))


def find_build_positions(game_map: GameMap, connected_bases: pd.DataFrame) -> Set[Tuple[int, int]]:
    """Find all valid positions around the connected bases for building new blocks."""
    build_positions = set()
    connected_coords = set(connected_bases[['x', 'y']].apply(tuple, axis=1))
    restricted_positions = find_restricted_positions(game_map)

    for x, y in connected_coords:
        potential_positions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        for px, py in potential_positions:
            if (px, py) not in restricted_positions and game_map.get_blocks_by_coordinates(px, py).empty:
                build_positions.add((px, py))

    return build_positions


def build_request(game_map: GameMap, player_gold: int) -> list:
    """Generate build commands based on valid positions and available gold."""
    commands = []

    # Find all connected bases
    connected_bases = find_connected_bases(game_map)
    # Find valid build positions around the connected bases
    build_positions = find_build_positions(game_map, connected_bases)

    # Generate build commands
    for px, py in build_positions:
        if player_gold > 0:
            commands.append({"x": px, "y": py})
            player_gold -= 1
        else:
            break

    return commands
