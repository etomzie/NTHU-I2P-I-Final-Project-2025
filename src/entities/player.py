from __future__ import annotations
import pygame as pg
from .entity import Entity
from src.core.services import input_manager
from src.utils import Position, PositionCamera, GameSettings, Logger, Direction
from src.core import GameManager
import math
from typing import override

from src.core.services import scene_manager



import json

class Player(Entity):
    speed: float = 4.0 * GameSettings.TILE_SIZE
    game_manager: GameManager

    def __init__(self, x: float, y: float, game_manager: GameManager) -> None:
        super().__init__(x, y, game_manager)

        self.bushes = self.current_bushes()

    def current_bushes(self):
        with open("saves/game0.json", "r") as f:
            data = json.load(f)

        bushes = set()

        for raw in data["map"]:
            if not raw["bushes"]: continue
            for now in raw["bushes"]:
                
                bushes.add((now["x"], now["y"]))

        return bushes

    @override
    def update(self, dt: float) -> None:
        dis = Position(0, 0)
        '''
        [TODO HACKATHON 2]
        Calculate the distance change, and then normalize the distance
        '''
        x_axis = 0
        y_axis = 0
        
        
        if input_manager.key_down(pg.K_UP) or input_manager.key_down(pg.K_w):
            self.animation.switch('up')
            y_axis -= 1
        if input_manager.key_down(pg.K_DOWN) or input_manager.key_down(pg.K_s):
            self.animation.switch('down')
            y_axis += 1
        if input_manager.key_down(pg.K_LEFT) or input_manager.key_down(pg.K_a):
            self.animation.switch('left')
            x_axis -= 1
        if input_manager.key_down(pg.K_RIGHT) or input_manager.key_down(pg.K_d):
            self.animation.switch('right')
            x_axis += 1


        
        
        mag = math.sqrt(x_axis ** 2 + y_axis ** 2)
        if mag != 0:
            x_axis /= mag
            y_axis /= mag
        
        
        
        self.position.x += x_axis * self.speed * dt
        if self.game_manager.check_collision(pg.Rect(self.position.x, self.position.y, GameSettings.TILE_SIZE, GameSettings.TILE_SIZE)):
            self.position.x = self._snap_to_grid(self.position.x)
        self.position.y += y_axis * self.speed * dt
        if self.game_manager.check_collision(pg.Rect(self.position.x, self.position.y, GameSettings.TILE_SIZE, GameSettings.TILE_SIZE)):
            self.position.y = self._snap_to_grid(self.position.y)
        
        if (self.position.x // GameSettings.TILE_SIZE, self.position.y // GameSettings.TILE_SIZE) in self.bushes:

            if input_manager.key_down(pg.K_SPACE):
                scene_manager.change_scene("bush")
                
                



        # Check teleportation
        tp = self.game_manager.current_map.check_teleport(self.position)
        if tp:
            #self.position = tp.pos
            dest = tp.destination
            
            print(tp.pos.x, tp.pos.y, self.position.x, self.position.y)

            self.game_manager.switch_map(dest)
            #self.position = tp.pos

            print(tp.pos.x, tp.pos.y, self.position.x, self.position.y)

            
                
        super().update(dt)
            
            

    @override
    def draw(self, screen: pg.Surface, camera: PositionCamera) -> None:
        super().draw(screen, camera)
        
    @override
    def to_dict(self) -> dict[str, object]:
        return super().to_dict()
    
    @classmethod
    @override
    def from_dict(cls, data: dict[str, object], game_manager: GameManager) -> Player:
        return cls(data["x"] * GameSettings.TILE_SIZE, data["y"] * GameSettings.TILE_SIZE, game_manager)

