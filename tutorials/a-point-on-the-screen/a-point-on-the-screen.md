---
title: "A Point on the Screen"
year: "2026-2027"
version: 2026.09.21.1
covers:
  a-road-of-posts:
    covers: [CMPS-LO4]
  why-dividing-works:
    covers: [CMPS-LO4]
  where-the-camera-stands:
    covers: [CMPS-LO4]
  a-ball-in-orbit:
    covers: [CMPS-LO4]
    touches: [MIT-4.6]
  through-the-camera:
    touches: [CMPS-LO4]
---

# A Point on the Screen

Every picture on a screen is flat, and most of the things in it are not.
A game, a film's special effects and a 3D chart all start with points
that have a depth. They all end as pixels on a flat screen, which have
none. Somewhere in between, every point loses its third number. This
tutorial is about the rule that takes it away. The rule turns out to be
one division.

## A Road of Posts

Here are twelve fence posts, six on each side of a road, all the same
height, running away from you into the distance. Run the cell before
reading on.

```python exec
id: a-road-of-posts-1
import matplotlib.pyplot as plt

def project(x, y, z):
    return x / z, y / z

plt.figure(figsize=(5, 5))
for depth in [2, 3, 4, 6, 9, 14]:
    for side in [-1.5, 1.5]:
        foot_x, foot_y = project(side, -1, depth)
        top_x, top_y = project(side, 1, depth)
        plt.plot([foot_x, top_x], [foot_y, top_y], color="C0", linewidth=3)
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.gca().set_aspect("equal")
```

Every post is built the same way: two units tall, from $y = -1$ up to
$y = 1$, and one and a half units out from the middle of the road. The
only thing that changes from post to post is `depth`. Yet the far ones
are drawn smaller and closer to the centre, and the bottoms of the far
posts sit higher up the picture, the way the far end of a real road
does.
Nothing in the cell says "make the far ones smaller". All `project` does
is divide.

Each point going in has three numbers. $x$ is how far to the right, $y$
is how far up, and $z$ (called `depth` in the cell) is how far in front
of you. What comes out has two, because the picture is flat:

$$x' = \frac{x}{z}, \qquad y' = \frac{y}{z}$$

### Your turn

What happens to the posts if you double every depth? What about a post
at depth 1, or at depth 0.5? And where would a post at depth 0 land?
Trying that last one is fine. The error is the point.

```python exec
id: a-road-of-posts-2
hint: Copy the loop from the cell above and change the list of depths. Depth 0 is a division by zero, and Python says so.
```

## Why Dividing Works

Why divide, rather than subtract, or anything else? A side view answers
it. Imagine standing at the left edge of the next picture, looking to
the right along $z$. The screen is a sheet of glass standing one unit in
front of your eye. Light from a point behind the glass travels in a
straight line to your eye. The place where that line crosses the glass
is where you see the point.

```python exec
id: why-dividing-works-1
eye = (0, 0)
point = (4, 2)  # four units ahead, two units up
screen_z = 1

plt.figure(figsize=(6, 3))
plt.plot([eye[0], point[0]], [eye[1], point[1]], color="C1", label="line of sight")
plt.axvline(screen_z, color="grey", linestyle="--", label="the glass")
plt.plot(*point, "o", color="C0", label="the point")
plt.plot(*eye, "o", color="black", label="your eye")
plt.plot(screen_z, point[1] / point[0], "o", color="C3", label="where it appears")
plt.xlabel("z (ahead)")
plt.ylabel("y (up)")
plt.legend()
```

The line of sight crosses the glass at $y = 0.5$, and $0.5$ is $2 / 4$:
the point's height divided by its depth. Two triangles share this
picture. A big one runs from your eye out to the point, and a small one
runs from your eye out to the glass. They are the same shape. One is a
bigger copy of the other. Two triangles like that are called *similar
triangles*, and in similar triangles the matching sides are in the same
ratio. So the small triangle's height divided by its base equals the big
triangle's height divided by its base:

