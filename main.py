import time
from api_client import *
from game_map import GameMap
from build_strategia import build_request
from strategia import decide_actions
from viz import *
def main():
    # Initialize game map
    game_map = GameMap()

    # Register for the round (commented out for testing)
    time_to_start = register_for_round()
    if(time_to_start != -1):
        print(time_to_start)
        time.sleep(time_to_start)
        while True:
            # Get static and dynamic blocks from the local JSON files for testing
            static_blocks = get_static_blocks()
            dynamic_blocks = get_dynamic_blocks()

            # Update the game map with the current state
            game_map.load_static_blocks(static_blocks)
            game_map.load_dynamic_blocks(dynamic_blocks)
            
            # Get player gold from the updated game map
            player_gold = game_map.player.gold if game_map.player else 0

            # Create build commands
            build_commands = build_request(game_map, player_gold)
            attack_commands = decide_actions(game_map)
            move_base_command = None  # Adjust if needed

            commands = {
                'attack': attack_commands,
                'build': build_commands,
                'moveBase': move_base_command
            }

            # Send build commands to the server (commented out for testing)
            send_action_commands(commands['attack'], commands['build'], commands['moveBase'])
            plot_game_map(game_map)
            # Wait for the next turn (commented out for testing)
            time.sleep(2)  # Assuming each turn takes 2 seconds; adjust as needed

if __name__ == "__main__":
    main()
