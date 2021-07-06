import pygame
import utils

###  背景クラス  ###
class Background:
	def __init__(self, win_w, win_h):
		self.img = utils.Image.img_background
		(self.w, self.h) = (self.img.get_width(), self.img.get_height())
		(self.x, self.y) = ((win_w - self.w) / 2, (win_h - self.h) / 2)
		(self.win_w, self.win_h) = (win_w, win_h)
		
	# 描画
	def draw(self, screen):
		screen.blit(self.img, [self.x, self.y])
	
	# スクロール
	def scroll(self, player):
		# プレイヤーが画面のどの位置に存在するかを0～1の値にする
		Normalization_x = player.x / self.win_w
		Normalization_y = player.y / self.win_h
		
		n_x = self.w - self.win_w
		n_y = self.h - self.win_h
		
		# プレイヤーの現在位置から背景の表示位置を調整
		self.x = n_x * Normalization_x - n_x
		self.y = n_y * Normalization_y - n_y

class Score:
	def __init__(self, win_w, win_h):
		self.score = 0
		self.font = utils.Font.set_font(64)
		(self.x, self.y) = (win_w, win_w)
	
	def draw(self, screen):
		message = "SCORE : " + str(self.score)
		text_w, text_h = self.font.size(message)
		text = utils.Font.set_text(message, (255,255,255), self.font)
		screen.blit(text, [self.x - text_w, 0])
	
	def up_score(self):
		self.score += 100

