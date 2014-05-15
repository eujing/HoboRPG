import random

def getDamage (attack=0, attacker, weapon, target):
	total = 0.0
	#get basic damage first

	if attack == 0: #basic attack
		total = attacker.strength*2.5 + weapon*1.5
		if weapon != attacker.mainWeapon: total -= weapon*0.75
	else: #attack represents skill ID
		#todo add basic skill damage to total. implement later

	#for buff in playerBuffs:
		#total *= buff #todo check if buff applies?
	#todo rethink buff/debuff implementation

	total -= enemy.armour
	if total < 0: total = 0

	#todo implement criticals

	total *= random.randint(-96, 104)/100

	return total
