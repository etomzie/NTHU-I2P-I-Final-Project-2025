import pygame as pg

from src.utils import GameSettings
from src.sprites import BackgroundSprite
from src.scenes.scene import Scene
from src.interface.components import Button
from src.core.services import scene_manager, sound_manager, input_manager
from typing import override
from src.sprites import Sprite
from src.utils.settings import GameSettings





class inGameSetting(Scene):    
    def __init__(self):
        super().__init__()
        px, py = GameSettings.SCREEN_WIDTH // 2, GameSettings.SCREEN_HEIGHT * 3 // 4
        self.return_button = Button(
            "UI/button_x.png", "UI/button_x_hover.png",
            GameSettings.SCREEN_WIDTH * 3 // 4 - 75, GameSettings.SCREEN_HEIGHT // 5 - 10, 30, 30,
            lambda: scene_manager._current_scene.bag_close()
        )
        
        self.state_muted = 0
        
        self.mn_slider_x = 375
        self.mx_slider_x = GameSettings.SCREEN_WIDTH // 2 - 100 + 375
        self.vol_slider_hold = False
        
        
        self.mute_button = Button(
            "UI/raw/UI_Flat_ToggleOff01a.png", "UI/raw/UI_Flat_ToggleOff01a.png",
            500, 300, 40, 20,
            self.mute_click
        )
        self.slider_button = Button(
            "UI/raw/UI_Flat_Handle02a.png", "UI/raw/UI_Flat_Handle02a.png",
            375, 260, 40, 20,
            self.slider_hold
        )
        
        
        self.save_button = Button(
            "UI/button_save.png", "UI/button_save_hover.png",
            375, 450, 70, 70,
            
            lambda: scene_manager._current_scene.game_manager.save("saves/game0.json")
        )
        
        self.load_button = Button(
            "UI/button_load.png", "UI/button_load_hover.png",
            460, 450, 70, 70,
            lambda: scene_manager._current_scene.load_save()
        )
        
        
        
    
        
    
    def slider_hold(self):
        #print("asfas")
        self.vol_slider_hold = True


    
    def mute_click(self):
        self.state_muted = not self.state_muted
        if sound_manager.current_bgm.get_volume() == 0:
            sound_manager.current_bgm.set_volume((self.slider_button.hitbox.x  - self.mn_slider_x) / (self.mx_slider_x - self.mn_slider_x - 40))
            self.mute_button.img_button_default = Sprite("UI/raw/UI_Flat_ToggleOn01a.png", (40, 20))
            self.mute_button.img_button_hover = Sprite("UI/raw/UI_Flat_ToggleOn01a.png", (40, 20))
        else:
            sound_manager.current_bgm.set_volume(0)
            self.mute_button.img_button_default = Sprite("UI/raw/UI_Flat_ToggleOff01a.png",(40, 20))
            self.mute_button.img_button_hover = Sprite("UI/raw/UI_Flat_ToggleOff01a.png", (40, 20))
            
        
    @override
    def update(self, dt: float) -> None:
        #print(self.vol_slider_hold, input_manager.mouse_down(1))
        self.return_button.update(dt)
        self.mute_button.update(dt)
        self.slider_button.update(dt)
        self.save_button.update(dt)
        self.load_button.update(dt)
        
        if self.vol_slider_hold and input_manager.mouse_down(1):
            self.slider_button.hitbox.x = input_manager.mouse_pos[0]
            self.slider_button.hitbox.x = max(self.slider_button.hitbox.x, self.mn_slider_x)
            self.slider_button.hitbox.x = min(self.slider_button.hitbox.x, self.mx_slider_x - 40)
            
            if self.state_muted == 0:
                sound_manager.current_bgm.set_volume((self.slider_button.hitbox.x  - self.mn_slider_x) / (self.mx_slider_x - self.mn_slider_x - 40))
        else:
            self.vol_slider_hold = False
            
        GameSettings.AUDIO_VOLUME = sound_manager.current_bgm.get_volume()
        
            
        if input_manager.key_pressed(27):
            scene_manager._current_scene.bag_close()
        #print(input_manager._pressed_mouse, input_manager._released_mouse, input_manager._down_mouse)


    @override
    def draw(self, screen: pg.Surface) -> None:
        WIDTH = GameSettings.SCREEN_WIDTH
        HEIGHT = GameSettings.SCREEN_HEIGHT
        
        pg.font.init()
        fonts = pg.font.Font("assets/fonts/Minecraft.ttf", 20)

        
        # screen Fade
        game_over_screen_fade = screen.copy()
        game_over_screen_fade.fill((0, 0, 0))
        game_over_screen_fade.set_alpha(160)
        screen.blit(game_over_screen_fade, (0, 0))
        
        # bag bg
        bag_WIDTH = WIDTH // 2
        bag_HEIGHT = HEIGHT * 4 // 5.5
        bag_bg = Sprite("UI/raw/UI_Flat_FrameSlot03a.png", (bag_WIDTH, bag_HEIGHT))
        screen.blit(bag_bg.image, pg.Rect(WIDTH // 2 - bag_WIDTH / 2, HEIGHT // 2 - bag_HEIGHT / 2, bag_WIDTH, bag_HEIGHT))
        
        
        bag_font = pg.font.Font("assets/fonts/Minecraft.ttf", 28)
        bag_text = bag_font.render('SETTING', False, (0, 0, 0))
        screen.blit(bag_text, (WIDTH // 2 - bag_WIDTH / 2 + 50, HEIGHT // 2 - bag_HEIGHT / 2 + 45))
        
        
        volume_txt = fonts.render(f'Volume: {round((self.slider_button.hitbox.x  - self.mn_slider_x) / (self.mx_slider_x - self.mn_slider_x - 40) * 100)}%', False, (0, 0, 0))
        screen.blit(volume_txt, (375, 225))
        
        bar_WIDTH = WIDTH // 2 - 100
        bar_HEIGT = 20
        pg.draw.rect(screen, (221, 217, 195), 
                    (375, 260, bar_WIDTH, bar_HEIGT)
        )
        
        mute_txt = fonts.render(f'Mute: {"On" if self.state_muted or round((self.slider_button.hitbox.x  - self.mn_slider_x) / (self.mx_slider_x - self.mn_slider_x - 40) * 100) == 0 else "Off"}', False, (0, 0, 0))
        screen.blit(mute_txt, (375, 300))
        
        esc_txt = fonts.render('Press ESC to close', False, (0, 0, 0))
        screen.blit(esc_txt, (375, 565))
        
        
        self.mute_button.draw(screen)
        self.slider_button.draw(screen)
        self.return_button.draw(screen)
        self.save_button.draw(screen)
        self.load_button.draw(screen)
        



        
        
