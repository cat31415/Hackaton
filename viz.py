import matplotlib.pyplot as plt
import pandas as pd
from game_map import GameMap

# Функция для отображения карты
def plot_game_map(game_map: GameMap, visibility_radius: int = 10):
    fig, ax = plt.subplots()

    # Устанавливаем пределы отображения на основе координат наших баз
    player_base_coords = game_map.player_bases[['x', 'y']]
    if not player_base_coords.empty:
        x_min = player_base_coords['x'].min() - visibility_radius
        x_max = player_base_coords['x'].max() + visibility_radius
        y_min = player_base_coords['y'].min() - visibility_radius
        y_max = player_base_coords['y'].max() + visibility_radius
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

    # Отображаем статические блоки
    for _, block in game_map.static_blocks.iterrows():
        if block['type'] == 'wall':
            ax.plot(block['x'], block['y'], 's', color='black', label='Wall' if 'Wall' not in ax.get_legend_handles_labels()[1] else "")

    # Отображаем мои базы
    for _, base in game_map.player_bases.iterrows():
        color = 'blue' if base['isHead'] else 'cyan'
        ax.plot(base['x'], base['y'], 'o', color=color, label='Player Base (Head)' if base['isHead'] and 'Player Base (Head)' not in ax.get_legend_handles_labels()[1] else 'Player Base' if not base['isHead'] and 'Player Base' not in ax.get_legend_handles_labels()[1] else "")

    # Отображаем базы противника
    for _, base in game_map.enemy_bases.iterrows():
        color = 'red' if base['isHead'] else 'magenta'
        ax.plot(base['x'], base['y'], 'o', color=color, label='Enemy Base (Head)' if base['isHead'] and 'Enemy Base (Head)' not in ax.get_legend_handles_labels()[1] else 'Enemy Base' if not base['isHead'] and 'Enemy Base' not in ax.get_legend_handles_labels()[1] else "")

    # Отображаем зомби
    for _, zombie in game_map.zombies.iterrows():
        if zombie['type'] == 'normal':
            color = 'green'
        elif zombie['type'] == 'juggernaut':
            color = 'yellow'
        else:
            color = 'gray'
        ax.plot(zombie['x'], zombie['y'], 'x', color=color, label=zombie['type'].capitalize() + ' Zombie' if zombie['type'].capitalize() + ' Zombie' not in ax.get_legend_handles_labels()[1] else "")

    # Устанавливаем легенду
    ax.legend(bbox_to_anchor=( 1.05 , 1 ), loc='upper left', borderaxespad= 0 )

    # Устанавливаем сетку
    ax.set_xticks(range(int(x_min), int(x_max) + 1))
    ax.set_yticks(range(int(y_min), int(y_max) + 1))
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box')

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Game Map')
    plt.show()