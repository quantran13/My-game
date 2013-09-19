from random import randint, random
from time import sleep 


##############################
### character
class character(object):
	def __init__(self, name, att, defense, intel):
		self.name = name
		self.att = att
		self.defe = defense
		self.intel = intel
		self.hp = 6000
		self.mp = self.intel * 6
		self.x = 1
		self.y = 1
		self.lv = 1
		self.xp = 0
	
	def nav(self,x,y,room):
		if room.contains(x,y) == False:
			return False

		if room.cells[y][x] == ' ' or "potion" in room.cells[y][x]:
			room.cells[self.y][self.x] = ' '
			if room.cells[y][x] == "h_potion":
				print("You found a health potion! +1000 HP!")
				self.hp += 1000
			if room.cells[y][x] == "m_potion":
				print("You found a mana potion! +150 MP!")
				self.mp += 150
			self.x = x
			self.y = y
			self.room = room
			room.cells[y][x] = self
			for cell in room.adj_cells(self.x,self.y):
				if isinstance(cell, monster):
					self.room.show(self)
					print("Oh no! You are attacked!")
					print("What will you do?")
					choose = 1
					war = battle(self,cell)
					while not choose == '1' and not choose == '2':
						choose = raw_input("\t1. Fight!\n\t2. Flee!\n?> ")
					if choose == '1':
						kq2 = war.fight()
						check(kq2, "You have been defeated! Loser!")
						if kq2 == True:
							print("+%d XP") % cell.xp
							self.lvup(cell.xp)
							room.cells[cell.y][cell.x] = ' '
					else:
						kq2 = war.flee()
						if kq2 == False:
							kq2 = war.fight()
							check(kq2, "You have been defeated! Loser!")
							if kq2 == True:
								print("+%d XP") % cell.xp
								self.lvup(cell.xp)
								room.cells[cell.y][cell.x] = ' '
			return True
		else:
			return 'F'

	def lvup(self, xp):
		self.xp += xp
		while self.xp >= self.lv * (self.lv + 25):
			self.lv += 1
			self.att += 2
			self.defe += 2
			self.intel += 2
			print("Level up! You are now level %d") % self.lv
			print("+2 attack, defense, intelligent!")



##############################
### room
class room(object):
	def __init__(self,width,height,monsters):
		self.width = width
		self.height = height
		self.monsters = monsters
		self.cells = []	
		for y in range(self.height):
			self.cells.append([])
			for x in range(self.width):
				self.cells[y].append(' ')
		for monster in monsters:
			self.cells[monster.y][monster.x] = monster
		
		x, y = randint(0, width-1), randint(0, height-1)
		while not self.cells[y][x] == ' ':
			x, y = randint(0, width-1), randint(0, height-1)
		self.cells[randint(0, width-1)][randint(0, height-1)] = "h_potion"

		while not self.cells[y][x] == ' ':
			x, y = randint(0, width-1), randint(0, height-1)
		self.cells[y][x] = "m_potion"

	
	def show(self, pl):
		print("Level: %d; EXP: %d") % (pl.lv, pl.xp)
		print("Attack: %d; Defense: %d; Intelligent: %d.") % (pl.att, pl.defe, pl.intel)
		print("HP: %d     MP: %d\n") % (pl.hp, pl.mp)
		for line in self.cells:
			for cell in line:
				if isinstance(cell, monster):
					if cell.name == "JB":
						print("[?]"),
					else:
						print("[X]"),
				elif isinstance(cell, character):
					print("[0]"),
				else:
					print("[ ]"),
			print("\n")

	def addmonsters(self, addm):
		for m in addm:
			self.cells[m.y][m.x] = m
			self.monsters.append(m)

	def win(self):
		result = True
		for line in self.cells:
			for cell in line:
				if isinstance(cell, monster):
					result = False
					break
		return result

	def adj_cells(self,x,y):
		for dx,dy in (1, 0), (0, 1), (-1, 0), (0, -1):
			if self.contains(x + dx, y + dy):
				yield self.cells[y+dy][x+dx]

	def contains(self, x, y):
		return (0 <= x < self.width) and (0 <= y < self.height)



