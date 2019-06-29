import sys, pygame

class GameEntity(object):
	x = 0
	y = 0
	sprite = None
	rect = None

	def __init__(self, x, y, image):
		self.sprite = pygame.image.load(image)
		self.rect = self.sprite.get_rect()
		self.rect.x =  x
		self.rect.y =  y

class Player(GameEntity):
	NORTE = 1; ESTE = 2; SUR = 3; OESTE = 4
	game_map = None

	def __init__(self, game_map, x, y):
		self.game_map = game_map
		super(Player, self).__init__(x, y, "player.png")

	def action(self, key):
		if key[pygame.K_w]:
			self.mover(self.NORTE)
		if key[pygame.K_d]:
			self.mover(self.ESTE)
		if key[pygame.K_s]:
			self.mover(self.SUR)
		if key[pygame.K_a]:
			self.mover(self.OESTE)


	def mover(self, DIRECTION):
		if DIRECTION == self.NORTE:
			if self.rect.y > 0:
				self.rect.y -= 5
		if DIRECTION == self.ESTE:
			if self.rect.x < 640:
				self.rect.x += 5
		if DIRECTION == self.SUR:
			if self.rect.y < 480:
				self.rect.y += 5
		if DIRECTION == self.OESTE:
			if self.rect.x > 0:
				self.rect.x -= 5
		self.collideKey()
		self.collideDoor()

	def collideKey(self):
		if not self.game_map.key.on_player:
			if self.rect.colliderect(self.game_map.key.rect):
				self.game_map.key.on_player = True

	def collideDoor(self):
		if self.game_map.key.on_player:
			if self.rect.colliderect(self.game_map.door.rect):
				self.game_map.door.is_open = True

class Map:
	door = None
	key = None
	player = None

	def getElements(self, door, key, player):
		self.door = door
		self.key = key
		self.player = player

class Key(GameEntity):
	on_player = False

	def __init__(self, x, y):
		super(Key, self).__init__(x, y, "key.png")

class Door(GameEntity):
	is_open = False

	def __init__(self, x, y):
		super(Door, self).__init__(x, y, "door.png")

def main():
	print("Fase4")
	print("https://github.com/poseidon9/Taller-Videojuegos")

	pygame.init()
	clock = pygame.time.Clock()
	white = [255, 255, 255]

	MAX_FPS = 10
	size = width, height = 640, 480
	screen = pygame.display.set_mode(size)
	dt = clock.tick(MAX_FPS)
	
	game_map = Map()
	player = Player(game_map, 320, 240)
	key = Key(0,0)
	door = Door(300, 300)

	game_map.getElements(door, key, player)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		player.action(pygame.key.get_pressed())

		if(door.is_open):
			break

		screen.fill(white)
		screen.blit(door.sprite, door.rect)
		if not key.on_player:
			screen.blit(key.sprite, key.rect)
		screen.blit(player.sprite, player.rect)
		pygame.display.flip()
		clock.tick_busy_loop(MAX_FPS)

main()
