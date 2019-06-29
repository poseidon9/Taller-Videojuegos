import sys, pygame

WHITE = [255, 255, 255]
GRAVITY = 1

class GameEntity(object):
	x = 0
	y = 0
	sprite = None
	rect = None

	def __init__(self, x, y, image):
		self.x = x
		self.y = y
		self.sprite = pygame.image.load(image)
		self.setSpriteFromLoadedImage(self.sprite)

	def setSpriteFromLoadedImage(self, image):
		self.sprite = image
		self.rect = self.sprite.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

	def update(self):
		self.rect.x = self.x
		self.rect.y = self.y


#https://www.pygame.org/wiki/Spritesheet

class SpriteSheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x, y, x + offset, y + soffset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)





class SpriteStripAnim(GameEntity):
    """sprite strip animator
    
    This class provides an iterator (iter() and next() methods), and a
    __add__() method for joining strips which comes in handy when a
    strip wraps to the next row.
    """
    def __init__(self, filename, rect, count, colorkey=None, loop=False, frames=1):
        """construct a SpriteStripAnim
        
        filename, rect, count, and colorkey are the same arguments used
        by spritesheet.load_strip.
        
        loop is a boolean that, when True, causes the next() method to
        loop. If False, the terminal case raises StopIteration.
        
        frames is the number of ticks to return the same image before
        the iterator advances to the next image.
        """
        self.filename = filename
        ss = SpriteSheet(filename)
        self.images = ss.load_strip(rect, count, colorkey)
        self.i = 0
        self.loop = loop
        self.frames = frames
        self.f = frames
    def iter(self):
        self.i = 0
        self.f = self.frames
        return self
    def next(self):
        if self.i >= len(self.images):
            if not self.loop:
                raise StopIteration
            else:
                self.i = 0
        image = self.images[self.i]
        self.f -= 1
        if self.f == 0:
            self.i += 1
            self.f = self.frames
        return image
    def __add__(self, ss):
        self.images.extend(ss.images)
        return self


class Platform(GameEntity):
	def __init__(self, x, y):
		super(Platform, self).__init__(x, y, "plataforma.png")

class Player(GameEntity):
	NORTE = 1; ESTE = 2; SUR = 3; OESTE = 4
	game_map = None
	strips = None
	speed = 5
	JUMP_FORCE = 10
	on_ground = False
	change_x = 0
	change_y = 0
	looking_right = True
	current_animation = "RUN"


	def __init__(self, game_map, x, y):
		self.game_map = game_map
		super(Player, self).__init__(x, y, "player.png")
		self.setupString()

	def setupString(self):
		self.strips = {
			"IDLE": SpriteStripAnim('megaman_spritesheet.png', (0,4,32,34), 3, WHITE, True, 6),
			"RUN": SpriteStripAnim('megaman_spritesheet.png', (0,95,32,34), 10, WHITE, True, 6)
		}

	def action(self, key):
		if key[pygame.K_w]:
			self.jump()
		#	self.mover(self.NORTE)
		if key[pygame.K_d]:
			self.mover(self.ESTE)
		#if key[pygame.K_s]:
		#	self.mover(self.SUR)
		if key[pygame.K_a]:
			self.mover(self.OESTE)

	def jump(self):
		if self.on_ground:
			self.change_y = -self.JUMP_FORCE
			self.on_ground = False


	def mover(self, DIRECTION):
		if DIRECTION == self.ESTE:
			if self.rect.x < 640:
				self.change_x = self.speed
				self.current_animation = "RUN"
				self.looking_right = True
		if DIRECTION == self.OESTE:
			if self.rect.x > 0:
				self.change_x = -self.speed
				self.current_animation = "RUN"
				self.looking_right = False
		#if DIRECTION == self.SUR:
		#	if self.rect.y < 480:
		#		self.change_y = self.speed
		#		self.current_animation = "RUN"
		#if DIRECTION == self.NORTE:
		#	if self.rect.y > 0:
		#		self.change_y = -self.speed
		#		self.current_animation = "RUN"
		
	def collideKey(self):
		if not self.game_map.key.on_player:
			if self.rect.colliderect(self.game_map.key.rect):
				self.game_map.key.on_player = True

	def collideDoor(self):
		if self.game_map.key.on_player:
			if self.rect.colliderect(self.game_map.door.rect):
				self.game_map.door.is_open = True

	def collidePlatform(self, platform):
		if self.change_x != 0:
			temp_x = self.rect.x
			self.rect.x += self.change_x
			hit = self.rect.colliderect(platform.rect)
			if hit:
				if self.change_x < 0:
					self.x = platform.rect.right + 1
				elif self.change_x > 0:
					self.x = platform.rect.left - self. rect.width - 1
				self.change_x = 0
				self.current_animation = "IDLE"
			self.rect.x = temp_x
		if self.change_y != 0:
			temp_y = self.rect.y
			self.rect.y += self.change_y
			hit = self.rect.colliderect(platform.rect)
			if hit:
				if self.change_y < 0:
					self.y = platform.rect.bottom + 1
				elif self.change_y > 0:
					self.y = platform.rect.top - self. rect.height - 1
					self.on_ground = True
				self.change_y = 0
				self.current_animation = "IDLE"
			self.rect.y = temp_y

	def  update(self):
		for platform in self.game_map.platforms:
			self.collidePlatform(platform)
		self.x += self.change_x
		self.y += self.change_y
		super(Player, self).update()
		if self.looking_right:
			super(Player, self).setSpriteFromLoadedImage(self.strips[self.current_animation].next())
		else:
			super(Player, self).setSpriteFromLoadedImage(pygame.transform.flip(self.strips[self.current_animation].next(), True, False))

		self.change_x = 0
		if self.change_y < 10:
			self.change_y += GRAVITY
		else:
			self.change_y = 10
		self.collideKey()
		self.collideDoor()

class Map:
	door = None
	key = None
	platforms = None
	player = None

	def getElements(self, door, key, platforms, player):
		self.door = door
		self.key = key
		self.platforms = platforms
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
	print("Fase5")
	print("https://github.com/poseidon9/Taller-Videojuegos")

	pygame.init()
	clock = pygame.time.Clock()
	white = [255, 255, 255]

	MAX_FPS = 60
	size = width, height = 640, 480
	screen = pygame.display.set_mode(size)
	dt = clock.tick(MAX_FPS)
	
	game_map = Map()
	player = Player(game_map, 100, 60)
	key = Key(0,0)
	door = Door(300, 300)
	platforms = [Platform(100, 100)]

	game_map.getElements(door, key, platforms, player)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		player.action(pygame.key.get_pressed())

		if(door.is_open):
			break

		screen.fill(white)
		screen.blit(door.sprite, door.rect)
		for platform in platforms:
			screen.blit(platform.sprite, platform.rect)
		if not key.on_player:
			screen.blit(key.sprite, key.rect)
		screen.blit(player.sprite, player.rect)
		pygame.display.flip()
		player.update()
		clock.tick_busy_loop(MAX_FPS)

main()
