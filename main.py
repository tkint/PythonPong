from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, \
	ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock


class PongPaddle(Widget):
	score = NumericProperty(0)

	def bounce_ball(self, ball):
		if self.collide_widget(ball):
			vx, vy = ball.velocity
			offset = (ball.center_y - self.center_y) / (self.height / 10)
			bounced = Vector(-1 * vx, vy)
			vel = bounced * 1.1
			ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(0)
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	def move(self):
		self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
	step = 5
	ball = ObjectProperty(None)
	player1 = ObjectProperty(None)
	player2 = ObjectProperty(None)

	pressed_keys = {
		'a': False,
		'q': False,
		'p': False,
		'm': False
	}

	def serve_ball(self, vel=(4, 0)):
		self.keyboard = Window.request_keyboard(self.on_keyboard_closed, self)
		self.keyboard.bind(on_key_down=self.on_keyboard_down)
		self.keyboard.bind(on_key_up=self.on_keyboard_up)
		self.ball.center = self.center
		self.ball.velocity = vel

	def on_keyboard_closed(self):
		self.keyboard.unbind(on_key_down=self.on_keyboard_down)
		self.keyboard = None

	def on_keyboard_down(self, keyboard, keycode, text, modifiers):
		pressed_key = keycode[1]
		if pressed_key == 'spacebar':
			Window.fullscreen = not Window.fullscreen
		self.pressed_keys[pressed_key] = True
		return True

	def on_keyboard_up(self, keyboard, keycode):
		released_key = keycode[1]
		self.pressed_keys[released_key] = False
		return True

	def update(self, dt):
		self.ball.move()
		self.update_bounce()
		self.update_player_move()
		self.update_score()

	def update_bounce(self):
		self.player1.bounce_ball(self.ball)
		self.player2.bounce_ball(self.ball)
		if (self.ball.y < self.y) or (self.ball.top > self.top):
			self.ball.velocity_y *= -1

	def update_player_move(self):
		if self.pressed_keys['a']:
			if self.player1.center_y + self.step < self.height:
				self.player1.center_y += self.step

		if self.pressed_keys['q']:
			if self.player1.center_y + self.step > 0:
				self.player1.center_y -= self.step

		if self.pressed_keys['p']:
			if self.player2.center_y + self.step < self.height:
				self.player2.center_y += self.step

		if self.pressed_keys['m']:
			if self.player2.center_y + self.step > 0:
				self.player2.center_y -= self.step

	def update_score(self):
		if self.ball.x < self.x:
			self.player2.score += 1
			self.serve_ball(vel=(4, 0))
		if self.ball.x > self.width:
			self.player1.score += 1
			self.serve_ball(vel=(-4, 0))


class PongApp(App):
	def build(self):
		game = PongGame()
		game.serve_ball()
		Clock.schedule_interval(game.update, 1.0 / 60.0)
		return game


if __name__ == '__main__':
	PongApp().run()
