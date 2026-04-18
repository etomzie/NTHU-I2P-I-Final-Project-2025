import pygame as pg

from src.utils import GameSettings, Logger
from src.sprites import BackgroundSprite
from src.scenes.scene import Scene
from src.interface.components import Button
from src.core.services import scene_manager, sound_manager, input_manager
from typing import override
from src.sprites import Sprite, Animation
from src.core.managers.game_manager import GameManager
from src.data.bag import Bag
from src.entities.in_scene_enemy import InSceneEnemy

class BushScene(Scene):
    def __init__(self, ):
        super().__init__()
        self.background = BackgroundSprite("backgrounds/background1.png")
        manager = GameManager.load("saves/game0.json") 
        if manager is None:
            Logger.error("Failed to load game manager")
            exit(1)
        self.game_manager = manager
        
        dist = 100 + 15
        self.fight_button = Button(
            "UI/raw/UI_Flat_Button01a_4.png", "UI/raw/UI_Flat_Button01a_2.png",
            GameSettings.SCREEN_WIDTH // 2 - 250, GameSettings.SCREEN_HEIGHT - 70, 100, 35,
            lambda: self.fight_loop()
        )
        self.item_button = Button(
            "UI/raw/UI_Flat_Button01a_4.png", "UI/raw/UI_Flat_Button01a_2.png",
            GameSettings.SCREEN_WIDTH // 2 - 250 + dist * 1, GameSettings.SCREEN_HEIGHT - 70, 100, 35,
            lambda: self.bag_open()
        )
        self.switch_button = Button(
            "UI/raw/UI_Flat_Button01a_4.png", "UI/raw/UI_Flat_Button01a_2.png",
            GameSettings.SCREEN_WIDTH // 2 - 250 + dist * 2, GameSettings.SCREEN_HEIGHT - 70, 100, 35,
            lambda: self.switch_monster()
        )
        self.run_button = Button(
            "UI/raw/UI_Flat_Button01a_4.png", "UI/raw/UI_Flat_Button01a_2.png",
            GameSettings.SCREEN_WIDTH // 2 - 250 + dist * 3, GameSettings.SCREEN_HEIGHT - 70, 100, 35,
            lambda: self.return_to_game()
        )
        

        

        
        self.fight_started = True
        self.current_monster_index = 0
        
        self.curr_state = 'playing'
        
        self.switch_monster_buttons = []
        self.monster_data = self.game_manager.bag._monsters_data

        dist = 10 + 50  
        for i, now in enumerate(self.monster_data):
            self.switch_monster_buttons.append(Button(
                "UI/raw/UI_Flat_Button01a_4.png", "UI/raw/UI_Flat_Button01a_2.png",
                GameSettings.SCREEN_WIDTH / 2 - 50, GameSettings.SCREEN_HEIGHT / 4 + dist * i, 100, 50,
                lambda i = i: self.switch_monster_to_index(i)
            ))        

        
        self.faint_txt = False

        
    
    def return_to_game(self):
        # TODO sync bag
        #scene_manager._current_scene.game_manager.save("saves/game0.json") 
        


        scene_manager.change_scene('game')


    def fight_loop(self,):
        if self.faint_txt:
            return
        
        self.enemy.hp = max(0,  self.enemy.hp - self.monster_data[self.current_monster_index]["damage"])
        if self.enemy.hp == 0:
            self.return_to_game()
            return      
        
        self.monster_data[self.current_monster_index]["hp"] = max(0, self.monster_data[self.current_monster_index]["hp"] -self.enemy.damage)
        if self.monster_data[self.current_monster_index]["hp"] == 0:
            self.faint_txt = True
            self.switch_monster()
            
        



        

        
    
    def bag_open(self):
        self.curr_state  = 'bag'
    
    def bag_close(self):
        self.curr_state = "playing"
        
    def switch_monster(self):
        self.curr_state = 'switch'
    
    def switch_monster_to_index(self, index):
        if self.monster_data[index]["hp"] <= 0:
            return
        self.current_monster_index = index
        self.curr_state = 'playing'
        self.faint_txt = False
        
        
        
    @override
    def enter(self) -> None:
        sound_manager.play_bgm("RBY 107 Battle! (Trainer).ogg")
        self.enemy = InSceneEnemy()
        # [TODO] make animation
        pass

    @override
    def exit(self) -> None:
        
        pass

    @override
    def update(self, dt: float) -> None:
        self.fight_button.update(dt)
        self.item_button.update(dt)
        self.switch_button.update(dt)
        self.run_button.update(dt)
        
        self.game_manager.bag.update(dt)
        for now in self.switch_monster_buttons:
            now.update(dt)

    
    def draw_monster(self, screen, start_x, start_y, monster_data):
        #offset = 55 + 3 # bg height + distance

        offset = 0
        # bg
        monster_bg = Sprite("UI/raw/UI_Flat_Banner03a.png")
        monster_bg.image = pg.transform.scale(monster_bg.image, (250, 55))
        screen.blit(monster_bg.image, (start_x, start_y + offset ))
        
        # image
        monster = Sprite(monster_data["sprite_path"])
        monster.image = pg.transform.scale_by(monster.image, 1.5 )
        screen.blit(monster.image, (start_x + 14, start_y + offset - monster.rect.height + 55 / 2 + 2))
        
        # name
        monster_font = pg.font.Font("assets/fonts/Minecraft.ttf", 10,)
        monster_font.set_bold(True)
        monster_text = monster_font.render(monster_data["name"], False, (0, 0 ,0))
        screen.blit(monster_text, (start_x + 14 + monster.rect.width + 19, start_y + offset  + 10))
        
        # hp bar
        bar_WIDTH = 140
        bar_HEIGT = 11
        pg.draw.rect(screen, (0, 0, 0), 
                        (start_x + 14 + monster.rect.width + 19, start_y + offset  + 10 + 12, bar_WIDTH, bar_HEIGT)
                        )
        pg.draw.rect(screen, (98, 174, 98), 
                        (start_x + 14 + monster.rect.width + 19, start_y + offset  + 10 + 12, 
                        monster_data["hp"] / monster_data["max_hp"] * bar_WIDTH, bar_HEIGT)
                        )

        # level
        level_text = monster_font.render(f"Lv{monster_data["level"]}", False, (0, 0, 0))
        screen.blit(level_text, 
                    (start_x + 14 + monster.rect.width + 19 + bar_WIDTH + 7,
                        start_y + offset  + 10 + 12
                    ))
        
        # hp text
        monster_hp_font = pg.font.Font("assets/fonts/Minecraft.ttf", 8,)
        monster_hp_font.set_bold(True)
        monster_hp_text = monster_hp_font.render(f"{monster_data["hp"]} / {monster_data["max_hp"]}", False, (0, 0, 0))
        screen.blit(monster_hp_text, (start_x + 14 + monster.rect.width + 19, start_y + offset  + 35))

    @override
    def draw(self, screen: pg.Surface) -> None:
        self.background.draw(screen)
        
        monster_bg = Sprite("UI/raw/UI_Flat_Banner03a.png")
        monster_bg.image = pg.transform.scale(monster_bg.image, (250, 55))
        
        bar_WIDTH = GameSettings.SCREEN_WIDTH
        bar_HEIGT = 135
        
        
        border_WIDTH = 1.5
        pg.draw.rect(screen, (176, 177, 166), 
                        (0, GameSettings.SCREEN_HEIGHT - bar_HEIGT, bar_WIDTH, bar_HEIGT)
                        )
        pg.draw.rect(screen, (0, 0, 0), 
                        (border_WIDTH, GameSettings.SCREEN_HEIGHT - bar_HEIGT + border_WIDTH, 
                         bar_WIDTH - border_WIDTH * 2, bar_HEIGT - border_WIDTH * 2)
                        )
        
        if self.fight_started:
            current_monster = self.monster_data[self.current_monster_index]
            #print(my_monsters)
            pg.font.init()
            fnt = pg.font.Font("assets/fonts/Minecraft.ttf", 15)

            if self.faint_txt:
                txt = fnt.render(f'{self.monster_data[self.current_monster_index]["name"]} has fainted!', False, (255, 255, 255))
            else:
                txt = fnt.render(f'What will {current_monster['name']} do?', False, (255, 255, 255))
            screen.blit(txt, (15, GameSettings.SCREEN_HEIGHT - bar_HEIGT + 15))
            
            # my monster
            start_x = 15
            start_y = GameSettings.SCREEN_HEIGHT - 65 - bar_HEIGT
            self.draw_monster(screen, start_x, start_y, current_monster)
            
            # enemy monster
            start_x = GameSettings.SCREEN_WIDTH - 275
            start_y = 25

            self.draw_monster(screen ,start_x, start_y, {"name": self.enemy.name,
                                                         "max_hp": self.enemy.max_hp,
                                                         "hp": self.enemy.hp,
                                                         "level": self.enemy.lvl,
                                                         "sprite_path": self.enemy.sprite_path
                                                         })
            
            self.fight_button.draw(screen)
            self.item_button.draw(screen)
            self.switch_button.draw(screen)
            self.run_button.draw(screen)
            
            s_x = GameSettings.SCREEN_WIDTH // 2 - 250 + 25
            s_y = GameSettings.SCREEN_HEIGHT - 70 + 10
            dist = 100 + 15
            for i, now in enumerate([' Fight', ' Items', 'Switch', '  Run']):
                txt = fnt.render(now, False, (0, 0, 0))
                screen.blit(txt, (s_x + dist * i, s_y))
  
            monster = Sprite(current_monster["sprite_path"])
            monster.image = pg.transform.scale_by(monster.image, 8)
            monster.image = pg.transform.flip(monster.image, True, False)
            screen.blit(monster.image, (GameSettings.SCREEN_WIDTH / 4, GameSettings.SCREEN_HEIGHT / 2 - 100))
            
            self.enemy.draw(screen)
                
        if self.curr_state == 'bag':
            self.game_manager.bag.draw(screen)
        elif self.curr_state == 'switch':
            bag_WIDTH = GameSettings.SCREEN_WIDTH / 4 + 50
            bag_HEIGHT = GameSettings.SCREEN_HEIGHT * 4 / 7
            bag_bg = Sprite("UI/raw/UI_Flat_FrameSlot03a.png", (bag_WIDTH, bag_HEIGHT))
            screen.blit(bag_bg.image, pg.Rect(GameSettings.SCREEN_WIDTH / 2 - bag_WIDTH / 2, 
                                              GameSettings.SCREEN_HEIGHT / 2 - bag_HEIGHT / 2,
                                              bag_WIDTH,
                                              bag_HEIGHT)) 
            
            for i, now in enumerate(self.switch_monster_buttons):
                now.draw(screen)  
                
            dist = 50 + 10
            s_x = GameSettings.SCREEN_WIDTH / 2 - 50 + 10
            s_y = GameSettings.SCREEN_HEIGHT / 4 + 15
            fnt = pg.font.Font("assets/fonts/Minecraft.ttf", 15)
            for i, now in enumerate(self.monster_data):

                txt = fnt.render(now['name'], False, (0, 0 ,0))
                screen.blit(txt, (s_x, s_y + dist * i))
        

            
            

        
        
        

        