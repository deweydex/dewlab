---
title: "3D animation: a camera and a ball in orbit"
year: "2026-2027"
version: 2026.09.22.1
covers:
  where-the-camera-stands:
    covers: [CMPS-LO4]
  a-ball-in-orbit:
    covers: [CMPS-LO4]
    touches: [MIT-4.6]
  through-the-camera:
    touches: [CMPS-LO4]
---

# 3D animation: a camera and a ball in orbit

[Perspective projection: dividing by depth](tutorial:a-point-on-the-screen)
drew a road of fence posts with one division. Each point's $x$ and $y$
were divided by its depth, how far it is in front of you, and the far
posts came out small. In that tutorial the eye stayed in one place, and
nothing moved.

This tutorial changes both of those things. First the camera moves.
Then a ball goes round in a circle, and we make it move on the screen.
By the end you will have moved a camera, made a ball go round in a
circle, and seen what happens when the ball passes behind the camera.
All of it uses the same one division.

Keep three things in mind as you go:

- Every cell on this page is yours to change. Change a number, run it
  again, and see what happens.
- A cell that gives an error has told you something about a line, not
  about you. There is one cell below that is *meant* to go wrong.
- If a word is new, it is in bold the first time it appears, and the
  Reference panel, on the left, has all of them.

## Where the camera stands

In [the last tutorial](tutorial:a-point-on-the-screen) your eye was at
$(0, 0, 0)$, looking along $z$. A camera somewhere else sees a different
picture. That is because a point's depth is how far it is *ahead of the
camera*, not how far it is from some fixed spot. If the camera is at
`camera`, then a point's position as the camera sees it is the point's
position minus the camera's position. There are two steps, always in this order:

1. Subtract the camera's position from the point.
2. Divide by what is left of $z$.

Each page here begins with no code from earlier pages. So the cell
below starts with `project`, the divide from the last tutorial, exactly
as it was. `project_from` is the new part. It does step 1, then step 2.

```python exec
id: where-the-camera-stands-1
import matplotlib.pyplot as plt

def project(x, y, z):
    return x / z, y / z

def project_from(point, camera):
    x, y, z = point
    camera_x, camera_y, camera_z = camera
    depth = z - camera_z
    return (x - camera_x) / depth, (y - camera_y) / depth

print(project_from((1.5, 1, 4), camera=(0, 0, 0)))
print(project_from((1.5, 1, 4), camera=(0, 0, -4)))
```

The first line is the camera where it was before, at $(0, 0, 0)$. It
prints $(0.375, 0.25)$, the same answer `project(1.5, 1, 4)` gives.

Let's check the second line by hand. The point is $(1.5, 1, 4)$ and the
camera is at $(0, 0, -4)$. Subtraction gives $(1.5, 1, 8)$. This is the same
post top, now eight units ahead instead of four. Division by 8 gives
$(0.1875, 0.125)$, exactly what the cell printed, and exactly half of
the first line. The post is twice as far away, so it is drawn half as
far from the centre. Here is
the road of posts from the last tutorial again, drawn from wherever you
put the camera:

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
at $(0, 1.5, 0)$. Then try one at $(1.5, 0, 0)$, standing in line with
the posts on one side. Before each run, say what you expect to see,
then check. A guess that does not match costs nothing here, and it teaches you a lot.

```python exec
id: where-the-camera-stands-3
hint: draw_posts(camera=(0, 1.5, 0)) is the first one. A camera above the posts is higher than their tops, so where do the tops land?
```

Our camera can move but it cannot turn. It always looks straight along
$z$. A turn needs a matrix. The next tutorial,
[The rotation matrix: turning a cube in 3D](tutorial:turning-a-cube), does that.

## A ball in orbit

Now let's make something move. Here is a ball travelling in a circle in
front of the camera. The circle lies flat, like a hoop on a table. It
sits a little below eye level, so that we look slightly down on it, and
its centre is five units ahead.

To place the ball we need a point on a circle, and $\cos$ and $\sin$
are the tools for that. For a circle of radius 1, the point at angle
$\theta$ round from the right-hand side is at $(\cos\theta, \sin\theta)$:
$\cos\theta$ is how far across, $\sin\theta$ is how far up. That is all
you need here. [The unit circle: sine, cosine and tangent](tutorial:the-unit-circle), on the
maths course, has the full story if you want it. Our hoop has radius
$r$, and it lies flat, so the two coordinates that change are $x$ and
$z$:

- $x = r\cos\theta$, how far left or right the ball is;
- $z = 5 + r\sin\theta$, how far away it is, with the 5 pushing the
  whole hoop out in front of the camera;
- $y = -0.8$, a little below eye level, and it never changes.

One more thing before the cell. Python's `math.cos` and `math.sin`
measure an angle in ***radians***, a unit where a whole turn is $2\pi$,
about $6.28$. In degrees a whole turn is $360$. So the cell turns "a
quarter of a turn" into an angle by multiplying $0.25$ by `2 * math.pi`.

```python exec
id: a-ball-in-orbit-1
import math

def ball_position(angle, radius=2, centre_depth=5, height=-0.8):
    return radius * math.cos(angle), height, centre_depth + radius * math.sin(angle)

for turn in [0, 0.25, 0.5, 0.75]:
    x, y, z = ball_position(turn * 2 * math.pi)
    print(f"{turn} of a turn: depth {z:.1f}")
```

At a quarter turn the ball is seven units away. At three quarters of a
turn it is only three units away. It goes away from the camera and
comes back. Let's project sixty positions around the hoop and plot them
all at once, with each dot's size set by its depth:

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

