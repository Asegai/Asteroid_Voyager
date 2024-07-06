from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
import random
import os
import json
from kivy.uix.floatlayout import FloatLayout
from PIL import Image



class MainMenu(Widget):
    def __init__(self, app, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.app = app
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(BASE_PATH, 'pixel.ttf')
        self.title_label = Label(text='Asteroid Voyager', font_name=font_path, font_size='40sp', size_hint=(None, None), size=(400, 100), pos=(Window.width / 2 - 200, Window.height / 2 + 100))
        self.add_widget(self.title_label)
        self.start_button = Button(text='Start Game', font_name=font_path, size_hint=(None, None), size=(200, 50), pos=(Window.width / 2 - 100, Window.height / 2 - 25))
        self.start_button.bind(on_release=self.start_game)
        self.add_widget(self.start_button)


        self.difficulty_slider = Slider(min=1, max=10, value=5, size_hint=(None, None), size=(400, 50), pos=(Window.width / 2 - 200, Window.height / 2 - 100))
        self.add_widget(self.difficulty_slider)
        self.difficulty_label = Label(text='Difficulty: 5', font_name=font_path, font_size='20sp', size_hint=(None, None), size=(200, 50), pos=(Window.width / 2 - 100, Window.height / 2 - 150))
        self.add_widget(self.difficulty_label)
        self.difficulty_slider.bind(value=self.on_slider_value_change)


        self.music = SoundLoader.load(os.path.join(BASE_PATH, 'flat-8-bit-gaming-music-instrumental-by-SoundUniverseStudio-from-Pixabay.mp3'))
        self.start_button_sound = SoundLoader.load(os.path.join(BASE_PATH, 'mario-coin-200bpm-from-Pixabay.mp3'))

    def on_slider_value_change(self, instance, value):
        self.difficulty_label.text = f'Difficulty: {int(value)}'

    def start_game(self, instance):
        if self.start_button_sound:
            self.start_button_sound.play()
        self.app.start_game()



class Player(Widget):
    def __init__(self, game, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.game = game
        self.size = (50, 50)
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(BASE_PATH, 'spaceship_by_simeon_templar_.gif')
        self.texture = self.load_gif_as_texture(self.image_path)
        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=self.size, texture=self.texture)
        self.bind(pos=self.update_rect)
        self.invincible = False

    def load_gif_as_texture(self, image_path):
        gif = Image.open(image_path)
        gif.seek(0)
        gif_data = gif.convert('RGBA').tobytes()
        texture = Texture.create(size=gif.size)
        texture.blit_buffer(gif_data, colorfmt='rgba', bufferfmt='ubyte')
        texture.flip_vertical()
        return texture

    def on_touch_move(self, touch):
        if not self.game.paused:
            self.center = touch.pos

    def on_mouse_pos(self, window, pos):
        if not self.game.paused:
            self.center = pos

    def update_rect(self, *args):
        self.rect.pos = self.pos

class Enemy(Widget):
    def __init__(self, **kwargs):
        self.speed = kwargs.pop('speed', 2)
        super(Enemy, self).__init__(**kwargs)
        self.size = (30, 30)
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(BASE_PATH, 'ufo_by_Bodzio855.png')
        self.texture = self.load_png_as_texture(self.image_path)
        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=self.size, texture=self.texture)
        self.velocity = Vector(0, 0)
        self.bind(pos=self.update_rect)

    def load_png_as_texture(self, image_path):
        png = Image.open(image_path)
        png_data = png.convert('RGBA').tobytes()
        texture = Texture.create(size=png.size)
        texture.blit_buffer(png_data, colorfmt='rgba', bufferfmt='ubyte')
        texture.flip_vertical()
        return texture

    def move_towards(self, target, speed): 
        direction = Vector(target.x - self.x, target.y - self.y).normalize()
        self.velocity = direction * speed
        self.pos = Vector(*self.velocity) + self.pos

    def update_rect(self, *args):
        self.rect.pos = self.pos

