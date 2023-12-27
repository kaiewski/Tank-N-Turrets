#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tiles import *
from pathlib import Path
from level_text import *

non_collision_objects = ['Ground', 'Bush', 'Water', 'Finish', 'Power-up', 'Rocks', 'Asphalt', 'Barricade_Falled', 'Manhole', 'Mine']
non_full_objects = ["Bush", "Tank_Spawn", "Turret", "Machinegun", "Launcher", "Finish", "Rocks", "Barricade", "Barricade_Falled", "Mine", "Manhole"]
non_shadow_objects = ["Tank_Spawn", "Static Turret", "Turret", "Machine gun", "Machinegun", "Launcher", "Finish", "Ground", "Water", "Rocks", "Asphalt", "Barricade", "Barricade_Falled", "Mine", "Manhole"]
destructible_objects = ["Static Turret", "Machine gun", "Launcher", "Rocks", "Barricade", "Barricade_Falled", "Mine", "Brick", "Box", "Ammo_Box"]

obj_to_health = { 	
				'Ground':None,
				'Water':None,
				'Bush':100,
				'Wall':None,
				'Box':100,
				'Ammo_Box':200,
				'Brick':300,
				'Tank_Spawn':None,
				'Turret':500,
				'Machinegun':300,
				'Launcher':600,
				'Finish':None,
				'Rocks':None,
				'Asphalt':None,
				'Barricade':50,
				'Barricade_Falled':None,
				'Mine':50,
				'Manhole':None,
				}

enemies_to_list = {'Turret','Machinegun','Launcher'}
enemies_list = ['Turret','Machinegun','Launcher']

tutorial_level_text = [
					Level_text(640,0,20, "Press ← ↑ → ↓ to move"),
					Level_text(640,640,20, "Press the SPACEBAR to fire"),
					Level_text(1300,480,20, "Destroy the Enemy Turret"),
					Level_text(1700,640,20, "Amplifiers fall out of boxes"),
					Level_text(1700,0,20, "Press and hold the G key to throw a grenade"),
					Level_text(2430,150,20, "The bushes will help you hide from the enemies"),
					Level_text(3700,200,20, "Your mission is to get to the finish line"),
					]
					
def check_local_ground(objects, rect):
	ground_list = {"Ground": 0, "Asphalt":0}
	for obj in objects:
		if rect.collidepoint((obj.rect.x, obj.rect.y)) and obj.tile_name in ground_list:
			ground_list[obj.tile_name] += 1
	if (ground_list["Ground"] > ground_list["Asphalt"]):
		return "Ground"
	return "Asphalt"

def levels_quanity(path):
	folder = Path(path)
	return len(list(folder.iterdir()))
