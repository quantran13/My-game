#!/usr/bin/python

from sys import exit
from random import randint, random
from data import *
from check import check
		

##############################
### Name:

print("Welcome! Let's make your character!")
name = raw_input("Your character's name: ")

###############################
### Create your character here

print("Your HP will be 6000.")
print("Your attack will affect normal attack,"), 
print("while your intelligent will affect magic attack.")
print("Your intelligent will be 110 - attack - defense.")
print("You will have 2 magic skill: ")
print("\t1. Fire ball (30 MP).\n\t2. Heal 600 HP (25 MP).")
print("Your MP will be your intel * 6.")

att, defe = -1, -1
while not 0 < att < 100 or not 0 < defe < 100 or att + defe > 110:
	try:	
		att = int(raw_input("Your character's attack: ").strip('\\'))
		defe = int(raw_input("Your character's defense: ").strip('\\'))
	except ValueError, NameError:
		pass
intel = 110 - att - defe
player = character(name, att, defe, intel)
print("Your character has been made!")
print("\tName: %s; Attack: %d; Defense: %d; Intelligent: %s\n")\
      % (player.name, player.att, player.defe, player.intel)

###############################
### Let's get to the game!

"""Add a room and some monsters"""

width = 10
height = 10
room1 = room(width,height,[])

add = []
while not len(add) == 6:
	a, b = randint(1, width-1), randint(1, width-1)
	try:
		add.append(monster(a,b,room1,'Bat',55,40,30,2200,13))
	except TypeError:
		pass

a, b = randint(1, width-1), randint(1, height-1)
add.append(monster(a,b,room1,'JB',65,40,8,2600,60))

room1.addmonsters(add)

"""First step here"""

room1.show(player)

print("An X means a monster."),
print("If you are next to a monster, you will have to fight it!\n")
inp = raw_input("Where do you want to put your character? ").strip('\\')

x = -1
y = -1

try:
	x,y = inp.strip('()').split(',')
	x = int(x) - 1
	y = int(y) - 1
except ValueError, NameError:
	pass

while player.nav(x,y,room1) == False:
	print("Cannot go there!")
	inp = raw_input("Where do you want to put your character? ").strip('\\')
	try:
		x,y = inp.strip('()').split(',')
		x = int(x) - 1
		y = int(y) - 1
	except ValueError, NameError:
		pass

room1.show(player)	

"""Now the main part of the game"""

print("\n Now, enter a any sequence of W,S,A,D to move."),
print("For example: SA will move you down once, then left once.\n")

wall = "You ran into a wall and die! Loser!"
while True:
	try:
		move = raw_input("> ").strip('\\')
		for ch in move:
			if ch == 'W' or ch == 'w':
				kq = player.nav(player.x,player.y-1,room1)
				check(kq, wall)
			if ch == 'A' or ch == 'a':
				kq = player.nav(player.x-1,player.y,room1)
				check(kq, wall)
			if ch == 'D' or ch == 'd':
				kq = player.nav(player.x+1,player.y,room1)
				check(kq, wall)
			if ch == 'S' or ch == 's':
				kq = player.nav(player.x,player.y+1,room1)
				check(kq, wall)
		room1.show(player)
	except EOFError, KeyboardInterrupt:
		print("\nBye!")
		exit(0)	
	if room1.win() == True:
		print("You win!")
		print("Press CTRL+D to quit")