class Asteroid(Widget):
    def __init__(self, **kwargs):
        super(Asteroid, self).__init__(**kwargs)
        self.size = (40, 40)
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(BASE_PATH, 'brown_asteroid_by_FunwithPixels.png')
        self.texture = self.load_png_as_texture(self.image_path)
        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=self.size, texture=self.texture)
        self.velocity = Vector(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * 1
        self.bind(pos=self.update_rect)

    def load_png_as_texture(self, image_path):
        png = Image.open(image_path)
        png_data = png.convert('RGBA').tobytes()
        texture = Texture.create(size=png.size)
        texture.blit_buffer(png_data, colorfmt='rgba', bufferfmt='ubyte')
        texture.flip_vertical()
        return texture

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    def update_rect(self, *args):
        self.rect.pos = self.pos

class ExplodingAsteroid(Widget):
    def __init__(self, **kwargs):
        super(ExplodingAsteroid, self).__init__(**kwargs)
        self.size = (40, 40)
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(BASE_PATH, 'asteroid_by_thekokoricky_on_reddit.png')
        self.texture = self.load_png_as_texture(self.image_path)
        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=self.size, texture=self.texture)
        self.velocity = Vector(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * 1
        self.bind(pos=self.update_rect)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    def load_png_as_texture(self, image_path):
        png = Image.open(image_path)
        png_data = png.convert('RGBA').tobytes()
        texture = Texture.create(size=png.size)
        texture.blit_buffer(png_data, colorfmt='rgba', bufferfmt='ubyte')
        texture.flip_vertical()
        return texture

    def update_rect(self, *args):
        self.rect.pos = self.pos

class FreezeAsteroid(Widget):
    def __init__(self, **kwargs):
        super(FreezeAsteroid, self).__init__(**kwargs)
        self.size = (40, 40)
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(BASE_PATH, 'freeze_asteroid_from_terraria.png')
        self.texture = self.load_png_as_texture(self.image_path)
        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=self.size, texture=self.texture)
        self.velocity = Vector(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * 1
        self.bind(pos=self.update_rect)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    def load_png_as_texture(self, image_path):
        png = Image.open(image_path)
        png_data = png.convert('RGBA').tobytes()
        texture = Texture.create(size=png.size)
        texture.blit_buffer(png_data, colorfmt='rgba', bufferfmt='ubyte')
        texture.flip_vertical()
        return texture

    def update_rect(self, *args):
        self.rect.pos = self.pos

class RadioactiveAsteroid(Widget):
    def __init__(self, **kwargs):
        super(RadioactiveAsteroid, self).__init__(**kwargs)
        self.size = (40, 40)
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(BASE_PATH, 'radioactive_asteroid_from_r-slash-PixelArt.png')
        self.texture = self.load_png_as_texture(self.image_path)
        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=self.size, texture=self.texture)
        self.velocity = Vector(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * 1
        self.bind(pos=self.update_rect)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    def load_png_as_texture(self, image_path):
        png = Image.open(image_path)
        png_data = png.convert('RGBA').tobytes()
        texture = Texture.create(size=png.size)
        texture.blit_buffer(png_data, colorfmt='rgba', bufferfmt='ubyte')
        texture.flip_vertical()
        return texture

    def update_rect(self, *args):
        self.rect.pos = self.pos

class Game(Widget):
    initial_enemy_speed = 2

    def __init__(self, app, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.app = app
        self.enemy_speed = Game.initial_enemy_speed
        self.score = 0
        self.high_score = 0
        self.paused = False
        self.freeze_timer = None
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.asteroid_spawn_sound = SoundLoader.load(os.path.join(BASE_PATH, 'asteroid_spawn_sound_by_Lesiakower_on_Pixabay.mp3'))
        with self.canvas.before:
            self.bg_image_path = os.path.join(BASE_PATH, 'bg.png')
            self.bg_texture = self.load_png_as_texture(self.bg_image_path)
            self.bg_rect = Rectangle(texture=self.bg_texture, size=Window.size)
        Window.bind(on_resize=self.update_background)
        Window.bind(on_key_down=self.on_key_down)
        try:
            with open('high_score.json', 'r') as f:
                high_score_data = json.load(f)
            self.high_score = high_score_data.get('high_score', 0)
        except (FileNotFoundError, json.JSONDecodeError):
            self.high_score = 0
        self.setup_game()

    def load_png_as_texture(self, image_path):
        png = Image.open(image_path)
        png_data = png.convert('RGBA').tobytes()
        texture = Texture.create(size=png.size)
        texture.blit_buffer(png_data, colorfmt='rgba', bufferfmt='ubyte')
        texture.flip_vertical()
        return texture
    
    def display_pause_button(self):
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        pause_button_path = os.path.join(BASE_PATH, 'pause_button_from_Pixilart.png')
        self.pause_button = Button(size_hint=(None, None), size=(50, 50),
                                pos=(Window.width / 2 - 25, Window.height - 60),
                                background_normal=pause_button_path,
                                background_down=pause_button_path)
        self.pause_button.bind(on_release=self.toggle_pause)
        self.add_widget(self.pause_button)

    def update_background(self, window, width, height):
        self.bg_rect.size = (width, height)

    def setup_game(self):
        self.difficulty = self.app.main_menu.difficulty_slider.value
        self.clear_widgets()
        self.player = Player(game=self)
        self.add_widget(self.player)
        Window.bind(mouse_pos=self.player.on_mouse_pos)
        self.spawn_event = Clock.schedule_interval(self.spawn_enemy, 3 / self.difficulty)
        self.update_event = Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.spawn_asteroid_event = Clock.schedule_interval(self.spawn_invincible_asteroid, 10 * (self.difficulty / 5))
        self.spawn_boss_event = Clock.schedule_interval(self.spawn_boss, 60) #!
        self.spawn_exploding_asteroid_event = Clock.schedule_interval(self.spawn_exploding_asteroid, 5 * (self.difficulty / 5))
        self.spawn_freeze_asteroid_event = Clock.schedule_interval(self.spawn_freeze_asteroid, 15 * (self.difficulty / 5))
        self.spawn_radioactive_asteroid_event = Clock.schedule_interval(self.spawn_radioactive_asteroid, 20 * (self.difficulty / 5))
        self.score_event = Clock.schedule_interval(self.increment_score, 1)
        self.display_pause_button()

    def increment_score(self, dt):
        if not self.paused:
            self.score += 1

    def spawn_enemy(self, dt):
        if not self.paused:
            edge = random.choice(['top', 'bottom', 'left', 'right'])
            if edge == 'top':
                pos = (random.randint(0, Window.width), Window.height)
            elif edge == 'bottom':
                pos = (random.randint(0, Window.width), 0)
            elif edge == 'left':
                pos = (0, random.randint(0, Window.height))
            else:
                pos = (Window.width, random.randint(0, Window.height))
            enemy = Enemy(pos=pos, speed=self.enemy_speed)
            self.add_widget(enemy)

    def spawn_boss(self, dt):
        if not self.paused:
            pos = (random.randint(0, Window.width), random.randint(0, Window.height))
            boss = Boss(pos=pos)
            self.add_widget(boss)
            self.clear_enemies()
            Clock.unschedule(self.spawn_enemy)
            if self.asteroid_spawn_sound:
                self.asteroid_spawn_sound.play()

    def spawn_invincible_asteroid(self, dt):
        if not self.paused:
            center_x = Window.width / 2
            center_y = Window.height / 2
            pos = (random.randint(int(center_x) - 100, int(center_x) + 100), random.randint(int(center_y) - 100, int(center_y) + 100))
            asteroid = Asteroid(pos=pos)
            self.add_widget(asteroid)
            if self.asteroid_spawn_sound:
                self.asteroid_spawn_sound.play()

    def spawn_exploding_asteroid(self, dt):
        if not self.paused:
            pos = (random.randint(0, Window.width), random.randint(0, Window.height))
            exploding_asteroid = ExplodingAsteroid(pos=pos)
            self.add_widget(exploding_asteroid)
            if self.asteroid_spawn_sound:
                self.asteroid_spawn_sound.play()

    def spawn_freeze_asteroid(self, dt):
        if not self.paused:
            pos = (random.randint(0, Window.width), random.randint(0, Window.height))
            freeze_asteroid = FreezeAsteroid(pos=pos)
            self.add_widget(freeze_asteroid)
            if self.asteroid_spawn_sound:
                self.asteroid_spawn_sound.play()

    def spawn_radioactive_asteroid(self, dt):
        if not self.paused:
            pos = (random.randint(0, Window.width), random.randint(0, Window.height))
            radioactive_asteroid = RadioactiveAsteroid(pos=pos)
            self.add_widget(radioactive_asteroid)
            if self.asteroid_spawn_sound:
                self.asteroid_spawn_sound.play()

    def update(self, dt):
        if not self.paused:
            for child in self.children[:]:
                if isinstance(child, Enemy):
                    child.move_towards(self.player, self.enemy_speed)
                    if self.player.collide_widget(child) and not self.player.invincible:
                        self.end_game()
                elif isinstance(child, Boss):
                    child.move_towards(self.player, self.enemy_speed)
                    if self.player.collide_widget(child) and not self.player.invincible:
                        self.end_game()
                elif isinstance(child, Asteroid):
                    child.move()
                    if self.player.collide_widget(child):
                        self.player.invincible = True
                        Clock.schedule_once(self.remove_invincibility, 3)
                        self.remove_widget(child)
                    if child.x <= 0 or child.right >= Window.width or child.y <= 0 or child.top >= Window.height:
                        self.remove_widget(child)
                elif isinstance(child, ExplodingAsteroid):
                    child.move()
                    if self.player.collide_widget(child):
                        self.remove_widget(child)
                        self.clear_enemies()
                        self.clear_boss()
                elif isinstance(child, FreezeAsteroid):
                    child.move()
                    if self.player.collide_widget(child):
                        self.freeze_game(3)
                        self.remove_widget(child)
                elif isinstance(child, RadioactiveAsteroid):
                    child.move()
                    if self.player.collide_widget(child):
                        self.remove_widget(child)
                        self.start_removing_enemies()

    def remove_nearby_enemies(self, dt):
        player_pos = Vector(self.player.center_x, self.player.center_y)
        for child in self.children[:]:
            if isinstance(child, Enemy):
                enemy_pos = Vector(child.center_x, child.center_y)
                if player_pos.distance(enemy_pos) < 100:
                    self.remove_widget(child)

    def start_removing_enemies(self):
        Clock.schedule_once(self.stop_removing_enemies, 3)
        Clock.schedule_interval(self.remove_nearby_enemies, 0.1)
    
    def stop_removing_enemies(self, dt):
        Clock.unschedule(self.remove_nearby_enemies)

    def remove_invincibility(self, dt):
        self.player.invincible = False

    def clear_enemies(self):
        for child in self.children[:]:
            if isinstance(child, Enemy):
                self.remove_widget(child)
    
    def clear_boss(self):
        for child in self.children[:]:
            if isinstance(child, Boss):
                self.remove_widget(child)
                Clock.schedule_interval(self.spawn_enemy, 1)
        
    def end_game(self):
        self.spawn_event.cancel()
        self.spawn_boss_event.cancel()
        self.update_event.cancel()
        self.spawn_asteroid_event.cancel()
        self.spawn_exploding_asteroid_event.cancel()
        self.spawn_freeze_asteroid_event.cancel()
        self.score_event.cancel()
        self.spawn_radioactive_asteroid_event.cancel()
        Window.unbind(mouse_pos=self.player.on_mouse_pos)
        self.clear_widgets()
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(BASE_PATH, 'pixel.ttf')
        self.high_score = max(self.high_score, self.score)
        self.high_score = max(self.high_score, self.score)
        high_score_data = {'high_score': self.high_score}
        with open('high_score.json', 'w') as f:
            json.dump(high_score_data, f)
        score_label = Label(text=f"Score: {self.score}", font_size='20sp', font_name=font_path, center=(Window.width / 2, Window.height / 2 + 60))
        high_score_label = Label(text=f"High Score: {self.high_score}", font_size='20sp', font_name=font_path, center=(Window.width / 2, Window.height / 2 + 100))
        self.add_widget(score_label)
        self.add_widget(high_score_label)
        self.add_widget(Label(text="Game Over!", font_size='20sp', font_name=font_path, center=(Window.width / 2, Window.height / 2 + 20)))
        retry_button = Button(text="Retry?", font_name=font_path, size_hint=(None, None), size=(100, 50), pos=(Window.width / 2 - 50, Window.height / 2 - 50))
        retry_button.bind(on_release=self.restart_game)
        self.add_widget(retry_button)
        Window.show_cursor = True
        if self.app.main_menu.music:
            self.app.main_menu.music.stop()

    def restart_game(self, instance):
        if self.app.main_menu.start_button_sound:
            self.app.main_menu.start_button_sound.play()
        self.enemy_speed = Game.initial_enemy_speed
        self.score = 0
        Window.show_cursor = False
        self.setup_game()
        self.toggle_pause(manual=True)
        self.toggle_pause(manual=True)
        Window.bind(mouse_pos=self.player.on_mouse_pos)
        if self.app.main_menu.music:
            self.app.main_menu.music.play()
        self.paused = False

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if codepoint == 'p':
            self.toggle_pause(manual=True)

    def toggle_pause(self, manual=False):
        self.paused = not self.paused

        if self.paused:
            Clock.unschedule(self.update)
            Window.show_cursor = True
            if manual:
                self.freeze_timer = None
        else:
            Clock.schedule_interval(self.update, 1.0 / 60.0)
            Window.show_cursor = False
            if self.freeze_timer:
                self.freeze_timer.cancel()
                self.freeze_timer = None

    def freeze_game(self, duration):
        self.toggle_pause()
        self.freeze_timer = Clock.schedule_once(lambda dt: self.toggle_pause(), duration)

class Boss(Widget):
    def __init__(self, **kwargs):
        self.speed = kwargs.pop('speed', 2)
        super(Boss, self).__init__(**kwargs)
        self.size = (180, 180)
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(BASE_PATH, 'ufo_by_Bodzio855.png')
        self.texture = self.load_png_as_texture(self.image_path)
        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=self.size, texture=self.texture)
        self.velocity = Vector(0, 0)
        self.bind(pos=self.update_rect)

    def load_png_as_texture(self, image_path):
        png = Image.open(image_path)
        png_data = png.convert('RGBA').tobytes()
        texture = Texture.create(size=png.size)
        texture.blit_buffer(png_data, colorfmt='rgba', bufferfmt='ubyte')
        texture.flip_vertical()
        return texture

    def move_towards(self, target, speed): 
        direction = Vector(target.x - self.x, target.y - self.y).normalize()
        self.velocity = direction * speed
        self.pos = Vector(*self.velocity) + self.pos

    def update_rect(self, *args):
        self.rect.pos = self.pos

class Asteroid_VoyagerApp(App):
    def build(self):
        self.root = FloatLayout()
        self.main_menu = MainMenu(app=self)
        self.root.add_widget(self.main_menu)
        return self.root

    def start_game(self):
        self.root.clear_widgets()
        game = Game(app=self)
        self.root.add_widget(game)
        if self.main_menu.music:
            self.main_menu.music.play()
            self.main_menu.music.loop = True

if __name__ == '__main__':
    Asteroid_VoyagerApp().run()
