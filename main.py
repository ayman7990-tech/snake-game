from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Ellipse
import random

CELL = 25
GW, GH = 16, 24
BG = (0.05, 0.05, 0.1, 1)
SC = (0, 1, 0.5, 1)
FC = (1, 0.2, 0.4, 1)
TC = (1, 1, 1, 1)

class SnakeGame(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        Window.clearcolor = BG
        self.reset()
        self._last = None
        self.bind(pos=self.redraw, size=self.redraw)

    def reset(self):
        self.snake = [(8, 12), (7, 12), (6, 12)]
        self.dir = (1, 0)
        self.ndir = (1, 0)
        self.score = 0
        self.food = self.spawn()
        self.over = False
        if hasattr(self, 'ev') and self.ev:
            self.ev.cancel()
        self.ev = Clock.schedule_interval(self.move, 0.15)
        self.redraw()

    def spawn(self):
        while True:
            x, y = random.randint(0, GW-1), random.randint(0, GH-1)
            if (x, y) not in self.snake:
                return (x, y)

    def chdir(self, d):
        if (d[0]*-1, d[1]*-1) == self.dir:
            return
        self.ndir = d

    def move(self, dt):
        if self.over:
            return
        self.dir = self.ndir
        hx, hy = self.snake[0]
        nh = (hx + self.dir[0], hy + self.dir[1])
        if not (0 <= nh[0] < GW and 0 <= nh[1] < GH) or nh in self.snake:
            self.over = True
            self.ev.cancel()
            self.redraw()
            return
        self.snake.insert(0, nh)
        if nh == self.food:
            self.score += 10
            self.food = self.spawn()
        else:
            self.snake.pop()
        self.redraw()

    def redraw(self, *a):
        self.canvas.clear()
        ox = (self.width - GW * CELL) / 2
        oy = (self.height - GH * CELL) / 2
        with self.canvas:
            Color(*BG)
            Rectangle(pos=self.pos, size=self.size)
            Color(*SC)
            for i, (x, y) in enumerate(self.snake):
                p = 2 if i == 0 else 1
                Rectangle(pos=(ox + x*CELL + p, oy + y*CELL + p),
                          size=(CELL - p*2, CELL - p*2))
            Color(*FC)
            Ellipse(pos=(ox + self.food[0]*CELL + 2, oy + self.food[1]*CELL + 2),
                    size=(CELL - 4, CELL - 4))
        lbl = Label(text=f"SCORE: {self.score}", font_size='20sp', color=TC)
        lbl.texture_update()
        with self.canvas:
            Color(*TC)
            Rectangle(texture=lbl.texture, pos=(10, self.height - 40),
                      size=lbl.texture_size)
        if self.over:
            g = Label(text="GAME OVER\nTap to restart", font_size='28sp',
                      color=(1, 0.3, 0.3, 1), halign='center')
            g.texture_update()
            with self.canvas:
                Color(1, 0.3, 0.3, 1)
                Rectangle(texture=g.texture,
                          pos=(self.width/2 - g.texture_size[0]/2,
                               self.height/2 - g.texture_size[1]/2),
                          size=g.texture_size)

    def on_touch_down(self, t):
        if self.over:
            self.reset()
            return True
        self._last = t.pos
        return True

    def on_touch_move(self, t):
        if not self._last:
            self._last = t.pos
            return
        dx = t.x - self._last[0]
        dy = t.y - self._last[1]
        th = 20
        if abs(dx) > abs(dy):
            if dx > th: self.chdir((1, 0))
            elif dx < -th: self.chdir((-1, 0))
        else:
            if dy > th: self.chdir((0, 1))
            elif dy < -th: self.chdir((0, -1))
        self._last = t.pos

class SnakeApp(App):
    def build(self):
        self.title = "Snake"
        return SnakeGame()

if __name__ == "__main__":
    SnakeApp().run()