A circle, seen from slightly above, looks like a squashed oval. It is
lower and wider at the front, where the ball is near, and higher and
narrower at the back. The sixty steps are equally spaced around the
hoop. On the screen, though, they are spread out at the front and
crowded together at the back. That is because the same distance looks
shorter when it is far away. The ball's drawn size follows the same
rule as everything else: its real radius divided by its depth.
`scatter` wants an area rather than a radius, so the size is divided by
$z$ twice.

### How a picture moves

Pause here for a moment. The rest of the page depends on this idea. Nothing on a screen ever really moves. A screen shows one
still picture, then another, then another, very quickly. Each still
picture is called a ***frame***. If the frames come fast enough, your
eye stops seeing separate pictures and sees movement instead. Here
are some useful numbers:

- About 20 frames a second is enough for the eye to see movement.
- A cinema film shows 24 frames every second.
- A game usually draws 60, and a fast one 120.

The number of frames shown each second is the ***frame rate***. A
flip-book works the same way. It is a small book with a slightly
different drawing on every page, and when you turn the pages quickly,
the drawing seems to move. Here are ten pages of a flip-book of our
ball, one for every tenth of a turn:

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
starts on the right. It swings round the back, getting smaller and
higher. It comes out on the left, and then sweeps across the front,
large and low. Every frame is the same three lines of arithmetic with a
different angle in them. A moving picture is the same
drawing, done again and again, with one number changing each time.

### Your turn

How would you add a second ball to the flip-book, going round the other
way, or on a smaller hoop? `ball_position` already takes a `radius`.
What does a hoop of radius 4 look like?

```python exec
id: a-ball-in-orbit-4
hint: Copy the flip-book cell, and call ball_position twice per frame. Going the other way is a negative angle.
```

### Turning the pages

A flip-book only becomes a film when somebody turns the pages.
`FuncAnimation` turns them for us. Here is what you give it, in order:

1. `figure`, the picture to draw on.
2. `draw_step`, a function that draws one frame. `FuncAnimation` calls
   it once per frame and passes in the frame number: 0, then 1, then 2,
   and so on.
3. `frames=48`, how many frames there are.
4. `interval=60`, the pause between one frame and the next, in
   thousandths of a second. 60 thousandths is about sixteen frames a
   second.

When the last frame has been shown, the animation starts again from the
first, so it runs in a ***loop***.

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

The last line is the animation itself. The page plays it because it is
the last thing in the cell. Nothing else changed.
`draw_step` is the three lines of arithmetic from the flip-book, run
forty-eight times. Instead of drawing a new circle on a new page each
time, it moves the one circle, `ball`, to its new place and gives it
its new size.

This cell is yours to change, like any other. Here are some things to
try, one at a time:

- `interval=200`, to see the separate frames again.
- `frames=12`, to see the join where the loop starts again.
- `radius=3` inside `draw_step`, for a wider hoop.
- `height=0`, so the hoop is at eye level. What shape is the path now?

## Through the camera

What happens if the hoop is wider than the distance to its centre? With
a radius of 6 and the centre five units ahead, the nearest point of the
orbit is one unit *behind* the camera. This cell is meant to produce
something that looks wrong. Let's run it and look at what goes
wrong:

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

Here is what happened, in the order it happened:

1. The run of small dots along the bottom is the far half of the
   orbit, drawn as before.
2. As the ball came towards the camera, its depth shrank towards zero.
   Dividing by a number close to zero gives a huge answer. So the ball
   was drawn enormous, and so far below the picture that it is out of
   sight.
3. Then its depth became negative. Dividing by a negative number flips
   the sign, so the ball jumped to the wrong side of the picture. Those
   are the big dots along the top. They sit above eye level when the
   ball is really below it, and they are large because a small
   negative depth divides just like a small positive one.

The arithmetic did exactly what it was told. Nobody gave it a rule for
points that are not in front of the camera. A real ***renderer***, the
program that turns points into a picture, has such a rule. It refuses
to draw anything closer than a small fixed depth, called the ***near
plane***, and removes those points before any division happens.
[Field of view](tutorial:the-fourth-number#field-of-view), in the
fourth tutorial of this series, shows where that number lives.

### Your turn

Could you skip any position whose depth is less than $0.1$, so that the
cell above draws only the part of the orbit that is in front of the
camera? `continue` inside a loop skips to the next step without
doing anything else.

```python exec
id: through-the-camera-2
hint: An if right after ball_position, before project. Compare z with 0.1.
```

## Reflection

Look back at the flip-book, and at the animation after it. Nothing in
either of them knows what a ball is. Each frame knows three numbers,
one division for each of two of them, and a size scaled by the third.
The next frame does the same with a new angle. That is most of what a 3D
game engine does, for many thousands of points at a time, sixty times
a second. The next tutorial, [The rotation matrix: turning a cube in
3D](tutorial:turning-a-cube), gives it something with edges to draw,
and a way to turn it.

## Where to read more

O'Flaherty-Chan, G. (2026). *Divide by depth for instant 3D.*
<https://gabrieloc.com/2026/09/15/perspective.html>. This series grew
from this blog post. It has the same divide, a camera you can move, and
the same ball in orbit, in a few dozen lines of code. It ends at the
projection matrix the fourth tutorial builds.

Hughes, J. F., van Dam, A., McGuire, M., Sklar, D. F., Foley, J. D.,
Feiner, S. K. and Akeley, K. (2013). *Computer Graphics: Principles and
Practice* (3rd ed.). Addison-Wesley. Its chapters on cameras cover
perspective projection as it is really used, including the near plane.

Sebastian Lague (2020). *Coding Adventure: Solar System.*
<https://www.youtube.com/watch?v=7axImc1sxa0>. Our ball goes round because
we tell it to follow a circle. Here, Sebastian Lague uses gravity
instead, and builds a small solar system that you can explore.
About twelve minutes.
