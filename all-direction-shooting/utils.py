import pygame

class Image:
	img_background = pygame.image.load("./images/Background.png")
	img_player     = pygame.image.load("./images/Player.png")
	img_target     = pygame.image.load("./images/Target.png")
	img_bullet     = pygame.image.load("./images/Bullet.png")
	img_enemies    = [pygame.image.load("./images/Enemy1.png"), pygame.image.load("./images/Enemy2.png"), pygame.image.load("./images/Enemy3.png"), pygame.image.load("./images/Enemy4.png")]
	img_bar        = [pygame.image.load("./images/HPbar.png"), pygame.image.load("./images/HPbar-fill.png")]

class Font:
	filename = "./fonts/HeadlinerNo.45 DEMO.ttf"
	
	@staticmethod
	def set_text(str, color, font):
		return font.render(str, True, color)
	
	@staticmethod
	def set_font(size):
		return pygame.font.Font(Font.filename, size)
