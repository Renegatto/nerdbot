import io
import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, List, Tuple
from PIL import Image

# plot equation on cartesian graph and return png byte array
def static_cartesian(func: Callable[[np.ndarray], np.ndarray], x_range: Tuple[float, float]) -> io.BytesIO:
	fig, ax = plt.subplots()

	ax.grid(True, which="both")

	# set up spines
	ax.spines["left"].set_position("zero")
	ax.spines["right"].set_color("none")
	ax.yaxis.tick_left()
	ax.spines["bottom"].set_position("zero")
	ax.spines["top"].set_color("none")
	ax.xaxis.tick_bottom()

	x1, x2 = x_range

	x = np.linspace(x1, x2, 10*int(x2-x1))
	y = func(x)

	ax.plot(x, y)

	buf = io.BytesIO()
	plt.savefig(buf, format="png")

	return buf


# plot equation on cartesian graph and return gif byte array of animating a value over specified range
def animated_cartesian(func: Callable[[np.ndarray, np.ndarray], np.ndarray], x_range: Tuple[float, float], a_range: Tuple[float, float]) -> io.BytesIO:
	fig, ax = plt.subplots()

	ax.grid(True, which="both")

	# set up spines
	ax.spines["left"].set_position("zero")
	ax.spines["right"].set_color("none")
	ax.yaxis.tick_left()
	ax.spines["bottom"].set_position("zero")
	ax.spines["top"].set_color("none")
	ax.xaxis.tick_bottom()

	x1, x2 = x_range
	a1, a2 = a_range

	x = np.linspace(x1, x2, 10*int(x2-x1))
	a = np.linspace(a1, a2, int(a2-a1)+1)

	plt.xlim(x1, x2)
	plt.ylim(min(0, func(x1, a2)), func(x2, a2))

	plt.autoscale(False)

	frames = []
	for a_val in a:
		y = func(x, a_val)

		curve = ax.plot(x, y)
		plt.title(f"a = {a_val}", bbox={"facecolor": "black", "alpha": 0.75, "pad": 5}, loc="left", color="white")

		_buf = io.BytesIO()
		plt.savefig(_buf, format="png")
		frames.append(_buf)

		curve.pop(0).remove()

	buf = io.BytesIO()
	frames = [Image.open(frame) for frame in frames]
	frames[0].save(buf, format="GIF", save_all=True, append_images=frames[1:], duration=250, loop=0)

	return buf


# plot equation on polar graph and return png byte array
def static_polar(func: Callable[[np.ndarray], np.ndarray], theta_range: Tuple[float, float]) -> io.BytesIO:
	fig, ax = plt.subplots(subplot_kw={"projection": "polar"})

	ax.grid(True, which="both")

	theta1, theta2 = theta_range
	theta = np.linspace(theta1, theta2, 1000)

	r = func(theta)

	ax.plot(r, theta)

	buf = io.BytesIO()
	plt.savefig(buf, format="png")

	return buf


# plot equation on polar graph and return gif byte array of animating a value over specified range
def animated_polar(func: Callable[[np.ndarray, np.ndarray], np.ndarray], theta_range: Tuple[float, float], a_range: Tuple[float, float]) -> io.BytesIO:
	fig, ax = plt.subplots(subplot_kw={"projection": "polar"})

	ax.grid(True, which="both")

	theta1, theta2 = theta_range
	a1, a2 = a_range

	theta = np.linspace(theta1, theta2, 1000)
	a = np.linspace(a1, a2, int(a2-a1)+1)

	frames = []
	for a_val in a:
		r = func(theta, a_val)

		curve = ax.plot(r, theta)
		plt.title(f"a = {a_val}", bbox={"facecolor": "black", "alpha": 0.75, "pad": 5}, loc="left", color="white")

		_buf = io.BytesIO()
		plt.savefig(_buf, format="png")
		frames.append(_buf)

		curve.pop(0).remove()

	buf = io.BytesIO()
	frames = [Image.open(frame) for frame in frames]
	frames[0].save(buf, format="GIF", save_all=True, append_images=frames[1:], duration=250, loop=0)

	return buf


def static_surface(func: Callable[[np.ndarray, np.ndarray], np.ndarray], x_range: Tuple[float, float], y_range: Tuple[float, float]) -> io.BytesIO:
	fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

	x1, x2 = x_range
	y1, y2 = y_range

	point_count = max(10*int(x2-x1), 10*int(y2-y1))

	x = np.linspace(x1, x2, point_count)
	y = np.linspace(y1, y2, point_count)
	x, y = np.meshgrid(x, y)

	z = func(x, y)

	ax.plot_surface(x, y, z)

	buf = io.BytesIO()
	plt.savefig(buf, format="png")

	return buf