$$\frac{y'}{1} = \frac{y}{z}$$

Look at the same scene from above instead of from the side, and the
same picture gives $x'$. That is the whole rule, and it has a name: the
*perspective divide*. Turning a point that has a depth into a point on a
flat screen is called *projecting* it. This division is the projection
that every camera does, whether it is a real camera or a few lines of
code.

One thing in the picture was a choice: the glass stands one unit away.
Stand it two units away and everything on it is drawn twice as big.
That is what a zoom lens does. We come back to that in the third
tutorial of this series.

```question
id: why-dividing-works-2
type: multiple-choice
correct: 2

A post 2 units tall stands at depth 8. How tall is it on the screen?

- 2 units
- 0.25 units
- 4 units
```

## Where the Camera Stands

So far your eye has been at $(0, 0, 0)$, looking along $z$. A camera
somewhere else sees a different picture, because a point's depth is how
far it is *ahead of the camera*, not how far it is from some fixed spot.
If the camera is at `camera`, then a point's position as the camera
sees it is the point's position minus the camera's position. Subtract
first, then divide.

```python exec
id: where-the-camera-stands-1
def project_from(point, camera):
    x, y, z = point
    camera_x, camera_y, camera_z = camera
    depth = z - camera_z
    return (x - camera_x) / depth, (y - camera_y) / depth

print(project_from((1.5, 1, 4), camera=(0, 0, 0)))
print(project_from((1.5, 1, 4), camera=(0, 0, -4)))
```

The second camera stands four units further back. The same post top is
now eight units ahead of it instead of four, so it lands half as far
from the centre. Here is the road again, drawn from wherever
you put the camera:

```python exec
id: where-the-camera-stands-2
def draw_posts(camera):
    plt.figure(figsize=(4, 4))
    for depth in [2, 3, 4, 6, 9, 14]:
        for side in [-1.5, 1.5]:
            foot = project_from((side, -1, depth), camera)
            top = project_from((side, 1, depth), camera)
            plt.plot([foot[0], top[0]], [foot[1], top[1]], color="C0", linewidth=3)
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.gca().set_aspect("equal")

draw_posts(camera=(0, 0, -3))
```

### Your turn

Where would you stand to look down on the road from above? Try a camera
at $(0, 1.5, 0)$, then one at $(1.5, 0, 0)$, standing right over the
posts on one side. Before each run, say what you expect to see, then
check.

```python exec
id: where-the-camera-stands-3
hint: draw_posts(camera=(0, 1.5, 0)) is the first one. A camera above the posts is higher than their tops, so where do the tops land?
```

Our camera can move but it cannot turn. It always looks straight along
$z$. Turning is a matrix, and it is the next tutorial's job.

## A Ball in Orbit

Now something that moves. Here is a ball travelling in a circle in
front of the camera. The circle lies flat, like a hoop on a table. It
sits a little below eye level, so that we look slightly down on it, and
its centre is five units ahead. At an angle $\theta$ around the hoop, the
ball is at $x = r\cos\theta$ and $z = 5 + r\sin\theta$, which is the
unit circle from [The Unit Circle](tutorial:the-unit-circle) scaled up
by the hoop's radius $r$ and pushed out to depth 5.

```python exec
id: a-ball-in-orbit-1
import math

def ball_position(angle, radius=2, centre_depth=5, height=-0.8):
    return radius * math.cos(angle), height, centre_depth + radius * math.sin(angle)

for turn in [0, 0.25, 0.5, 0.75]:
    x, y, z = ball_position(turn * 2 * math.pi)
    print(f"{turn} of a turn: depth {z:.1f}")
```

At a quarter turn the ball is seven units away, and at three quarters it
is only three. It goes away from the camera and comes back. Let's
project sixty positions around the hoop and plot them all at once, with
each dot's size set by its depth:

```python exec
id: a-ball-in-orbit-2
steps = 60
screen_xs, screen_ys, sizes = [], [], []
for step in range(steps):
    x, y, z = ball_position(step * 2 * math.pi / steps)
    screen_x, screen_y = project(x, y, z)
    screen_xs.append(screen_x)
    screen_ys.append(screen_y)
    sizes.append(600 / z ** 2)

plt.figure(figsize=(6, 3))
plt.scatter(screen_xs, screen_ys, s=sizes, alpha=0.5)
plt.xlim(-0.6, 0.6)
plt.ylim(-0.35, 0)
plt.gca().set_aspect("equal")
```

A circle, seen from slightly above, comes out as a squashed oval: lower
and wider at the front, where the ball is near, and higher and narrower
at the back. The sixty steps are equally spaced around the hoop, but on
the screen they are spread out at the front and crowded together at the
back, because the same distance looks shorter when it is far away. The
ball's drawn radius follows the same rule as everything else, its real
radius divided by its depth. `scatter` wants an area rather than a
radius, so the size is divided by $z$ twice.

A film is a flip-book: many still pictures, shown quickly one after
another. A game draws sixty of those pictures every second. Here are ten
pages of our flip-book, one for every tenth of a turn:

```python exec
id: a-ball-in-orbit-3
figure, frames = plt.subplots(2, 5, figsize=(10, 4))
for index, frame in enumerate(frames.flat):
    x, y, z = ball_position(index * 2 * math.pi / 10)
    screen_x, screen_y = project(x, y, z)
    frame.add_patch(plt.Circle((screen_x, screen_y), 0.3 / z, color="C0"))
    frame.set_xlim(-0.8, 0.8)
    frame.set_ylim(-0.6, 0.6)
    frame.set_aspect("equal")
    frame.set_xticks([])
    frame.set_yticks([])
    frame.set_title(f"frame {index + 1}")
```

Read them left to right along the top row, then the bottom. The ball
starts on the right, swings round the back getting smaller and higher,
comes out on the left, and then sweeps across the front, large and low.
Every frame is the same three lines of arithmetic with a different
angle in them.

### Your turn

How would you add a second ball to the flip-book, going round the other
way, or on a smaller hoop? `ball_position` already takes a `radius`.
What does a hoop of radius 4 look like?

```python exec
id: a-ball-in-orbit-4
hint: Copy the flip-book cell, and call ball_position twice per frame. Going the other way is a negative angle.
```

A flip-book only becomes a film when somebody turns the pages.
`FuncAnimation` turns them. It calls `draw_step` once for each frame
number, and `interval` is the pause between one page and the next, in
thousandths of a second. Forty-eight frames, and the ball goes round:

```python exec
id: a-ball-in-orbit-5
from matplotlib.animation import FuncAnimation

figure, stage = plt.subplots(figsize=(3.5, 2.6))
ball = plt.Circle((0, 0), 0.1, color="C0")
stage.add_patch(ball)
stage.set_xlim(-0.8, 0.8)
stage.set_ylim(-0.6, 0.6)
stage.set_aspect("equal")

def draw_step(step):
    x, y, z = ball_position(step * 2 * math.pi / 48)
    ball.center = project(x, y, z)
    ball.radius = 0.3 / z

FuncAnimation(figure, draw_step, frames=48, interval=60)
```

The last line is the animation itself, and leaving it as the last
thing in the cell is what makes the page play it. Nothing else changed:
`draw_step` is the three lines of arithmetic from the flip-book, run
forty-eight times.

This cell is yours to change, like any other. What happens with
`interval=200`? With `frames=12`? Try `radius=3` inside `draw_step`,
and then try a `height` of $0$, so the hoop is at eye level.

## Through the Camera

What happens if the hoop is wider than the distance to its centre? With
a radius of 6 and the centre five units ahead, the nearest point of the
orbit is one unit *behind* the camera. This cell is meant to produce
something that looks wrong, so run it and look at what kind of wrong:

```python exec
id: through-the-camera-1
screen_xs, screen_ys, sizes = [], [], []
for step in range(60):
    x, y, z = ball_position(step * 2 * math.pi / 60, radius=6)
    screen_x, screen_y = project(x, y, z)
    screen_xs.append(screen_x)
    screen_ys.append(screen_y)
    sizes.append(600 / z ** 2)

plt.figure(figsize=(6, 4))
plt.scatter(screen_xs, screen_ys, s=sizes, alpha=0.5)
plt.xlim(-2, 2)
plt.ylim(-1.5, 1.5)
plt.gca().set_aspect("equal")
```

The run of small dots along the bottom is the far half of the orbit,
drawn as before. As the ball comes towards the camera, its depth
shrinks towards zero. Dividing by a number close to zero gives a huge
answer, so the ball is drawn enormous, and so far below the picture
that it is out of sight. Then its depth becomes negative. Dividing by a
negative number flips the sign, so the ball jumps to the wrong side of
the picture. Those are the big dots along the top. They sit above eye
level when the ball is really below it, and they are large because a
small negative depth divides just like a small positive one. The
arithmetic did exactly what it was told. Nobody gave it a rule for
points that are not in front of the camera.

A real *renderer*, the program that turns a scene into a picture, has
such a rule. It refuses to draw anything closer than a small fixed
depth, called the *near plane*, and cuts those points away before any
dividing happens. The third tutorial in this series shows where that
number lives.

### Your turn

Could you skip any position whose depth is less than $0.1$, so the cell
above draws only the part of the orbit that is in front of the camera?
`continue` inside the loop moves on to the next step without appending
anything.

```python exec
id: through-the-camera-2
hint: An if right after ball_position, before project. Compare z with 0.1.
```

## Reflection

One division, and a flat picture gains depth. Where did the division
come from, when you saw the side view with the glass in it? Was it what
you expected, or had you assumed something more complicated was going
on inside a game?

Look back at the flip-book. Nothing in it knows what a ball is. It knows
three numbers per frame, one division for each of two of them, and a
radius scaled by the third. That is most of what a 3D game engine does, for
many thousands of points at a time. The next tutorial gives it something
with edges to draw, and a way to turn it.

## Where to Read More

O'Flaherty-Chan, G. (2026). *Divide by depth for instant 3D.*
<https://gabrieloc.com/2026/09/15/perspective.html>. The blog post this
series grew from: the same divide, a camera you can move, and the same
ball in orbit, in a few dozen lines of code, ending at the projection
matrix the third tutorial builds.

Scratchapixel. *Computing the Pixel Coordinates of a 3D Point.*
<https://www.scratchapixel.com/lessons/3d-basic-rendering/computing-pixel-coordinates-of-3d-point/>.
The same similar-triangles picture drawn out carefully, and then the
extra steps that turn a point on the glass into a pixel on a real
screen.

Hughes, J. F., van Dam, A., McGuire, M., Sklar, D. F., Foley, J. D.,
Feiner, S. K. and Akeley, K. (2013). *Computer Graphics: Principles and
Practice* (3rd ed.). Addison-Wesley. Its chapters on cameras cover
perspective projection as it is really used, near plane and all.
