import random

class Class:
	strength = 0
	intelligence = 0
	luck = 0
	agility = 0
	hp = 100

	currentHp = hp
	lv = 1

	skillPoints = 5

	isDefending = false
	currentTurnBuffs = 1

	weapon = null #at least 1?

	#def levelUp (self):
		#pass

class Alcoholic(Class):
	def __init__(self, id = -1):
		if id == -1: 
			#default lv 1
			strength = random.randint(6,10)
			intelligence = random.randint(3,5)
			luck = random.randint(2,3)
			agility = 20 - strength - intelligence - luck
		#load stats from save file with key id

	def levelUp(self):
		pass #todo: implement T-T

	def defend(self):
		isDefending = true







