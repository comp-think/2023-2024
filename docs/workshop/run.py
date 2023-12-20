# -*- coding: utf-8 -*-
# Copyright (c) 2023, Silvio Peroni <essepuntato@gmail.com>
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

from explorer import do_move
from group import do_move_wall

board = {
    "structure": [
        (0,0),            (3,0),(4,0),            (7,0),
              (1,1),(2,1),      (4,1),      (6,1),(7,1),
              (1,2),                  (5,2),(6,2),(7,2),
                    (2,3),(3,3),(4,3),(5,3),(6,3),(7,3),
        (0,4),(1,4),(2,4),(3,4),            (6,4),(7,4),
        (0,5),      (2,5),
        (0,6),(1,6),(2,6),      (4,6),(5,6),(6,6),
        (0,7),(1,7),            (4,7)], 
    "entrance": (0,5), 
    "exits": (7,3),
    "edge_size": 8
}

start = board["entrance"]
exit = board["exits"]
edge_size = board["edge_size"]
max_moves = int(edge_size * 2)

current_position = start
my_notebook = {}
labyrinth = board["structure"]

while current_position != exit and max_moves > 0:
    # The explorer moves
    current_position = do_move(labyrinth, edge_size, current_position, exit)

    # Urg swap a wall with a room
    labyrinth, my_notebook = do_move_wall(
        labyrinth, edge_size, current_position, exit, my_notebook)

    # Decrement the number of available moves    
    max_moves -= 1

if current_position == exit:
    print("The explorer found the exit!")
else:
    print("The explorer died.")