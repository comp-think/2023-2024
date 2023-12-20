# Workshop - Computational Thinking and Programming 23/24

## Useful documents

**Slides:** [PDF](https://comp-think.github.io/2023-2024/workshop/workshop2324-slides.pdf)

**Main Python file:** [run.py](https://comp-think.github.io/2023-2024/workshop/run.py)

**Group file:** [group.py](https://comp-think.github.io/2023-2024/workshop/group.py)


## Plot

Myntrakor, also known as Who Must Not Be Thought, was cheated! A mere human explorer was able to survive to the Tower Labyrinth, a complex system made of 100 squared mazes of different dimensions placed one upon the other created to custody one of the most marvellous gems of the (now destroyed) Library of Babel: the Book of Indefinite Pages, containing all the possible books ever written in just one portable volume.

The content of the Book was unbelievable. However, mere humans used it just to take inspiration for the creation of new abstract strategy games – fools who do not recognise the immense power that the Book encloses!

Myntrakor, dressed up as a player of the game Cracked Chess (very popular with the customers of the World End’s Inn), accessed the Inn, found the Book and took it to bring it back within the Tower Labyrinth. However, to avoid others having the chance to steal the Book again, he hired Urg, the best human player of Cracked Chess, a despicable man, after all, as a guarantor of the Tower Labyrinth. Myntrakor asked him to implement a new innovative idea for each maze of the Tower, i.e. a mechanism that allows the walls to move while someone is trying to reach the exit…


## Rules

1. Each labyrinth is a square (of length n per edge) which is initially filled with an arbitrary number of rooms and walls
1. The explorer, in every turn, try to move in a room (vertically or horizontally) to get closer to the exit, initially positioned in the start cell
1. In case, in a turn, the explorer see that there is no path available to reach the exit, he uses the teleport that will bring him in a random room (the exit room could be accidentally selected!)
1. The player (you!) control Urg and, thus, decides, in every turn, which wall should be swapped with which room (it is a mandatory move)
1. The player cannot put a wall in any (vertical, horizontal, diagonal) adjacent room of the exit room and in the room currently occupied by the explorer
The goal of the player is to avoid that the explorer reaches the exit within n * 2 moves


## Function to implement
```
def do_move_wall(labyrinth, length, explorer_position, exit, notebook)
```

It takes in input:
* `labyrinth`, a list of tuples of X/Y coordinates representing the rooms of the labyrinth
* `length`, a number identifying the length of the edge of the labyrinth
* `explorer_position`, a tuple of X/Y coordinates identifying the current position of the explorer
* `exit`, a tuple of X/Y coordinates identifying the exit cell
* `notebook`, a dictionary (empty in the first turn) available for note taking about a particular game

It returns a tuple of two items:
* the first item contains the new configuration of the labyrinth (i.e. the list of cells defining it) after having moved the selected wall
* the second item contains the notebook that can be modified (if needed, it is not mandatory to modify it) with additional information as a consequence of the choice of the move in the first item


Example of a list of tuples with X/Y coordinates representing the labyrinth:
```
[
        (0,0),            (0,3),(0,4),            (0,7),
              (1,1),(1,2),      (1,4),      (1,6),(1,7),
              (2,1),                  (2,5),(2,6),(2,7),
                    (3,2),(3,3),(3,4),(3,5),(3,6),(3,7),
        (4,0),(4,1),(4,2),(4,3),            (4,6),(4,7),
        (5,0),      (5,2),
        (6,0),(6,1),(6,2),      (6,4),(6,5),(6,6),
        (7,0),(7,1),            (7,4)
]
```

To test the implementation of `do_move_wall`, run:

```
python run.py
```
