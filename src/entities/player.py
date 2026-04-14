from __future__ import annotations
import pygame as pg
from .entity import Entity
from src.core.services import input_manager
from src.utils import Position, PositionCamera, GameSettings, Logger, Direction
from src.core import GameManager
import math
from typing import override

class Player(Entity):
    speed: float = 4.0 * GameSettings.TILE_SIZE
    game_manager: GameManager

    def __init__(self, x: float, y: float, game_manager: GameManager) -> None:
        super().__init__(x, y, game_manager)

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
        

        
        
        '''
        [TODO HACKATHON 4]
        Check if there is collision, if so try to make the movement smooth
        Hint #1 : use entity.py _snap_to_grid function or create a similar function
        Hint #2 : Beware of glitchy teleportation, you must do
                    1. Update X
                    2. If collide, snap to grid
                    3. Update Y
                    4. If collide, snap to grid
                  instead of update both x, y, then snap to grid
        
        if input_manager.key_down(pg.K_LEFT) or input_manager.key_down(pg.K_a):
            dis.x -= ...
        if input_manager.key_down(pg.K_RIGHT) or input_manager.key_down(pg.K_d):
            dis.x += ...
        if input_manager.key_down(pg.K_UP) or input_manager.key_down(pg.K_w):
            dis.y -= ...
        if input_manager.key_down(pg.K_DOWN) or input_manager.key_down(pg.K_s):
            dis.y += ...
        
        self.position = ...
        '''
        
        
        self.position.x += x_axis * self.speed * dt
        if self.game_manager.check_collision(pg.Rect(self.position.x, self.position.y, GameSettings.TILE_SIZE, GameSettings.TILE_SIZE)):
            self.position.x = self._snap_to_grid(self.position.x)
        self.position.y += y_axis * self.speed * dt
        if self.game_manager.check_collision(pg.Rect(self.position.x, self.position.y, GameSettings.TILE_SIZE, GameSettings.TILE_SIZE)):
            self.position.y = self._snap_to_grid(self.position.y)
        #print(self.position)

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

