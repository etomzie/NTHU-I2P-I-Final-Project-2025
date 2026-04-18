
from random import randint
import pygame as pg
from src.entities.entity import Entity
from src.sprites.sprite import Sprite
from src.utils.settings import GameSettings

class InSceneEnemy():
    def __init__(self):
        self.name = "Pikachu"
        self.max_hp = round(randint(250, 400), -1)
        self.hp = self.max_hp
        self.lvl = randint(1, 50)
        self.sprite_path = f"menu_sprites/menusprite{randint(1, 16)}.png"
        self.damage = round(randint(60, 120), -1)



        self.x = GameSettings.SCREEN_WIDTH / 5 * 3
        self.y = GameSettings.SCREEN_HEIGHT / 3 - 100


    def draw(self, screen):
        monster = Sprite(self.sprite_path)
        monster.image = pg.transform.scale_by(monster.image, 8)
        screen.blit(monster.image, (self.x, self.y))
        


