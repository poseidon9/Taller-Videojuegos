import sys, random

class GameEntity(object):
	x = 0
	y = 0

	def __init__(self, x, y):
		self.x = x
		self.y = y

class Player(GameEntity):
	NORTE = 1; ESTE = 2; SUR = 3; OESTE = 4
	game_map = None

	def __init__(self, game_map, x, y):
		self.game_map = game_map
		super(Player, self).__init__(x, y)

	def action(self):
		while True:
			print("1)Mover\n2)Agarrar\n3)Usar Llave")
			opc = int(raw_input())
			if opc == 1:
				print("1)Norte\n2)Este\n3)Sur\n4)Oeste\n")
				opc = int(raw_input())
				if opc > 0 and opc < 5:
					self.mover(opc)
					break;
				else:
					print("No Existe esa Direccion")
			elif opc == 2:
				if not self.game_map.key.on_player:
					if self.game_map.key.x == self.x and self.game_map.key.y == self.y:
						self.game_map.key.on_player = True
						print("Agarraste la Llave!")
					else:
						print("Aqui no esta la Llave!")
				else:
					print("Ya Tienes la Llave!")
				break;


			elif opc == 3:
				if self.game_map.key.on_player:
					if self.game_map.door.x == self.x and self.game_map.door.y == self.y:
						self.game_map.door.is_open = True
						print("Abriste la Puerta!")
					else:
						print("Aqui no esta la Puerta!")
				else:
					print("No Tienes la Llave!")
				break;

			else:
				print("No existe esa Direccion")

	def mover(self, DIRECTION):
		if DIRECTION == self.NORTE:
			if self.x > 0:
				self.x -= 1
			else:
				print("Esta en la Orilla del Norte")
		if DIRECTION == self.ESTE:
			if self.y < self.game_map.size[1] -1:
				self.y += 1
			else:
				print("Esta en la Orilla del ESTE")
		if DIRECTION == self.SUR:
			if self.x < self.game_map.size[0] - 1:
				self.x += 1
			else:
				print("Esta en la Orilla del SUR")
		if DIRECTION == self.OESTE:
			if self.y > 0:
				self.y -= 1
			else:
				print("Esta en la Orilla del OESTE")

class Map:
	size = []
	game_map = []
	door = None
	key = None
	player = None

	def __init__(self, size):
		self.size = size
		self.createMap()

	def getElements(self, door, key, player):
		self.door = door
		self.key = key
		self.player = player

	def createMap(self):
		for x in range(self.size[0]):
			self.game_map.append([])
			for y in range(self.size[1]):
				self.game_map[x].append(0)

	def setElementsonMap(self):
		self.game_map[self.door.x][self.door.y] = 3
		if not self.key.on_player:
			self.game_map[self.key.x][self.key.y] = 2
		self.game_map[self.player.x][self.player.y] = 1

	def cleanMap(self):
		for x in range(self.size[0]):
			for y in range(self.size[1]):
				self.game_map[x][y] = 0
		self.setElementsonMap()

	def printSymbol(self, symbol):
		if symbol == 1:
			return "o"
		if symbol == 2:
			return "k"
		if symbol == 3:
			return "d"
		else:
			return "."

	def printMap(self):
		print("o = jugador 	k = llave 	d = puerta")
		print(self.printSymbol(self.game_map[0][0]) + "|" + self.printSymbol(self.game_map[0][1]) + "|" + self.printSymbol(self.game_map[0][2]) + "|" + self.printSymbol(self.game_map[0][3]) + "|" + self.printSymbol(self.game_map[0][4]))
		print("_|_|_|_|_")
		print(self.printSymbol(self.game_map[1][0]) + "|" + self.printSymbol(self.game_map[1][1]) + "|" + self.printSymbol(self.game_map[1][2]) + "|" + self.printSymbol(self.game_map[1][3]) + "|" + self.printSymbol(self.game_map[1][4]))
		print("_|_|_|_|_")
		print(self.printSymbol(self.game_map[2][0]) + "|" + self.printSymbol(self.game_map[2][1]) + "|" + self.printSymbol(self.game_map[2][2]) + "|" + self.printSymbol(self.game_map[2][3]) + "|" + self.printSymbol(self.game_map[2][4]))
		print("_|_|_|_|_")
		print(self.printSymbol(self.game_map[3][0]) + "|" + self.printSymbol(self.game_map[3][1]) + "|" + self.printSymbol(self.game_map[3][2]) + "|" + self.printSymbol(self.game_map[3][3]) + "|" + self.printSymbol(self.game_map[3][4]))
		print("_|_|_|_|_")
		print(self.printSymbol(self.game_map[4][0]) + "|" + self.printSymbol(self.game_map[4][1]) + "|" + self.printSymbol(self.game_map[4][2]) + "|" + self.printSymbol(self.game_map[4][3]) + "|" + self.printSymbol(self.game_map[4][4]))

class Key(GameEntity):
	on_player = False

	def __init__(self, x, y):
		super(Key, self).__init__(x, y)

class Door(GameEntity):
	is_open = False

	def __init__(self, x, y):
		super(Door, self).__init__(x, y)

def main():
	print("Fase3")
	print("https://github.com/poseidon9/Taller-Videojuegos")

	while(1):
		print("1:Jugar\n2:Salir")
		opc = raw_input()
		active2 = True
		game_map = Map([5, 5])
		player = Player(game_map, 2, 2)
		key = Key(0, 0)
		door = Door(4, 4)
		game_map.getElements(door, key, player)

		if opc == "1":
			while(active2):
				game_map.cleanMap()
				game_map.printMap()
				active = True
				while active:
					player.action()
					game_map.cleanMap()
					game_map.printMap()
					if(door.is_open):
						print("Felicidades Acabaste el juego!")
						active = False
						active2 = False
		elif opc == "2":
			break
		else:
			print("No existe Dicha Opcion")

main()
