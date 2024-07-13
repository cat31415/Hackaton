def find_connected_blocks(game_map: GameMap):
    """Find all blocks connected to the main block."""
    main_block = game_map.player_bases[game_map.player_bases['isHead'] == True].iloc[0]
    connected_blocks = set([(main_block['x'], main_block['y'])])
    to_visit = [(main_block['x'], main_block['y'])]

    while to_visit:
        x, y = to_visit.pop()
        neighbors = [
            (x-1, y), (x+1, y), 
            (x, y-1), (x, y+1)
        ]
        for nx, ny in neighbors:
            if (nx, ny) in connected_blocks:
                continue
            block = game_map.get_blocks_by_coordinates(nx, ny)
            if not block.empty and block.iloc[0]['type'] == 'player_base':
                connected_blocks.add((nx, ny))
                to_visit.append((nx, ny))

    return connected_blocks

def find_new_block_position(game_map: GameMap, connected_blocks):
    """Find a valid new block position connected to the existing base."""
    for x, y in connected_blocks:
        potential_positions = [
            (x-1, y), (x+1, y), 
            (x, y-1), (x, y+1)
        ]
        for px, py in potential_positions:
            if game_map.get_blocks_by_coordinates(px, py).empty:
                if game_map.get_nearby_blocks(px, py, 1).empty:
                    return px, py
    return None, None

def build_strategy(game_map: GameMap, player_gold: int):
    commands = {"attack": [], "build": [], "moveBase": None}

    connected_blocks = find_connected_blocks(game_map)
    disconnected_blocks = set(game_map.player_bases[['x', 'y']].apply(tuple, axis=1)) - connected_blocks

    # Восстановление связи
    for x, y in disconnected_blocks:
        new_x, new_y = find_new_block_position(game_map, connected_blocks)
        if new_x is not None and player_gold > 0:
            commands['build'].append({"x": new_x, "y": new_y})
            connected_blocks.add((new_x, new_y))
            player_gold -= 1

    # Построение новых блоков, если все блоки связаны
    if not disconnected_blocks:
        for _ in range(player_gold):
            new_x, new_y = find_new_block_position(game_map, connected_blocks)
            if new_x is not None:
                commands['build'].append({"x": new_x, "y": new_y})
                connected_blocks.add((new_x, new_y))
            else:
                break

    return commands
