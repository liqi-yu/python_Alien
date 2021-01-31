import sys
import pygame
from alien import Alien
from bullet import Bullet

def check_keydown_events(event,ai_settings,screen,ship,bullets):
	'''相应按键'''
	if event.key==pygame.K_RIGHT:
		ship.moving_right=True
	elif event.key==pygame.K_LEFT:
		ship.moving_left=True
	elif event.key==pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)

def check_keyup_events(event,ship):
	'''相应松开'''
	if event.key==pygame.K_RIGHT:
		ship.moving_right=False
	elif event.key==pygame.K_LEFT:
		ship.moving_left=False

def check_events(ai_settings,screen,ship,bullets):
	'''相应按键和鼠标事件'''
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type==pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		elif event.type==pygame.KEYUP:
			check_keyup_events(event,ship)

def update_screen(ai_settings,screen,ship,aliens,bullets):
	'''更新屏幕上的图片，并切换到新屏幕'''
	#每次循环都重绘屏幕
	screen.fill(ai_settings.bg_color)
	for bullet in bullets:
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)

	#让最近绘制的屏幕可见
	pygame.display.flip()

def update_bullets(ai_settings,screen,ship,aliens,bullets):
	'''更新子弹的位置，并删除已消失的子弹'''
	#更新子弹的位置
	bullets.update()

	#删除已消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets)

def check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets):
	#检查是否有子弹击中了外星人
	#如果是，就删除相应的子弹和外星人
	collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)

	if len(aliens)==0:
		#删除现有的子弹并新建一群外星人
		bulltes.empty()
		create_fleet(ai_settings,screen,ship,aliens)

def fire_bullet(ai_settings,screen,ship,bullets):
	'''如果还没有达到限制，就发射一颗子弹'''
	#创建新子弹，并将其加入到编组bullets中
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet=Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)

def get_number_aliens_x(ai_settings,alien_width):
	'''计算每行可容纳多少个外星人'''
	available_space_x=ai_settings.screen_width-2*alien_width
	number_aliens_x=int(available_space_x/(2*alien_width))
	return number_aliens_x

def get_number_rows(ai_settigns,ship_height,alien_height):
	'''计算屏幕可容纳多少行外星人'''
	available_space_y=(ai_settigns.screen_height-(3*alien_height)-ship_height)
	number_rows=int(available_space_y/(2*alien_height))
	return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	'''创建一个外星人并将其放在当前行'''
	alien=Alien(ai_settings,screen)
	alien_width=alien.rect.width
	alien.x=alien_width+2*alien_width*alien_number
	alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
	alien.rect.x=alien.x
	aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
	'''创建外星人群'''
	#创建一个外星人，并计算一行可容纳多少个外星人
	#外星人间距为外星人宽度
	alien=Alien(ai_settings,screen)
	number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
	number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)

	#创建外星人群
	for row_number in range(number_rows):
		#创建第一行外星人
		for alien_number in range(number_aliens_x):
			#创建一个外星人并加入当前行
			create_alien(ai_settings,screen,aliens,alien_number,row_number)

def check_fleet_edges(ai_settings,aliens):
	'''有外星人到达边缘时采取相应的措施'''
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break

def change_fleet_direction(ai_settings,aliens):
	'''将整群外星人下移，并改变他们的方向'''
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def update_aliens(ai_settings,aliens):
	'''检查是否有外星人在屏幕边缘，并更新外星人群中所有外星人的位置'''
	check_fleet_edges(ai_settings,aliens)
	aliens.update()
