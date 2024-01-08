# -*- coding: utf-8 -*-
# Copyright (c) 2019, Silvio Peroni <essepuntato@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.

import lazyurg
import explorer
from json import load
from collections import OrderedDict
from os.path import exists, sep
from os import remove
from collections import Counter

def load_labyrinth(labyrinth_file_path):
    with open(labyrinth_file_path, encoding="utf-8") as f:
        labyrinth_json = load(f)

        cur_labyrinth = []
        for room in labyrinth_json["structure"]:
            cur_labyrinth.append((room[0], room[1]))
        
        return cur_labyrinth, (labyrinth_json["entrance"][0], labyrinth_json["entrance"][1]),\
               (labyrinth_json["exits"][0], labyrinth_json["exits"][1]),\
               labyrinth_json["edge_size"]

def is_valid_move(old_rooms, old_walls, safe_rooms, labyrinth):
    if len(old_rooms) == len(labyrinth):
        new_wall = list(set(old_rooms).difference(set(labyrinth)))[0]
        new_room = list(set(labyrinth).difference(set(old_rooms)))[0]

        if new_wall in safe_rooms:
            return False
        elif new_room not in old_walls:
            return False
        else:
            return True   
    else:
        return False

def get_walls_and_safe_rooms(labyrinth, explorer_position, exit, length):
    walls = []
    for x in range(length):
        for y in range(length):
            if (x, y) not in labyrinth:
                walls.append((x, y))
    
    not_allowed = {explorer_position}
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            n_exit = (exit[0] + x, exit[1] + y)
            if n_exit in labyrinth:
                not_allowed.add(n_exit)
    
    return set(labyrinth), walls, not_allowed

def play(all_players, all_players_name, labyrinth, entrance, exit, edge_size):
    cur_status = {}
    notebooks = {}
    player_labyrinth = {}
    explorer_won = {}

    for player in all_players:
        player_name = player.__name__
        all_players_name.add(player_name)
        cur_status[player_name] = entrance
        notebooks[player_name] = {}
        player_labyrinth[player_name] = list(labyrinth)
        explorer_won[player_name] = False
    
    cheaters = set()
    winners = set()
    max_moves = int(edge_size * 2)
    max_moves = int(edge_size * 2)
        
    while max_moves > 0:
        for player in all_players:
            player_name = player.__name__
            if not explorer_won[player_name]:  # Explorer has not won so far
                new_explorer_position = \
                    explorer.do_move(
                        player_labyrinth[player_name], edge_size, 
                        cur_status[player_name], exit)
                cur_status[player_name] = new_explorer_position
                
                if new_explorer_position == exit:  # Explorer won
                    explorer_won[player_name] = True
                else:  # Player moves
                    rooms, walls, safe_rooms = get_walls_and_safe_rooms(
                        player_labyrinth[player_name], cur_status[player_name], 
                        exit, edge_size)

                    player_labyrinth[player_name], notebooks[player_name] = \
                        player.do_move_wall(
                            player_labyrinth[player_name], edge_size, 
                            cur_status[player_name], exit, notebooks[player_name])

                    if not is_valid_move(
                        rooms, walls, safe_rooms, player_labyrinth[player_name]):
                        cheaters.add(player_name)
                        explorer_won[player_name] = True
                    
        max_moves -= 1
    
    for player_name in explorer_won:
        if not explorer_won[player_name]:
            winners.add(player_name)

    return winners, cheaters
    

if __name__ == "__main__":
    all_players = [lazyurg]

    final_results = {
        "cheaters": set(),
        "winners": []
    }

    if exists("00_results.txt"):
        remove("00_results.txt")

    all_players_name = set()

    for idx in range(1, 101):
        labyrinth, entrance, exit, edge_size = \
            load_labyrinth("labyrinths" + sep + str(idx) + ".json")
        
        labyrinth_winners, labyrinth_cheaters = play(
            all_players, all_players_name, labyrinth, entrance, exit, edge_size)

        final_results["cheaters"].update(labyrinth_cheaters)
        final_results["winners"].extend(labyrinth_winners)

        final_list = ["\n\n# Room " + str(idx), 
                      "WINNERS:", "\t" + ", ".join([player for player in labyrinth_winners])]
        
        with open("00_results.txt", "a", encoding="utf-8") as f:
            f.write("\n".join(final_list))
    
    final_results_str = \
        "\n\n## FINAL RESULTS ##" + \
        "\nAvoiding non-permitted moves: " +  " ".join(all_players_name.difference(final_results["cheaters"])) + \
        "\nKilling the explorer in at least 30 labyrinths: " + " ".join(Counter({k: v for k, v in Counter(final_results["winners"]).items() if v >= 30}).keys()) + \
        "\nKilling the explorer in at least 70 labyrinths: " + " ".join(Counter({k: v for k, v in Counter(final_results["winners"]).items() if v >= 70})) + \
        "\nBest winner: " + " ".join({k: v for k, v in Counter(final_results["winners"]).items() if v == max(Counter(final_results["winners"]).values())}) + " [with " + str(max(Counter(final_results["winners"]).values())) + " victories]"

    with open("00_results.txt", "a", encoding="utf-8") as f:
        f.write(final_results_str)
    
    print(final_results_str)
