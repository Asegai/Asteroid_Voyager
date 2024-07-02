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
from PIL import Image

class Player(Widget):  #! PLAYER
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.size = (50, 50)
        self.image_path = r'C:\Users\aesas\Desktop\Asteroid_Miner\spaceship_by_simeon_templar_.gif'
        self.texture = self.load_gif_as_texture(self.image_path)
        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=self.size, texture=self.texture)
        self.bind(pos=self.update_rect)

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

    def move_towards(self, target):
        direction = Vector(target.x - self.x, target.y - self.y).normalize()
        self.velocity = direction * 2 
        self.pos = Vector(*self.velocity) + self.pos

    def update_rect(self, *args):
        self.rect.pos = self.pos

class Game(Widget):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.player = Player()
        self.add_widget(self.player)
        Clock.schedule_interval(self.spawn_enemy, 1) 
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def spawn_enemy(self, dt):  #! spawning 
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            pos = (random.randint(0, Window.width), Window.height)
        elif edge == 'bottom':
            pos = (random.randint(0, Window.width), 0)
        elif edge == 'left':
            pos = (0, random.randint(0, Window.height))
        else:
            pos = (Window.width, random.randint(0, Window.height))
        enemy = Enemy(pos=pos)
        self.add_widget(enemy)

    def update(self, dt):
        for child in self.children[:]:
            if isinstance(child, Enemy):
                child.move_towards(self.player)
                if self.player.collide_widget(child):
                    self.end_game()

    def end_game(self):
        self.clear_widgets()
        self.add_widget(Label(text="Game Over!", font_size='20sp', center=(Window.width / 2, Window.height / 2 + 20)))
        retry_button = Button(text="Retry", size_hint=(None, None), size=(100, 50), pos=(Window.width / 2 - 50, Window.height / 2 - 50))
        retry_button.bind(on_release=self.restart_game)
        self.add_widget(retry_button)
        Window.show_cursor = True  

    def restart_game(self, instance):
        self.clear_widgets()
        self.__init__()
        Window.show_cursor = False  
        Window.bind(mouse_pos=self.player.on_mouse_pos)

class Asteroid_VoyagerApp(App):
    def build(self):
        game = Game()
        Window.bind(mouse_pos=game.player.on_mouse_pos)
        Window.show_cursor = False 
        return game

if __name__ == '__main__':
    Asteroid_VoyagerApp().run()
