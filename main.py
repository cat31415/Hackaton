import time
from api_client import get_static_blocks, get_dynamic_blocks, register_for_round, send_action_commands
from game_map import GameMap
from build_strategia import build_request

def main():
    # Initialize game map
    game_map = GameMap()

    # Register for the round
    register_for_round()

    while True:
        # Get static and dynamic blocks from the server
        static_blocks = get_static_blocks()
        dynamic_blocks = get_dynamic_blocks()

        # Update the game map with the current state
        game_map.load_static_blocks(static_blocks)
        game_map.load_dynamic_blocks(dynamic_blocks)

        # Get player gold from the updated game map
        player_gold = game_map.player.gold

        # Create build commands
        commands = build_request(game_map, player_gold)

        # Send build commands to the server
        send_action_commands(commands['attack'], commands['build'], commands['moveBase'])

        # Wait for the next turn
        time.sleep(2)  # Assuming each turn takes 2 seconds; adjust as needed

if __name__ == "__main__":
    main()
