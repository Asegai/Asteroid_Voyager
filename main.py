from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.uix.label import Label
from kivy.uix.button import Button
import random
import sys
from kivy.uix.floatlayout import FloatLayout
from PIL import Image

class MainMenu(Widget):
    def __init__(self, app, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.app = app
        self.start_button = Button(text='Start Game', size_hint=(None, None), size=(200, 50), pos=(Window.width / 2 - 100, Window.height / 2 - 25))
        self.start_button.bind(on_release=self.start_game)
        self.add_widget(self.start_button)

    def start_game(self, instance):
        self.app.start_game()

class Player(Widget):  #! PLAYER
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.size = (50, 50)
        self.image_path = r'C:\Users\aesas\Desktop\Asteroid_Miner\spaceship_by_simeon_templar_.gif'
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
        self.center = touch.pos

    def on_mouse_pos(self, window, pos):
        self.center = pos

    def update_rect(self, *args):
        self.rect.pos = self.pos

class Enemy(Widget):  #! ENEMIES
    def __init__(self, **kwargs):
        self.speed = kwargs.pop('speed', 2)
        super(Enemy, self).__init__(**kwargs)
        self.size = (30, 30)
        self.image_path = r'C:\Users\aesas\Desktop\Asteroid_Miner\ufo_by_Bodzio855.png'
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

class Asteroid(Widget):  #! ASTEROID
    def __init__(self, **kwargs):
        super(Asteroid, self).__init__(**kwargs)
        self.size = (40, 40)
        self.image_path = r'C:\Users\aesas\Desktop\Asteroid_Miner\brown_asteroid_by_FunwithPixels.png'
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

class Game(Widget):
    initial_enemy_speed = 2

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.enemy_speed = Game.initial_enemy_speed
        with self.canvas.before:
            self.bg_image_path = r'C:\Users\aesas\Desktop\Asteroid_Miner\background_by_astrellon3_on_reddit.png'
            self.bg_texture = self.load_png_as_texture(self.bg_image_path)
            self.bg_rect = Rectangle(texture=self.bg_texture, size=Window.size)
        Window.bind(on_resize=self.update_background)
        self.setup_game()

    def load_png_as_texture(self, image_path):
        png = Image.open(image_path)
        png_data = png.convert('RGBA').tobytes()
        texture = Texture.create(size=png.size)
        texture.blit_buffer(png_data, colorfmt='rgba', bufferfmt='ubyte')
        texture.flip_vertical()
        return texture

    def update_background(self, window, width, height):
        self.bg_rect.size = (width, height)

    def setup_game(self):
        self.clear_widgets()
        self.player = Player()
        self.add_widget(self.player)
        Window.bind(mouse_pos=self.player.on_mouse_pos)
        self.spawn_event = Clock.schedule_interval(self.spawn_enemy, 1)
        self.update_event = Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.spawn_asteroid_event = Clock.schedule_interval(self.spawn_asteroid, 18)

    def spawn_enemy(self, dt): 
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

    def spawn_asteroid(self, dt):  
        center_x = Window.width / 2
        center_y = Window.height / 2
        pos = (random.randint(center_x - 100, center_x + 100), random.randint(center_y - 100, center_y + 100))
        asteroid = Asteroid(pos=pos)
        self.add_widget(asteroid)

    def update(self, dt):
        for child in self.children[:]:
            if isinstance(child, Enemy):
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

    def remove_invincibility(self, dt):
        self.player.invincible = False

    def end_game(self):
        self.spawn_event.cancel()
        self.update_event.cancel()
        self.spawn_asteroid_event.cancel()
        Window.unbind(mouse_pos=self.player.on_mouse_pos)
        self.clear_widgets()
        font_path = r'C:\Users\aesas\Desktop\Asteroid_Miner\pixel.ttf'
        self.add_widget(Label(text="Game Over!", font_size='20sp', font_name=font_path, center=(Window.width / 2, Window.height / 2 + 20)))
        retry_button = Button(text="Retry?", font_name=font_path, size_hint=(None, None), size=(100, 50), pos=(Window.width / 2 - 50, Window.height / 2 - 50))
        retry_button.bind(on_release=self.restart_game)
        self.add_widget(retry_button)
        Window.show_cursor = True  

    def restart_game(self, instance):
        self.enemy_speed = Game.initial_enemy_speed
        Window.show_cursor = False
        self.setup_game()
        Window.bind(mouse_pos=self.player.on_mouse_pos)

class Asteroid_VoyagerApp(App):
    def build(self):
        self.root = FloatLayout()
        self.main_menu = MainMenu(app=self)
        self.root.add_widget(self.main_menu)
        return self.root

    def start_game(self):
        self.root.clear_widgets()
        game = Game()
        self.root.add_widget(game)

if __name__ == '__main__':
    Asteroid_VoyagerApp().run()
