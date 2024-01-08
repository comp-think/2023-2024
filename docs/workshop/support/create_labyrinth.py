from random import shuffle, choice
import networkx as nx
from collections import defaultdict
from argparse import ArgumentParser
from os import makedirs
from os.path import exists, sep
from json import dump
from numpy import multiply
from scipy.spatial import distance


def get_number_of_cells(total, p_room, p_walls):
    n_room = round((total / 100) * p_room)
    n_walls = round((total / 100) * p_walls)

    diff = total - (n_room + n_walls)
    while diff != 0:
        if diff > 0:
            val = 1
            diff -= 1
        else:
            val = -1
            diff += 1
        n_walls += val
    
    return n_room, n_walls


def get_edge_cells(set_of_cells, edge_size):
    result = defaultdict(list)

    for x, y in set_of_cells:
        if 0 <= x < edge_size - 1 and y == 0:
            result["top"].append((x, y))
        elif x == 0 and 1 <= y < edge_size:
            result["left"].append((x, y))
        elif 0 < x < edge_size and y == edge_size - 1:
            result["bottom"].append((x, y))
        elif x == edge_size - 1 and 0 <= y < edge_size - 1:
            result["right"].append((x, y))
    
    return result


def find_entrance_and_exit(labyrinth_structure, edge_size):
    coordinates = set([room for room in labyrinth_structure])
    list_of_edges = []
    for x, y in coordinates:
        possible_moves = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)
        ]
        for move in possible_moves:
            if move in coordinates:
                list_of_edges.append(((x, y), move))
    
    g = nx.from_edgelist(list_of_edges)
    connected_components = sorted(list(nx.connected_components(g)), 
                                  key=len, reverse=True)

    for component in connected_components:
        if len(component) > ((edge_size * edge_size) / 3):
            edge_cells = get_edge_cells(component, edge_size)
            if len(edge_cells) > 1:
                entrance = None
                exit = None
                for v in edge_cells.values():
                    if entrance is None:
                        entrance = choice(v)
                    else:
                        cur_exit = choice(v)
                        cur_dist = distance.euclidean(entrance, cur_exit)
                        if cur_dist >= edge_size - 1:
                            exit = choice(v)
                
                return entrance, exit

    return None, None


def create_labyrinth(edge_size, p_room, p_wall):
    room, wall = get_number_of_cells(edge_size * edge_size, p_room, p_wall)
    cell_list = room * ["room"] + wall * ["wall"]
    shuffle(cell_list)
    
    structure = []
    for x in range(edge_size):
        for y in range(edge_size):
            cell = cell_list.pop(0)
            if cell == "room":
                structure.append((x, y))
    
    entrance, exit = find_entrance_and_exit(structure, edge_size)
    if entrance is not None and exit is not None:
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                n_exit = (exit[0] + x, exit[1] + y)
                if 0 < n_exit[0] < edge_size and 0 < n_exit[1] < edge_size and n_exit not in structure:
                    structure.append(n_exit)

        return {
            "structure": structure,
            "entrance": entrance,
            "exits" : exit,
            "edge_size": edge_size
        }

if __name__ == "__main__":
    arg_parser = ArgumentParser("Create Labyrinth")

    arg_parser.add_argument("-o", "--outdir", required=True,
                            help="The folder where to store the 100 labyrinths.")
    
    args = arg_parser.parse_args()

    if not exists(args.outdir):
        makedirs(args.outdir)
    
    count_labyrinth = 1
    base_edge = 6
    edge_size = base_edge
    multiplier = 0
    divider = 6

    while count_labyrinth < 101:
        labyrinth = None

        while labyrinth is None:
            p_wall = 0
            while p_wall < 40:
                p_wall = choice(range(101))
                p_room = choice(range(101 - p_wall))

            labyrinth = create_labyrinth(edge_size, p_room, p_wall)
            if labyrinth is not None:
                print(count_labyrinth, 
                    f"- Generated labyrinth {edge_size}x{edge_size} with {p_room}% "
                    f"rooms and {p_wall}% walls")
        
        with open(args.outdir + sep + str(count_labyrinth) + ".json", "w", encoding="utf-8") as f:
            dump(labyrinth, f)
        
        multiplier += 1
        edge_size = base_edge * ((multiplier % divider) + 1)
        count_labyrinth += 1
