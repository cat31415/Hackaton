from game_map import GameMap
from api_client import get_static_blocks, get_dynamic_blocks

if __name__ == "__main__":
    game_map = GameMap()

    static_blocks = get_static_blocks()
    game_map.load_static_blocks(static_blocks)

    dynamic_blocks = get_dynamic_blocks()
    game_map.load_dynamic_blocks(dynamic_blocks)
