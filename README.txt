# 15-112_Term_Project

Name - Dungeon Wizard
Description - Dungeon Wizard is Roguelike video game, that has many randomized aspects, including randomly generated floors, monsters, bosses, and items. The player plays as a wizard that traverses multiple rooms and floors, trying to find the boss room. Once the player defeats the cyclop boss, the player must travel down to the next floor where the enemies become faster and stronger. There are randomly spawned items that the player can pick up to help them along the way. If the player manages to defeat the boss on the 3rd floor, the player will beat the game. 


How to run the game:
There are multiple files that need to be in the same directory: 
app.py, rooms.py, monsters.py, sprites.py, player.py, StacksAndQueues.py, cmu_112_graphics.py
User must be able to run a python file
PIL/Pillow must also be downloaded (details on how to install these are here: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html)
The main file is app.py and the user must run this file to run the game.

Libraries used:
cmu_112_graphics
PIL/Pillow for images

Commands:
W - UP
A - LEFT
S - DOWN 
D - RIGHT
Left-Mouse - Shoots in any direction
Arrow keys - Shoots in cardinal directions
SPACE - Special Attack(Hits touching monsters harder and sends shots in all directions)
M - MAP
R - Restarts Game
B - Boss room
C - Debug mode: No damage, Noclip, Unlimited Mana, Enter any door




# Overall goals:
-Roguelike Game
-Everything is randomized
-Random Dungeon generator, that has multiple levels
-Multiple different enemies with different movement/attack mechanics
-A handful of bosses that increase in difficulty(goal: create 5 different bosses for 5 different levels, increase in difficulty as you go do in levels)
-Random objects/obstacles in side each room 
-Mini-map that keeps track of the rooms that have been seen
-Player has a health bar(each room should have a chance at giving more health back)
-Player only has one life
-Each floor has a boss room, once you beat the boss the player can go down a level(can't go back up)
-Once a player goes down a floor the data storing the floor above should clear the data so that the game doesn't get too slow. 
-Once the player enters a room the doors lock until the player defeats all of the monsters.

