![](http://kuuri.net/game/kobato/img/progress_1.png)

# KOBATO
KOBATO is a simple action game developed with Python, Pygame.  
Use the arrow keys to operate a red flying object and collect gems while avoiding enemies.

This game has a unique gimmick, **"discontinuous time operation"** , **"pseudo inertia"** .  
I recommend playing after reading the note at the end of this document.

## How to play

### Basics
Use the arrow keys to operate a red line.  
This is you.

If you hit the enemies that appear under the prescribed conditions, the life (displayed on the upper left of the screen) will decrease.  
You will lose tha game when life is exhausted.

When you touch the gem that appear on the screen, the "acquired gems" (displayed on the upper right of the screen) will increase.
Level (stage) will proceed as the number of acquired jewels reaches the prescribed number.
At this time, the number of "acquired gems" will be reset and the number of acquisition orders will be increased by one.
It is clear if you can proceed to level 10. (Score feature is not implemented.)

![](http://kuuri.net/game/kobato/img/title.png)

### Other operations
Other operations are as written on the game start screen.  
It is a comment below.

- R  
Replay recording starts when you enter "R" on the startup screen.
The replay file is saved in this folder.
- P  
Play the replay.
Replay refers to the replay file in the "replay" folder, but if there are multiple files, which one will be played is top of arbitrary order.  
- space  
Save the screenshot.
- enter  
Return to the game start screen.  
It is used to reset the game progress.
- esc  
Exit from the game.
You can also exit by closing the window.

## Note) About the unique element of this work
This work is basically a simple action game.
But please note the following two points.
These are special elements of this work, and you should be confused if you start without annotations.

### About the "discontinuous time operation"

This game proceeds with a turn system.
One turn begins with one input by the player, movement of all objects and collision judgment are done, and finally the result is outputted on the screen and it ends.
After that, the screen does not change at all until the next input.

### About the "pseudo inertia"
In this game, all objects are on an invisible grid.
The flying objects move from the intersection of this grid to other one, basically the same as the previous each turn.
The player's input and enemy's direction correction process work as a fine adjustment in the "single grid unit" of the arrival point in this movement.

## Licence
MIT Lisence for code, CC-BY for assets.