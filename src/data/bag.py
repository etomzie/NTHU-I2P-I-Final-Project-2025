import pygame as pg
import json
from src.interface.components.button import Button
from src.utils import GameSettings
from src.utils.definition import Monster, Item
from src.core.services import scene_manager
from src.sprites import Sprite



class Bag:
    _monsters_data: list[Monster]
    _items_data: list[Item]

    def __init__(self, monsters_data: list[Monster] | None = None, items_data: list[Item] | None = None):
        self._monsters_data = monsters_data if monsters_data else []
        self._items_data = items_data if items_data else []
        
        self.back_button = Button(
            "UI/button_x.png", "UI/button_x_hover.png",
            GameSettings.SCREEN_WIDTH // 2 + 230, 130, 40, 40,
            lambda: scene_manager._current_scene.bag_close()
        )
        
        

    def update(self, dt: float):
        self.back_button.update(dt)

    def draw(self, screen: pg.Surface):
        WIDTH = GameSettings.SCREEN_WIDTH
        HEIGHT = GameSettings.SCREEN_HEIGHT
        
        # screen Fade
        game_over_screen_fade = screen.copy()
        game_over_screen_fade.fill((0, 0, 0))
        game_over_screen_fade.set_alpha(160)
        screen.blit(game_over_screen_fade, (0, 0))
        # bag BG
        bag_WIDTH = WIDTH // 2
        bag_HEIGHT = HEIGHT * 4 // 5.5
        bag_bg = Sprite("UI/raw/UI_Flat_FrameSlot03a.png", (bag_WIDTH, bag_HEIGHT))
        screen.blit(bag_bg.image, pg.Rect(WIDTH // 2 - bag_WIDTH / 2, HEIGHT // 2 - bag_HEIGHT / 2, bag_WIDTH, bag_HEIGHT))
        # text
        pg.font.init()
        bag_font = pg.font.Font("assets/fonts/Minecraft.ttf", 28)
        bag_text = bag_font.render('BAG', False, (0, 0, 0))
        screen.blit(bag_text, (WIDTH // 2 - bag_WIDTH / 2 + 50, HEIGHT // 2 - bag_HEIGHT / 2 + 45))
        
        
        # bag monsters
        start_x = WIDTH // 2 - bag_WIDTH / 2 + 55
        start_y = HEIGHT // 2 - bag_HEIGHT / 2 + 80
        offset = 55 + 3 # bg height + distance
        for i, monster_data in enumerate(self._monsters_data):
            # bg
            monster_bg = Sprite("UI/raw/UI_Flat_Banner03a.png")
            monster_bg.image = pg.transform.scale(monster_bg.image, (250, 55))
            screen.blit(monster_bg.image, (start_x, start_y + offset * i))
            
            # image
            monster = Sprite(monster_data["sprite_path"])
            monster.image = pg.transform.scale_by(monster.image, 1.5 )
            screen.blit(monster.image, (start_x + 14, start_y + offset * i - monster.rect.height + 55 / 2 + 2))
            
            # name
            monster_font = pg.font.Font("assets/fonts/Minecraft.ttf", 10,)
            monster_font.set_bold(True)
            monster_text = monster_font.render(monster_data["name"], False, (0, 0 ,0))
            screen.blit(monster_text, (start_x + 14 + monster.rect.width + 19, start_y + offset * i + 10))
            
            # hp bar
            bar_WIDTH = 140
            bar_HEIGT = 11
            pg.draw.rect(screen, (0, 0, 0), 
                         (start_x + 14 + monster.rect.width + 19, start_y + offset * i + 10 + 12, bar_WIDTH, bar_HEIGT)
                         )
            pg.draw.rect(screen, (98, 174, 98), 
                          (start_x + 14 + monster.rect.width + 19, start_y + offset * i + 10 + 12, 
                           monster_data["hp"] / monster_data["max_hp"] * bar_WIDTH, bar_HEIGT)
                         )

            # level
            level_text = monster_font.render(f"Lv{monster_data["level"]}", False, (0, 0, 0))
            screen.blit(level_text, 
                        (start_x + 14 + monster.rect.width + 19 + bar_WIDTH + 7,
                         start_y + offset * i + 10 + 12
                        ))
            
            # hp text
            monster_hp_font = pg.font.Font("assets/fonts/Minecraft.ttf", 8,)
            monster_hp_font.set_bold(True)
            monster_hp_text = monster_hp_font.render(f"{monster_data["hp"]} / {monster_data["max_hp"]}", False, (0, 0, 0))
            screen.blit(monster_hp_text, (start_x + 14 + monster.rect.width + 19, start_y + offset * i + 35))
        
        # bag items
        start_x = WIDTH // 2 + 70
        start_y = HEIGHT // 4 + 20
        offset = 40
        for i, item_data in enumerate(self._items_data):
            item = Sprite(item_data["sprite_path"])
            item.image = pg.transform.scale_by(item.image, 1.8)
            screen.blit(item.image, (start_x, start_y + offset * i))
            
            # text
            item_font = pg.font.Font("assets/fonts/Minecraft.ttf", 10,)
            item_font.set_bold(True)
            item_text = item_font.render(item_data["name"], False, (0, 0 ,0))
            screen.blit(item_text, (start_x + item.rect.width * 2, start_y + offset * i))
            
            item_count = item_font.render(f"x{item_data["count"]}", False, (0, 0, 0))
            screen.blit(item_count, (start_x + item.rect.width * 6, start_y + offset * i + 10))
            
            
            
            
            
            
            
            
            
            
        
        
        
        
        #print(self._monsters_data)
        #print(self._items_data)
        self.back_button.draw(screen)
        
        

    def to_dict(self) -> dict[str, object]:
        return {
            "monsters": list(self._monsters_data),
            "items": list(self._items_data)
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Bag":
        monsters = data.get("monsters") or []
        items = data.get("items") or []
        bag = cls(monsters, items)
        return bag