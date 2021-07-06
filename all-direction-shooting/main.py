# モジュールのインポート
import pygame
import sys
import random
import actors
import field
import utils

# ウィンドウの大きさ
WIN_W = 800
WIN_H = 600
# フレームレート
FRAME_RATE = 30

# メイン処理
def main():
	# pygameモジュールの初期化
	pygame.init()
	# タイトル設定
	pygame.display.set_caption("shooooooting")
	# スクリーンの初期化
	screen = pygame.display.set_mode((WIN_W, WIN_H))
	# clockオブジェクトの作成
	clock = pygame.time.Clock()
	
	timer = 0
	enemy_rate = 20
	enemy_count = 0
	font = utils.Font.set_font(128)
	
	player = actors.Player(WIN_W / 2, WIN_H / 2)
	background = field.Background(WIN_W, WIN_H)
	score = field.Score(WIN_W, WIN_H)
	enemies = []
	enemies.append(actors.Enemy(0, 0))
	enemies.append(actors.Enemy(WIN_W, WIN_H))

	while True:
		timer = timer + 1
		
		for event in pygame.event.get():
			# ウィンドウを閉じる
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		# 背景を塗りつぶす
		screen.fill((0, 0, 0))
		
		# ここから
		background.draw(screen)
		background.scroll(player)
		player.draw(screen)
		player.update(key, WIN_W, WIN_H)
		for b in player.bullets[:]:
			for e in enemies[:]:
				if b.collision(e):
					player.bullets.remove(b)
					enemies.remove(e)
					score.up_score()
					break
		for e in enemies:
			e.draw(screen, player)
			e.move(player)
			e.collision(player, screen)
		for e in enemies[:]:
			if e.HP <= 0:
				enemies.remove(e)
		score.draw(screen)
		
		# 敵を追加
		if enemy_count < 100:
			if timer % enemy_rate == 0:
				rand = random.randint(0, 3)
				if rand == 0:
					(ex, ey) = (-100, random.randint(-100, WIN_H + 100))
				elif rand == 1:
					(ex, ey) = (WIN_W + 100, random.randint(-100, WIN_H + 100))
				elif rand == 2:
					(ex, ey) = (random.randint(-100, WIN_W + 100), -100)
				else:
					(ex, ey) = (random.randint(-100, WIN_W + 100), WIN_H + 100)
				enemies.append(actors.Enemy(ex, ey))
				enemy_count += 1
			if timer % 100 == 0:
				enemy_rate -= 2
				if enemy_rate < 3:
					enemy_rate = 3
		
		# ゲームクリア
		if score.score == 100 * 100:
			text = utils.Font.set_text("GAME CLEAR", (255, 255, 0), font)
			text_w, text_h = font.size("GAME CLEAR")
			screen.blit(text, [(WIN_W - text_w) / 2, (WIN_H - text_h) / 2])
		# ゲームオーバー
		if player.HP <= 0:
			text = utils.Font.set_text("GAME OVER", (255, 0, 0), font)
			text_w, text_h = font.size("GAME OVER")
			screen.blit(text, [(WIN_W - text_w) / 2, (WIN_H - text_h) / 2])
		
		# 画面更新
		pygame.display.update()
		# フレームレートの設定
		clock.tick(FRAME_RATE)

if __name__ == '__main__':
	main()
