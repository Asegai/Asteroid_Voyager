from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.uix.label import Label
import random
import sys

class Player(Widget):        #! PLAYER
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.size = (50, 50)
        with self.canvas:
            Color(0, 0, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect)

    def on_touch_move(self, touch):
        self.center = touch.pos

    def on_mouse_pos(self, window, pos):
        self.center = pos

    def update_rect(self, *args):
        self.rect.pos = self.pos

class Enemy(Widget):      #! ENEMIES
    def __init__(self, **kwargs):
        super(Enemy, self).__init__(**kwargs)
        self.size = (30, 30)
        with self.canvas:
            Color(1, 0, 0, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.velocity = Vector(0, 0)
        self.bind(pos=self.update_rect)

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
        self.add_widget(Label(text="Game Over!", font_size='20sp', center=self.center))
        Clock.schedule_once(lambda dt: sys.exit(), 2)

class Asteroid_VoyagerApp(App):
    def build(self):
        game = Game()
        Window.bind(mouse_pos=game.player.on_mouse_pos)
        return game

if __name__ == '__main__':
    Asteroid_VoyagerApp().run()
