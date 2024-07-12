from game_map import GameMap
from api_client import *
from viz import *


if __name__ == "__main__":
    game_map = GameMap()

    static_blocks = read_json_file_Stat()
    dynamic_blocks = read_json_file_Not_Stat()

    game_map.load_static_blocks(static_blocks)
    game_map.load_dynamic_blocks(dynamic_blocks)

    plot_game_map(game_map)
