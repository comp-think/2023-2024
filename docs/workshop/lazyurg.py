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

# This is a fake (i.e. it fails) implementation of the 'do_move' 
# function, that does always select an invalid couple of coordinates
# as next move to run. Change the body of the function to provide 
# better instructions to play The Cracked Chess.
from random import choice


def do_move_wall(labyrinth, length, explorer_position, exit, notebook):
    walls = list()
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
    
    ok_rooms = list(set(labyrinth).difference(not_allowed))
    
    ok_wall = choice(walls)
    ok_room = choice(ok_rooms)
    
    labyrinth.remove(ok_room)
    labyrinth.append(ok_wall)
    
    # do something here and then return the new labyrinth updated
    return labyrinth, notebook