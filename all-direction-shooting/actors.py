import utils
import pygame
import math
import random

class Actor:
	def __init__(self, x, y):
		# 位置座標
		(self.x, self.y) = (x, y)
		# 移動スピード
		self.speed = 12
		# 大きさ
		self.size  = 48
		# 体力
		self.HP = 10
		# 弾を格納するリスト
		self.bullets = []
		# カウント変数
		self.time = 0

class Player(Actor):
	def __init__(self, x, y):
		super().__init__(x, y)
		# ターゲットの座標
		(self.target_x, self.target_y) = (x, y)
		# プレイヤー画像
		self.img = utils.Image.img_player
		self.img = pygame.transform.scale(self.img, (self.size, self.size))
		# ターゲット画像
		self.img_target = utils.Image.img_target
		self.img_target = pygame.transform.scale(self.img_target, (self.size, self.size))
		# 体力バー画像
		self.img_bar1 = utils.Image.img_bar[0]
		self.img_bar1 = pygame.transform.scale(self.img_bar1, (160, 48))
		self.img_bar2 = utils.Image.img_bar[1]
		self.img_bar2 = pygame.transform.scale(self.img_bar2, (131, 27))
	
	def draw(self, screen):
		# 弾を描画
		for b in self.bullets:
			b.draw(screen)
		
		# プレイヤーを描画
		if self.HP > 0:
			rotate_img = pygame.transform.rotate(self.img, self.getAngle())
			img_rect = rotate_img.get_rect()
			img_rect.center = (self.x, self.y)
			screen.blit(rotate_img, img_rect)
		
		# HPバー描画
		self.img_bar2 = pygame.transform.scale(self.img_bar2, (int(13.1 * self.HP), 27))
		screen.blit(self.img_bar1, [0, 0])
		screen.blit(self.img_bar2, [15, 11])
		
		# 的の描画
		screen.blit(self.img_target, [self.target_x  - self.size / 2, self.target_y  - self.size / 2])
		
		# HPが減ったときに画面に警告
	
	def update(self, key, win_w, win_h):
		self.time += 1
		for b in self.bullets:
			b.move()
		if self.HP > 0:
			self.move(key, win_w, win_h)
			self.shot()
		self.set_target_pos()
		self.clean_bullet(win_w, win_h)
	
	# 的の座標取得
	def set_target_pos(self):
		self.target_x, self.target_y = pygame.mouse.get_pos()
	
	# 的とプレイヤーの角度を取得
	def getAngle(self):
		return math.degrees(math.atan2(self.target_x - self.x, self.target_y - self.y)) + 180
	
	# 移動
	def move(self, key, win_w, win_h):
		if key[pygame.K_RIGHT] == 1:
			self.x += self.speed
		if key[pygame.K_LEFT] == 1:
			self.x -= self.speed
		if key[pygame.K_UP] == 1:
			self.y -= self.speed
		if key[pygame.K_DOWN] == 1:
			self.y += self.speed
		# 移動制限
		if self.x < 0:
			self.x = 0
		elif self.x > win_w:
			self.x = win_w
		if self.y < 0:
			self.y = 0
		elif self.y > win_h:
			self.y = win_h
	
	# 射撃
	def shot(self):
		click = pygame.mouse.get_pressed()
		if click[0]:
			if self.time % 5 == 0:
				self.bullets.append(Bullet(self.x, self.y, self.getAngle()))
	
	# 弾削除
	def clean_bullet(self, win_w, win_h):
		for b in self.bullets[:]:
			if b.delete(win_w, win_h):
				self.bullets.remove(b)
	
	def damage(self, num):
		self.HP -= num
		if self.HP < 0:
			self.HP = 0
	
class Enemy(Actor):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.speed = 8
		# 敵画像
		image = utils.Image.img_enemies[random.randint(0, 3)]
		self.img = pygame.transform.scale(image, (self.size, self.size))
	
	def draw(self, screen, player):
		rotate_img = pygame.transform.rotate(self.img, self.getAngle(player))
		img_rect = rotate_img.get_rect()
		img_rect.center = (self.x, self.y)
		screen.blit(rotate_img, img_rect)
	
	# 移動
	def move(self, player):
		if player.HP > 0:
			# 敵→プレイヤーのベクトルを計算
			(vx, vy) = (player.x - self.x, player.y - self.y)
			l = math.sqrt(vx * vx + vy * vy)
			# ベクトルを正規化
			if l == 0:
				(vx, vy) = (0, 0)
			else:
				(vx, vy) = (vx / l, vy / l)
			(self.x, self.y) = (self.x + vx * self.speed, self.y + vy * self.speed)
	
	# プレイヤーとの角度を取得
	def getAngle(self, player):
		return math.degrees(math.atan2(player.x - self.x, player.y - self.y)) + 180
	
	# プレイヤーとの当たり判定
	def collision(self, player, screen):
		if (player.x - player.size / 2) < self.x and (player.x + player.size / 2) > self.x and (player.y - player.size / 2) < self.y and (player.y + player.size / 2) > self.y:
			self.HP = 0
			player.damage(1)
			screen.fill((255, 0, 0))
	
	

class Bullet:
	Speed = 16   # 弾の速度
	Size  = 20  # 弾の大きさ
	
	def __init__(self, x, y, angle):
		# 位置座標
		(self.x, self.y) = (x, y)
		# 発射位置
		(self.ax, self.ay) = (x, y)
		# 半径
		self.rad = 0
		# 発射角度
		self.angle = angle * -1 - 90
		image = utils.Image.img_bullet
		self.img = pygame.transform.scale(image, (Bullet.Size, Bullet.Size))
	
	def draw(self, screen):
		screen.blit(self.img, [self.x  - Bullet.Size / 2, self.y  - Bullet.Size / 2])
	
	# 弾の軌道
	def move(self):
		(self.x, self.y) = (self.rad * math.cos(math.radians(self.angle)) + self.ax, self.rad * math.sin(math.radians(self.angle)) + self.ay)
		self.rad += Bullet.Speed
	
	# 弾の削除
	def delete(self, win_w, win_h):
		if self.x < -Bullet.Size or self.y < -Bullet.Size:
			return True
		elif self.x > win_w + Bullet.Size or self.y > win_h + Bullet.Size:
			return True
		return False
	
	# 弾の当たり判定
	def collision(self, actor):
		if (actor.x - actor.size / 2) < self.x and (actor.x + actor.size / 2) > self.x and (actor.y - actor.size / 2) < self.y and (actor.y + actor.size / 2) > self.y:
			return True
		return False