##############################
### battle
class battle(object):
	def __init__(self,p1,p2):
		self.p1 = p1
		self.p2 = p2

	def fight(self):
		while self.p1.hp > 0 and self.p2.hp > 0:
			hp_1 = self.p1.hp
			hp_2 = self.p2.hp
			mp   = self.p1.mp
			print("You: HP: %d; MP: %d.\nOpponent: HP: %d.") % (hp_1, mp, hp_2)

			damage_1 = 0
			op1 = ''
			while not op1 == '1' and not op1 == '2' and not op1 == '3':
				print("\t1. Normal attack.\n\t2. Fire ball.\n\t3. Heal")
				op1 = raw_input("?> ").strip('\\')
				if op1 == '2':
					if mp < 30:
						print("Not enough mana!")
						op1 = ''
				elif op1 == '3':
					if mp < 25:
						print("Not enough mana!")
						op1 = ''
			if op1 == '1':
				diff = self.p1.att - self.p2.defe
				if diff < 0:
					diff = 0
				damage_1 = randint(15,100) + diff * 10
			elif op1 == '2':
				diff = self.p1.intel - self.p2.intdef
				if diff < 0:
					diff = 0
				damage_1 = randint(15,100) + diff * 12
				mp_lost = 30
			elif op1 == '3':
				mp_lost = 25
			crit_1 = randint(1,10)
			if crit_1 == 1:
				damage_1 *= 2

			op2 = randint(1,5)
			if op2 == 5:
				dodge = True
			else:
				dodge = False
				diff = self.p2.att - self.p1.defe
				if diff < 0:
					diff = 0
				damage_2 = randint(15,125) + diff*10
			crit_2 = randint(1,10)
			if crit_2 == 1:
				damage_2 *= 2

			sleep(1)
			print("")

			if op1 == '1' and dodge == False:
				self.p2.hp -= damage_1
				self.p1.hp -= damage_2
				if crit_1 == 1:
					print("Critical hit!"),
				print("You attacked %s for %d hp!") % (self.p2.name, damage_1)
				if crit_2 == 1:
					print("Critical hit!"),
				print("%s damaged you for %d hp!") % (self.p2.name, damage_2)
			elif op1 == '1' and dodge == True:
				print("You attacked %s but %s dodged!")\
			          % (self.p2.name, self.p2.name)
			elif op1 == '2' and dodge == True:
				self.p2.hp -= damage_1
				self.p1.mp -= mp_lost
				if crit_1 == 1:
					print("Critical hit!"),
				print("You used Fire ball! %s cannot dodge your Fire ball!")\
					  % self.p2.name
				print("You damaged %s for %d hp!") % (self.p2.name, damage_1)
			elif op1 == '2' and dodge == False:
				self.p2.hp -= damage_1
				self.p1.mp -= mp_lost
				self.p1.hp -= damage_2	
				if crit_1 == 1:
					print("Critical hit!"),
				print("You used Fire ball and damaged %s for %d hp!")\
					  % (self.p2.name, damage_1)
				if crit_2 == 1:
					print("Critical hit!"),
				print("%s damaged you for %d hp!") % (self.p2.name, damage_2)
			elif op1 == '3' and dodge == False:
				self.p1.hp -= damage_2 - 600
				self.p1.mp -= mp_lost
				print("You heal yourself! +600 HP!")
				print("%s damaged you for %d hp!") % (self.p2.name, damage_2)
			elif op1 == '3' and dodge == True:
				self.p1.hp += 600
				self.p1.mp -= mp_lost
				print("You heal yourself! +600 HP!")
				print("%s dodged!?! What a fool!") % self.p2.name

			print("\n----------------------\n")
			sleep(1)


		if self.p1.hp <= 0:
			return False
		else:
			return True

				
	def flee(self):
		x = randint(1,2)
		if x == 1:
			print("\nYou have fled successfully!")
			return True
		else:
			print("\nOh no you cannot flee! You must fight!")
			return False



##############################
### monster
class monster(object):
    def __init__(self,x,y,room,name,att,defe,intdef,hp,xp):
		check = True
		for m in room.monsters:
			if (x, y) == (m.x, m.y):
				check = False
				break


		if check == True:
			self.x = x
			self.y = y
			self.name = name
			self.att = att
			self.defe = defe
			self.intdef = intdef
			self.hp = hp
			self.xp = xp
		else:
			del self
