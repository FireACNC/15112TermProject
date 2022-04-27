'Spider: No way home' is a game project designed for 15112 term project.
It is a maze game but you are controlling the maze rather than the character.
The game can also be played online by two players where player 2 place bombs to prevent player 1 from solving the maze.

Github: https://github.com/FireACNC/15112TermProject.git

Before exploring this project:
1. Libraries
    Make sure to have working cmu_cs3_graphics.py and cmu_graphics folder underthe same folder of all the python files presented in the project.
    Socket, threading, time, queue, random, copy, math are required to be installed.

2. Instructions
    Run 'main.py' to start game for player 1. Press any key to start.
    In the setting UI of p1:
        Instructions are provided at the top.
        Press ‘maze size’ to switch maze size between 5x5 to 15x15.
        Press ‘maze algorithm’ to switch between random or different maze algorithms.
        Press ‘lock & key’ to enable/disable lock and key feature, generate a lock at exit that requires the spider to pick up a key to unlock.
        Press ‘bombs’ to enable two-player mode (details provided later).

    In the game UI of p1:
        Current maze algorithm and maze solved will be displayed at the top and bottom of the maze
        Press A and D to rotate the maze.
        Press R to restart current level.
        Press S to enable path finder.
        Press Esc to enter the setting UI.

    To play in a two player mode, run 'main_p2.py' in a separate console while 'main.py' is running.
    To play the game on seperate computers, change the IP address in both 'client.py' and 'server.py' to current IP address.
    In game UI of p2:
        Instructions are provided at the bottom.
        If p1 is in setting mode or two-player mode not enabled, there would be a waiting message.
        Spider position will be displayed on the screen in green.
        Click on the board to place a bomb in p1’s game. 
            The bomb need to be at least one block away from the spider.
            Each block can only be bombed once, turning red and became unable to be clicked after the first click.

Enjoy!