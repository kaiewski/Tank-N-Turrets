#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import time
import random
import math
import sys
from pathlib import Path

sys.path.insert(0, 'sources')

from bullet import *
from player import *
from tiles import *
from enemies import *
from screens import *
from power_up import *
from button import *
from shadows import *
from particles import *
from object_settings import *
from level_text import *

tick = 0
last_fps = 0
max_fps = 0
cent_fps = []
res_fps = 0

pygame.init()
pygame.font.init()
pygame.mixer.init(44100, 16, 2, 1024)

window_size = pygame.display.Info()

WIDTH = 1280
HEIGHT = 720
size = [WIDTH, HEIGHT]

win = pygame.display.set_mode((size), pygame.RESIZABLE)

clock = pygame.time.Clock()
game = False
main_menu = True
pause = False

FPS = 48

BG_IMAGE = pygame.image.load('images/screens/background_main.jpg')
background_image = pygame.transform.smoothscale(BG_IMAGE, (WIDTH, HEIGHT))
BG_CHOOSE_LEVEL = pygame.image.load('images/screens/select_level_screen.jpg')
choose_level_image = pygame.transform.smoothscale(BG_CHOOSE_LEVEL, (WIDTH, HEIGHT))

main_font = pygame.font.SysFont('Arial', 60)

player = Player()
bullet_buffer = []
tiles = []
power_ups = []
penetrations = []
explosions = []

cam_x, cam_y = 0, 0

random_to_image = {
	0:'damage',
	1:'heal',
	2:'speed',
	3:'grenade'
}

pygame.display.set_caption(f"|   TANK 'N' TURRETS   |")

destroy_sounds = [pygame.mixer.Sound("sounds/destroy/destroy_1.wav"), pygame.mixer.Sound("sounds/destroy/destroy_2.wav"), pygame.mixer.Sound("sounds/destroy/destroy_3.wav")]
master_volume = 0.1

for sound in destroy_sounds:
	sound.set_volume(master_volume)

def collide_on_coordinates(objects, mouse_x, mouse_y):
	if type(objects) == list:
		for obj in objects:
			if obj.rect.collidepoint((mouse_x, mouse_y)):
				return obj
	return False

def change_screen_mode(state, w, h):
	if state == 1:
		win = pygame.display.set_mode((size), pygame.FULLSCREEN)
	else:
		win = pygame.display.set_mode((w, h), pygame.RESIZABLE)
	return win

def get_reached_level():
	try:
		with open('sources/player.data', 'r+') as file:
			data = file.read()
			return data
	except FileNotFoundError:
		with open('sources/player.data', 'w+') as file:
			file.write('1')
			return 1
def set_reached_level(level):
	with open('sources/player.data', 'r+') as file:
		file.write(str(level))

def main_menu_theme(master_volume):
	pygame.mixer.music.load("music/main_theme.wav")
	pygame.mixer.music.set_volume(master_volume)
	pygame.mixer.music.play(-1)

def level_theme(master_volume):
	pygame.mixer.music.load("music/level_theme.wav")
	pygame.mixer.music.set_volume(master_volume)
	pygame.mixer.music.play(-1)

def change_level(level_info):
	if level_info[0] != []:
		all_scene_tiles = []
		[tiles, enemies, player_x, player_y] = level_info
		for tile in tiles:
			all_scene_tiles.append(tile)
		for enemie in enemies:
			all_scene_tiles.append(enemie)

		player.rect.x = player_x - WIDTH/2 + player.w/2 - 20
		player.rect.y = player_y - HEIGHT/2 + player.h/2 - 20
		player.update_gun_position()

		for tile in all_scene_tiles:
			tile.update(prev_player_x-player.rect.x, prev_player_y-player.rect.y)

		player.rect.x = WIDTH/2 + player.w/4 - 40
		player.rect.y = HEIGHT/2 + player.h/4 - 40

		player.update_gun_position()

		for tile in all_scene_tiles:
			tile.update(cam_x-WIDTH/2, cam_y-HEIGHT/2)

		return all_scene_tiles, tiles, enemies, player_x, player_y
	return [], [], [], 0, 0