def static_surface_rotate(func: Callable[[np.ndarray, np.ndarray], np.ndarray], x_range: Tuple[float, float], y_range: Tuple[float, float]) -> io.BytesIO:
	fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

	x1, x2 = x_range
	y1, y2 = y_range

	point_count = max(10*int(x2-x1), 10*int(y2-y1))

	x = np.linspace(x1, x2, point_count)
	y = np.linspace(y1, y2, point_count)
	x, y = np.meshgrid(x, y)

	z = func(x, y)

	ax.plot_surface(x, y, z)

	frames = []
	for a in range(0, 360, 6):
		ax.view_init(30, a)
		
		_buf = io.BytesIO()
		plt.savefig(_buf, format="png")
		frames.append(_buf)

	buf = io.BytesIO()
	frames = [Image.open(frame) for frame in frames]
	frames[0].save(buf, format="GIF", save_all=True, append_images=frames[1:], duration=150, loop=0)

	return buf


def animated_surface(func: Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray], x_range: Tuple[float, float], y_range: Tuple[float, float], a_range: Tuple[float, float]) -> io.BytesIO:
	fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

	x1, x2 = x_range
	y1, y2 = y_range
	a1, a2 = a_range

	point_count = max(10*int(x2-x1), 10*int(y2-y1))

	x = np.linspace(x1, x2, point_count)
	y = np.linspace(y1, y2, point_count)
	a = np.linspace(a1, a2, int(a2-a1)+1)

	x, y = np.meshgrid(x, y)

	plt.xlim(x1, x2)
	plt.ylim(y1, y2)
	ax.set_zlim(min(0, func(x1, y1, a2)), func(x2, y2, a2))

	frames = []
	for a_val in a:
		z = func(x, y, a_val)

		surface = ax.plot_surface(x, y, z)
		plt.title(f"a = {a_val}", bbox={"facecolor": "black", "alpha": 0.75, "pad": 5}, loc="left", color="white")

		_buf = io.BytesIO()
		plt.savefig(_buf, format="png")
		frames.append(_buf)

		surface.remove()

	buf = io.BytesIO()
	frames = [Image.open(frame) for frame in frames]
	frames[0].save(buf, format="GIF", save_all=True, append_images=frames[1:], duration=250, loop=0)

	return buf


def animated_surface_rotate(func: Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray], x_range: Tuple[float, float], y_range: Tuple[float, float], a_range: Tuple[float, float]) -> io.BytesIO:
	fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

	x1, x2 = x_range
	y1, y2 = y_range
	a1, a2 = a_range

	point_count = max(10*int(x2-x1), 10*int(y2-y1))

	x = np.linspace(x1, x2, point_count)
	y = np.linspace(y1, y2, point_count)
	a = np.linspace(a1, a2, 60)

	x, y = np.meshgrid(x, y)

	plt.xlim(x1, x2)
	plt.ylim(y1, y2)
	ax.set_zlim(min(0, func(x1, y1, a2)), func(x2, y2, a2))

	frames = []
	for angle in range(0, 360, 6):
		a_val = a[angle//6]

		z = func(x, y, a_val)

		surface = ax.plot_surface(x, y, z)
		plt.title(f"a = {a_val}", bbox={"facecolor": "black", "alpha": 0.75, "pad": 5}, loc="left", color="white")

		ax.view_init(30, angle)

		_buf = io.BytesIO()
		plt.savefig(_buf, format="png")
		frames.append(_buf)

		surface.remove()

	buf = io.BytesIO()
	frames = [Image.open(frame) for frame in frames]
	frames[0].save(buf, format="GIF", save_all=True, append_images=frames[1:], duration=250, loop=0)

	return buf


#remove from here down, just for testing
def display_gif(gif: io.BytesIO) -> None:
	import pyglet

	gif.seek(0)

	animation = pyglet.image.load_animation("noname.gif", file=gif)
	sprite = pyglet.sprite.Sprite(animation)

	win = pyglet.window.Window(width=sprite.width, height=sprite.height)
	pyglet.gl.glClearColor(0, 0, 0, 1)

	@win.event
	def on_draw() -> None:
		win.clear()
		sprite.draw()

	pyglet.app.run()


def main() -> None:
	graph = animated_surface_rotate(lambda x, y, a: a * x**2 + a * y, (-5, 5), (0, 5), (0, 5))
	display_gif(graph)


if __name__ == "__main__":
	main()