def load_level(path):
	try:		
		with open(path, 'r+') as file:
			data = file.read().split('\n')
			tiles = data[0].split('|')
			rect_list = []
			enemies_list = []
			tsx, tsy = 0,0
			health = None

			for i in tiles:
				tile = i.split(' ')

				if tile[5] != 'Tank_Spawn' and not(tile[5] in enemies_to_list):
					x = int(tile[0])
					y = int(tile[1])
					width = int(tile[2])
					height = int(tile[3])
					angle = int(tile[4])
					if (obj_to_health[tile[5]] != None):
						health = int(obj_to_health[tile[5]])

					image_directory = f'images/tiles/{tile[5].lower()}.png'
					new_object = Tile(x, y, width, height, image_directory, tile[5], angle)
					new_object.health = obj_to_health[tile[5]]

					rect = pygame.Rect(x, y, width, height)
					rect_list.append(new_object)

				if tile[5] in enemies_to_list:
					if tile[5] == 'Turret':
						new_object = Enemy_Turret(int(tile[0]), int(tile[1]), obj_to_health[tile[5]], 'images', angle-90)
					if tile[5] == 'Machinegun':
						new_object = Enemy_Machinegun(int(tile[0]), int(tile[1]), obj_to_health[tile[5]], 'images', angle-90)
					if tile[5] == 'Launcher':
						new_object = Enemy_Launcher(int(tile[0]), int(tile[1]), obj_to_health[tile[5]], 'images', angle-90)
					enemies_list.append(new_object)

				if tile[5] == 'Tank_Spawn':
					tsx = int(tile[0])
					tsy = int(tile[1])

			return (rect_list, enemies_list, tsx, tsy)

	except FileNotFoundError as e:
		print(f'We have an error: {e}')
		return [], [] ,0, 0

max_level = levels_quanity("levels")
max_reached_level = get_reached_level()
level_number = 1

level_info = load_level(f'levels/level_{level_number}')
prev_player_x, prev_player_y = player.rect.x, player.rect.y
[all_scene_tiles, tiles, enemies, player_x, player_y] = change_level(level_info)

stealth_screen = Stealth_screen(WIDTH, HEIGHT)

menu_state = 0
main_screen_shadow = Main_menu_theme(WIDTH, HEIGHT, "main_menu_screen.png")

play_button = Button(273, 370, 300, 300/3.430107527, "play", "play_button.png", master_volume)
settings_button = Button(273, 477, 300, 300/5.907407407, "settings", "settings_button.png", master_volume)
leave_button = Button(273, 545, 300, 300/4.169934641, "leave", "leave_button.png", master_volume)
back_button = Button(65*1.2-65, HEIGHT-65*1.2, 65, 65, "back", "back_button.png", master_volume)
return_button = Button(273, 400, 300, 300/5.059259259, "return", "return_button.png", master_volume)

music_checkbox = Checkbox(273, 370, 50, 50/0.99375, "music_checkbox", "check_button", "music_button", 300, 300/3.133027523)
fullscreen_checkbox = Checkbox(273, 450, 50, 50/0.99375, "fullscreen_checkbox", "check_button", "fullscreen_button", 300, 300/8.64556962, 0)

settings_menu_buttons = [music_checkbox, fullscreen_checkbox, back_button]
main_menu_buttons = [play_button, settings_button, leave_button]
pause_menu_buttons = [settings_button, return_button, leave_button]
select_menu_buttons = [back_button]

if int(max_reached_level) > 4:
	max_reached_level = 4

for i in range(0, int(max_reached_level)):
	select_menu_buttons.append(Button(546+178*(i), 330, 150, 150, f"level_{i+1}", "choose_level_button.png", master_volume))

all_menus = [main_menu_buttons, settings_menu_buttons, pause_menu_buttons, select_menu_buttons]

key_g_is_down = False
grenade_throw_power = 1

if __name__ == '__main__':
	main_menu_theme(master_volume)
	while main_menu:
		prev_player_x, prev_player_y = player.rect.x, player.rect.y

		if music_checkbox.state == 1:
			pygame.mixer.music.set_volume(master_volume)
		else:
			pygame.mixer.music.set_volume(0)

		for event in pygame.event.get():
			mouse = pygame.mouse.get_pressed()	
			mouse_x, mouse_y = pygame.mouse.get_pos()	

			if event.type == pygame.QUIT:
				exit()
				sys.exit()
				main_menu = False

			if event.type == pygame.VIDEORESIZE:
				oldw, oldh = WIDTH, HEIGHT
				WIDTH, HEIGHT = pygame.display.get_surface().get_size()
				size = [WIDTH, HEIGHT]
				background_image = pygame.transform.scale(BG_IMAGE, (WIDTH, HEIGHT))
				choose_level_image = pygame.transform.smoothscale(BG_CHOOSE_LEVEL, (WIDTH, HEIGHT))

				player.rect.x = WIDTH/2 + player.w/4 - 40
				player.rect.y = HEIGHT/2 + player.h/4 - 40

				for menu in all_menus:
					for btn in menu:
						btn.update_size(WIDTH/oldw, HEIGHT/oldh)

				for menu in all_menus:
					for btn in menu:
						btn.resized = False

				ox, oy = oldw-WIDTH, oldh-HEIGHT

				for tile in all_scene_tiles:
				    tile.update(prev_player_x-player.rect.x-ox, prev_player_y-player.rect.y-oy)

				for power_up in power_ups:
					power_up.update(prev_player_x-player.rect.x-ox, prev_player_y-player.rect.y-oy)

				for text in tutorial_level_text:
					text.update(prev_player_x-player.rect.x-ox, prev_player_y-player.rect.y-oy)
					text.update_pos()

				stealth_screen.update_size(WIDTH, HEIGHT)
				main_screen_shadow.update_size(WIDTH, HEIGHT)
				player.rect.x = WIDTH/2 + player.w/4 - 40
				player.rect.y = HEIGHT/2 + player.h/4 - 40
				player.update_gun_position()

		target = collide_on_coordinates(all_menus[menu_state], mouse_x, mouse_y)

		if target:
			target.aimed = True
			for menu in all_menus:
				for btn in menu:
					if btn != target:
						btn.aimed = False

			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				if target.name == "play":
					menu_state = 3

				if 'level_' in target.name:
					level_number = target.level
					main_screen_shadow.update_size(WIDTH, HEIGHT)
					menu_state = 2

					level_info = load_level(f'levels/level_{level_number}')
					prev_player_x, prev_player_y = player.rect.x, player.rect.y
					[all_scene_tiles, tiles, enemies, player_x, player_y] = change_level(level_info)

					level_theme(master_volume)
					pygame.mixer.music.set_volume(0.05)
					game = True
					main_menu = False

				if target.name == "leave":
					exit()
					sys.exit()
					main_menu = False

				if target.name == "settings":
					menu_state = 1

				if target.name == "music_checkbox":
					if target.clicked == False:
						target.change_self_state()

				if target.name == "fullscreen_checkbox":
					if target.clicked == False:
						target.change_self_state()
						settings_button.resize()
						change_screen_mode(target.state, window_size.current_w, window_size.current_h)
						main_screen_shadow.update_size(WIDTH, HEIGHT)

				if target.name == "back":
					if menu_state == 3:
						menu_state -= 2
					else:
						menu_state -= 1
		else:
			for menu in all_menus:
				for btn in menu:
					btn.aimed = False

		for btn in all_menus[menu_state]:
			btn.update()	

		main_screen_shadow.update()
		win.blit(background_image, (0,0, WIDTH, HEIGHT))
		if menu_state == 3:
			win.blit(choose_level_image, (0,0, WIDTH, HEIGHT))

		for btn in all_menus[menu_state]:
			btn.draw(win)		
		
		main_screen_shadow.draw(win)

		pygame.display.flip()
		clock.tick(FPS)

	while game:
		while not(pause):
			start_time = time.time()
			new_bullet_buffer = []
			visible_tiles = []
			shadows = []
			new_pens = [] 
			new_explosions = []
			grenades = []
			new_power_ups = power_ups
			prev_player_x, prev_player_y = player.rect.x, player.rect.y
			pygame.mouse.set_visible(False)

			for event in pygame.event.get():
				key = pygame.key.get_pressed()
				mouse = pygame.mouse.get_pressed()
				mouse_move = pygame.mouse.get_rel() 
				mouse_x, mouse_y = pygame.mouse.get_pos()

				if event.type == pygame.QUIT:
					exit()
					sys.exit()
					game = False

				if event.type == pygame.VIDEORESIZE:
					oldw, oldh = WIDTH, HEIGHT
					WIDTH, HEIGHT = pygame.display.get_surface().get_size()
					size = [WIDTH, HEIGHT]
					background_image = pygame.transform.scale(BG_IMAGE, (WIDTH, HEIGHT))
					choose_level_image = pygame.transform.smoothscale(BG_CHOOSE_LEVEL, (WIDTH, HEIGHT))

					ox, oy = oldw-WIDTH, oldh-HEIGHT

					for tile in all_scene_tiles:
					    tile.update(prev_player_x-player.rect.x-ox, prev_player_y-player.rect.y-oy)

					for power_up in power_ups:
						power_up.update(prev_player_x-player.rect.x-ox, prev_player_y-player.rect.y-oy)

					for text in tutorial_level_text:
						text.update(prev_player_x-player.rect.x-ox, prev_player_y-player.rect.y-oy)
						text.update_pos()

					stealth_screen.update_size(WIDTH, HEIGHT)
					player.rect.x = WIDTH/2 + player.w/4 - 40
					player.rect.y = HEIGHT/2 + player.h/4 - 40
					player.update_gun_position()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						player.left = True
						player.direction = 'left'
					if event.key == pygame.K_RIGHT:
						player.right = True
						player.direction = 'right'
					if event.key == pygame.K_UP:
						player.up = True
						player.direction = 'up'
					if event.key == pygame.K_DOWN:
						player.down = True
						player.direction = 'down'
					if event.key == pygame.K_g:
						key_g_is_down = True
						grenade_throw_power = 1

				if event.type == pygame.KEYUP:
					if event.key == pygame.K_LEFT:
						player.left = False
					if event.key == pygame.K_RIGHT:
						player.right = False
					if event.key == pygame.K_UP:
						player.up = False
					if event.key == pygame.K_DOWN:
						player.down = False
					if event.key == pygame.K_ESCAPE:
						pause = True
						main_screen_shadow.update_size(WIDTH, HEIGHT)
					if event.key == pygame.K_g:
						key_g_is_down = False
						player.throw_grenade(grenade_throw_power)

				if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
					bullet = Bullet(0,0,3,3, player.damage)
					bullet.shoot(player)
					bullet_buffer.append(bullet)
					player.shoot_sounds[random.randrange(0,3)].play()

			player.check_collision(power_ups)
			player.update(all_scene_tiles)
			dplayer_x, dplayer_y = prev_player_x-player.rect.x, prev_player_y-player.rect.y

			if key_g_is_down and grenade_throw_power < 10:
				grenade_throw_power += 0.3

			for tile in all_scene_tiles:
				tile.check_visibility(WIDTH, HEIGHT)

			visible_tiles = [tile for tile in all_scene_tiles if tile.visibility]

			if player.health <= 0:
				level_info = load_level(f'levels/level_{level_number}')
				[all_scene_tiles, tiles, enemies, player_x, player_y] = change_level(level_info)
				power_ups = []
				new_power_ups = []
				player.power_ups = []
				new_bullet_buffer = []
				bullet_buffer = []
				grenades = []
				player.grenades = []
				player.grenade_quanity = 1
				main_screen_shadow.update_size(WIDTH, HEIGHT)

				for text in tutorial_level_text:
					text.x = text.normal_x
					text.y = text.normal_y

				player.health = player.max_health

			if player.can_ride:
				for tile in all_scene_tiles:
					tile.update(dplayer_x, dplayer_y)

				for enemie in enemies:
					enemie.update_rotate(player)

				for power_up in power_ups:
					power_up.update(dplayer_x, dplayer_y)

				if player.on_finish_line:
					if player.grenade_quanity < 3:
						player.grenade_quanity += 1
					level_number += 1
					level_info = load_level(f'levels/level_{level_number}')
					[all_scene_tiles, tiles, enemies, player_x, player_y] = change_level(level_info)
					power_ups = []
					new_power_ups = []
					new_bullet_buffer = []
					bullet_buffer = []
					grenades = []
					player.rect.x = WIDTH/2 + player.w/4 - 40
					player.rect.y = HEIGHT/2 + player.h/4 - 40
					player.update_gun_position()
					player.on_finish_line = False
					set_reached_level(level_number)
					main_screen_shadow.update_size(WIDTH, HEIGHT)
					player.health = player.max_health
				player.update_position()

			for tile in all_scene_tiles:
				if tile.health != None and tile.health <= 0:
					local_ground = check_local_ground(visible_tiles, pygame.Rect(tile.rect.x-tile.rect.w, tile.rect.y-tile.rect.h, tile.rect.w*3, tile.rect.h*3))
					new_tile_object = Tile(tile.rect.x, tile.rect.y, 64, 64, f'images/tiles/{local_ground.lower()}.png', local_ground)
					destroy_sounds[random.randrange(0,3)].play()
					explosion = Explosion(tile.rect.centerx, tile.rect.centery, 32, 32)
					explosions.append(explosion)
					
					if tile.tile_name == "Ammo_Box":
						random_power_up = random.randrange(0, 4)
						power_ups.append(Power_up(new_tile_object.rect.centerx-24, new_tile_object.rect.centery-34, 48, 48, f'images/tiles/power_ups/{random_to_image[random_power_up]}.png', f'{random_to_image[random_power_up]}'))
					
					if tile.tile_name == 'Box' and random.randrange(0, 100) > 85:
						random_power_up = random.randrange(0, 4)
						power_ups.append(Power_up(new_tile_object.rect.centerx-24, new_tile_object.rect.centery-34, 48, 48, f'images/tiles/power_ups/{random_to_image[random_power_up]}.png', f'{random_to_image[random_power_up]}'))
					all_scene_tiles[all_scene_tiles.index(tile)] = new_tile_object

			for enemie in enemies:
				res = enemie.shoot()
				if res != None:
					if isinstance(res, list):
						for i in res:
							bullet_buffer.append(i)
					else:
						bullet_buffer.append(i)

			for bullet in bullet_buffer:
				if bullet.flight:
					new_bullet_buffer.append(bullet)
				else:
					penetrations.append(bullet.penetration)

			bullet_buffer = new_bullet_buffer

			for bullet in bullet_buffer:
				bullet.check_collision(visible_tiles)
				bullet.check_collision([player])
				bullet.update(dplayer_x, dplayer_y)

			for power_up in power_ups:
				if power_up.delete_me:
					del new_power_ups[new_power_ups.index(power_up)]
			power_ups = new_power_ups

			for up in player.power_ups:
				up.update_timer(FPS)

			for pen in penetrations:
				pen.update(dplayer_x, dplayer_y)
				if pen.tick > 0:
					new_pens.append(pen)

			for grenade in player.grenades:
				grenade.update(dplayer_x, dplayer_y)
				if not(grenade._explode):
					grenades.append(grenade)
				else:
					grenade.explode(visible_tiles, destructible_objects)
					destroy_sounds[random.randrange(0,3)].play()
					explosion = Explosion(grenade.rect.centerx, grenade.rect.centery, 32, 32)
					explosions.append(explosion)

			for explosion in explosions:
				explosion.update(dplayer_x, dplayer_y)
				if explosion.tick > 0:
					new_explosions.append(explosion)

			player.grenades = grenades

			penetrations = new_pens
			explosions = new_explosions

			if level_number == 1:
				for text in tutorial_level_text:
					text.update(dplayer_x, dplayer_y)

			stealth_screen.update()
			main_screen_shadow.update()
			win.fill((255,70,20))

			for tile in visible_tiles:
				if tile.tile_name in non_shadow_objects:
					tile.draw(win)

			for tile in visible_tiles:
				if not(tile.tile_name in non_shadow_objects):
					new_shadow = Shadow(tile.rect.x, tile.rect.y+tile.rect.h-2, tile.rect.w, tile.rect.h/4, (0,0,0,64))
					shadows.append(new_shadow)

			player.draw(win)

			for shadow in shadows:
				shadow.draw(win)
			
			for tile in visible_tiles:
				if tile.tile_name != "Bush" and not(tile.tile_name in non_shadow_objects):
					tile.draw(win)

			for bullet in bullet_buffer:
				bullet.draw(win)
	 
			for power_up in power_ups:
				power_up.draw(win)

			for tile in visible_tiles:
				if tile.tile_name == "Bush":
					tile.draw(win)

			for pen in penetrations:
				pen.draw(win)

			for explosion in explosions:
				explosion.draw(win)

			if player.down_block == "Bush":
				stealth_screen.on_screen = True
			elif player.down_block != "Bush":
				stealth_screen.on_screen = False

			for grenade in player.grenades:
				grenade.draw(win)

			if level_number == 1:
				for text in tutorial_level_text:
					text.draw(win)

			if level_number == 5:
				info_surface = main_font.render(("Thank You for playing! :)"), True, (255,255,255))
				win.blit(info_surface, (WIDTH/2, HEIGHT-100))
			
			stealth_screen.draw(win)
			main_screen_shadow.draw(win)

			win.blit(player.health_bar, (10, HEIGHT-player.health_bar.get_height()-10, 250, 30))
			pygame.draw.rect(win, (255,90,60), (15, HEIGHT-46, (player.health / player.max_health) * 250, 28))
			info_surface = player.font.render(f'{player.health}/{player.max_health}', True, (255,255,255))
			win.blit((info_surface), (18, HEIGHT-46, 250/2, 30))

			for up in player.power_ups:
				win.blit(up.image, (117+player.power_ups.index(up)*up.rect.w, HEIGHT-100, up.rect.w, up.rect.h))
				info_surface = up.font.render(f'{int(up.up_timer)}', True, (255,255,255))
				win.blit((info_surface), (117+player.power_ups.index(up)*up.rect.w, HEIGHT-100, up.rect.w, up.rect.h))

			win.blit(player.grenade_image, (16, HEIGHT-156, 32, 32))
			info_surface = player.font.render(f'x{player.grenade_quanity}', True, (255,255,255))
			win.blit((info_surface), (48, HEIGHT-140, 32, 32))

			if key_g_is_down and player.grenade_quanity > 0:
				pygame.draw.rect(win, (255,0,0), (75, HEIGHT-player.health_bar.get_height()-15-grenade_throw_power*10, 35, grenade_throw_power*10))
				win.blit(player.grenade_indicator, (75, HEIGHT-player.health_bar.get_height()-115))

			pygame.display.flip()
			clock.tick(FPS)

		while pause:
			pygame.mouse.set_visible(True)
			pygame.mixer.music.set_volume(master_volume)
			mouse_x, mouse_y = pygame.mouse.get_pos()	

			if music_checkbox.state == 1:
				pygame.mixer.music.set_volume(master_volume)
			else:
				pygame.mixer.music.set_volume(0)
				
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
					sys.exit()
					game = False

				if event.type == pygame.VIDEORESIZE:
					oldw, oldh = WIDTH, HEIGHT
					WIDTH, HEIGHT = pygame.display.get_surface().get_size()
					size = [WIDTH, HEIGHT]
					background_image = pygame.transform.scale(BG_IMAGE, (WIDTH, HEIGHT))
					choose_level_image = pygame.transform.smoothscale(BG_CHOOSE_LEVEL, (WIDTH, HEIGHT))

					player.rect.x = WIDTH/2 + player.w/4 - 40
					player.rect.y = HEIGHT/2 + player.h/4 - 40

					for menu in all_menus:
						for btn in menu:
							btn.update_size(WIDTH/oldw, HEIGHT/oldh)

					ox, oy = oldw-WIDTH, oldh-HEIGHT

					for tile in all_scene_tiles:
					    tile.update(prev_player_x-player.rect.x-ox, prev_player_y-player.rect.y-oy)

					for power_up in power_ups:
						power_up.update(prev_player_x-player.rect.x-ox, prev_player_y-player.rect.y-oy)

					for text in tutorial_level_text:
						text.update(prev_player_x-player.rect.x-ox, prev_player_y-player.rect.y-oy)
						text.update_pos()

					stealth_screen.update_size(WIDTH, HEIGHT)
					main_screen_shadow.update_size(WIDTH, HEIGHT)
					player.rect.x = WIDTH/2 + player.w/4 - 40
					player.rect.y = HEIGHT/2 + player.h/4 - 40
					player.update_gun_position()

			target = collide_on_coordinates(all_menus[menu_state], mouse_x, mouse_y)
			if target:
				target.aimed = True
				for menu in all_menus:
					for btn in menu:
						if btn != target:
							btn.aimed = False

				if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					if target.name == "return":
						menu_state = 2
						pause = False

					if target.name == "settings":
						menu_state = 1

					if target.name == "leave":
						exit()
						sys.exit()
						main_menu = False

					if target.name == "music_checkbox":
						if target.clicked == False:
							target.change_self_state()

					if target.name == "fullscreen_checkbox":
						if target.clicked == False:
							target.change_self_state()
							settings_button.resize()
							change_screen_mode(target.state, window_size.current_w, window_size.current_h)
							main_screen_shadow.update_size(WIDTH, HEIGHT)

					if target.name == "back":
						menu_state = 2

			else:
				for menu in all_menus:
					for btn in menu:
						btn.aimed = False

			for btn in all_menus[menu_state]:
				btn.update()

			main_screen_shadow.update()
			win.blit(background_image, (0,0, WIDTH, HEIGHT))
			
			for btn in all_menus[menu_state]:
				btn.draw(win)
			main_screen_shadow.draw(win)
			pygame.display.flip()
			clock.tick(FPS)