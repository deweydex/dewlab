---
title: "Mixed problems: shapes, angles and waves"
practice_across:
  - straight-lines
  - how-far-apart
  - going-round-in-circles
  - waves
  - how-tall-is-that-tree
year: "2026-2027"
version: 2026.09.26.1
---

# Mixed problems: shapes, angles and waves

Each problem here draws on at least one page of Unit 8, and many draw on
two or more. None of them is harder than what those pages covered. This
time, nobody tells you which page a problem comes from. You choose the
tool yourself, and that is part of the problem.

Along the way, the problems build this unit's product: a small collision
checker for a 2D game. A ball and a player are circles, and a wall is a
straight line at a slant. The checker says when the ball hits either of
them, and an arrow in the corner of the screen gives the bearing and
distance to the goal. Problems 5, 7, 8, 10, 12 and 14 are the checker's
parts, and they build on each other, so do those in order. At the end,
the checker runs a small game you can play with the arrow keys, and
change level by level.

Your toolkit is loaded on this page: `slope`, `line_through`,
`distance`, `midpoint`, `point_on_circle`, `wave` and `angle_between`
from this unit, and every tool from Units 1 to 7, such as
`solve_simultaneous` and `close_enough`. A cell that says
`distance = ...` hides that tool for the rest of the page, so give your
numbers names like `gap`. Each answer is hidden until you open it, and
each one is only one way. Yours may be different and work too. Where
a problem asks you to predict, make the prediction before you run
anything. It is the most useful part.

## Warm-up

Use this cell for any warm-up problem. Paste in the code, and run it.

```python exec
id: mixed-shapes-scratch-1
import math
# Try things here
```

**1. Predict.** What does each line print?

```python
print(slope((0, 0), (4, 2)))
print(distance((0, 0), (6, 8)))
print(midpoint((0, 0), (6, 8)))
```

<details class="dl-answer"><summary>answer</summary>

`0.5`, `10.0` and `(3.0, 4.0)`.

The line rises 2 over a run of 4, so its slope is $\frac{2}{4}$. The
distance is a 6, 8, 10 triangle, the 3, 4, 5 triangle made twice as
big, as on
[How far apart?](tutorial:how-far-apart#the-distance-between-two-points).
The midpoint is halfway across and halfway up.

</details>

**2. Predict.** What do these three lines print? The last one is a
musical note. Which note is it?

```python
x, y = point_on_circle(2, 90)
print(round(x, 3), round(y, 3))
print(round(wave(3, 1, 0.25), 3))
print(440 * 2)
```

<details class="dl-answer"><summary>answer</summary>

`0.0 2.0`, then `3.0`, then `880`.

A quarter turn on a circle of radius 2 takes the point to the top. The
`round` hides a tiny float error in $x$, as on
[Going round in circles](tutorial:going-round-in-circles#converting).
A wave of amplitude 3 that repeats once a second is at its top a quarter
of a second in. And 880 Hz is the A an octave above the 440 Hz A,
because an octave is a doubling, as on
[Waves](tutorial:waves#higher-notes-an-octave-is-a-doubling).

</details>

**3. Predict.** A physiotherapist checks how far a knee bends. A phone
photo gives three points, in centimetres: the hip at $(0, 90)$, the knee
at $(10, 45)$ and the ankle at $(0, 0)$. Roughly what angle does the
knee make? Guess, then run it.

```python
print(round(angle_between((0, 90), (10, 45), (0, 0)), 1))
```

<details class="dl-answer"><summary>answer</summary>

`154.9`.

The knee is the middle point, so it goes in the middle of
`angle_between`. A straight leg would be 180°, and this knee is bent by
about 25°. The picture is symmetric. The thigh and the shin each lean
about 12.5° away from straight.

</details>

**4. Explain.** In a video game set on a small round planet, a player
walks straight ahead. She turns left through 90° and walks the same
distance again. She turns left through 90° once more, walks the same
distance, and is back where she started. The corner where she started
is a right angle too. Could that happen on a flat plane? What does it
tell you about the planet?

<details class="dl-answer"><summary>answer</summary>

Not on a flat plane. The path is a triangle with three corners of 90°,
which adds up to 270°. On a flat plane, a triangle's angles always make
180°, and three equal walks with 90° turns trace three sides of a
square, which does not close.

On a ball it can happen. This is the triangle from the North Pole to two
points on the equator, from
[Going round in circles](tutorial:going-round-in-circles#triangles-on-a-ball).
Each walk is a quarter of the way round the planet. The game's world is
curved, and the rule of 180° is true only on a flat plane.

</details>

## Core

The screen for the checker is 400 pixels wide and 300 high, with $y$
going up, as on the maths plane. A scratch cell for the core problems.
Keep the checker's functions in it as you write them, so that later
problems can use them.

```python exec
id: mixed-shapes-scratch-2
import math
# Your collision checker, problem by problem
```

**5. Make.** A game keeps each circle as a dictionary with a centre and
a radius, such as `ball = {"centre": (120, 80), "radius": 10}`. The
first part of the checker is `circles_hit(first, second)`, which returns
True when two such circles touch or overlap. Test it with a
player `{"centre": (160, 110), "radius": 25}`, and then with the ball
moved to `(140, 95)`.

<details class="dl-answer"><summary>answer</summary>

```python
def circles_hit(first, second):
    """Return True when two circles, each a dict with a centre and a radius, touch or overlap."""
    gap = distance(first["centre"], second["centre"])
    return gap <= first["radius"] + second["radius"]

ball = {"centre": (120, 80), "radius": 10}
player = {"centre": (160, 110), "radius": 25}
print(circles_hit(ball, player))
print(circles_hit({"centre": (140, 95), "radius": 10}, player))
```

`False`, then `True`. The centres are 50 apart, a 40, 30, 50 triangle,
and the two radii add up to 35, so there is a gap of 15 pixels between
the edges. Moved to $(140, 95)$, the ball's centre is 25 from the
player's, a triangle half the size, and the circles overlap by 10
pixels. This is the test from
[How far apart?](tutorial:how-far-apart#did-the-ball-hit-the-player),
with the circles kept as dictionaries so each one carries its own
radius.

</details>

**6. Fix.** Schlomi, who is learning Python too, is writing a
five-a-side football game. It checks whether a ball of radius 11 cm
touches a player's foot, a circle of radius 5 cm. It says there is no
touch, but the centres are 14 cm apart. What is her check comparing,
and what needs to change?

```python exec
id: mixed-shapes-fix-touch
def ball_touches_foot(ball_centre, foot_centre):
    """Return True when the ball (radius 11) touches the foot (radius 5)."""
    return distance(ball_centre, foot_centre) <= 11

print(ball_touches_foot((0, 0), (14, 0)))
```

<details class="dl-answer"><summary>answer</summary>

The test compares the gap with the ball's radius only. Two circles
touch when the gap is at most both radii added: $11 + 5 = 16$. So the
last line should be

```python
    return distance(ball_centre, foot_centre) <= 11 + 5
```

and the call then gives `True`. Schlomi's version treats the foot as a
single point, with no size, which is how many games start before the
players have a shape.

</details>

**7. Make.** Now the wall. It runs across the screen from $(0, 300)$ to
$(400, 100)$. `solve_simultaneous` from
[Several unknowns at once](tutorial:several-unknowns-at-once) wants a
line as $ax + by = c$. That is the general form from
[Straight lines](tutorial:straight-lines#every-line-at-once-ax-by-c-0),
with the number moved to the other side, so it has room for a wall that
goes straight up too. Write `wall_line(end_a, end_b)`, which returns
`(a, b, c)` for the line through two points, using

$$a = y_2 - y_1 \qquad b = x_1 - x_2 \qquad c = a x_1 + b y_1$$

Check it the Unit 7 way: substitute both ends back in. Then try a wall
that goes straight up, from $(50, 0)$ to $(50, 300)$.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Split the two points: `x1, y1 = end_a` and `x2, y2 = end_b`.
2. Calculate `a`, `b` and `c` from the three formulas, in that order,
   since `c` needs the other two.
3. For the check, `a * x + b * y` should equal `c` for both ends.

**Think about:** why does the formula for `c` use the first end? Would
the second end give the same `c`?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def wall_line(end_a, end_b):
    """Return (a, b, c) for the line a*x + b*y = c through two different points."""
    x1, y1 = end_a
    x2, y2 = end_b
    a = y2 - y1
    b = x1 - x2
    c = a * x1 + b * y1
    return (a, b, c)

wall = wall_line((0, 300), (400, 100))
print(wall)
a, b, c = wall
for x, y in [(0, 300), (400, 100)]:
    print(a * x + b * y == c)
print(wall_line((50, 0), (50, 300)))
```

The wall is $-200x - 400y = -120000$, and both ends land on it. The
numbers are large, but any multiple of the three describes the same
line: dividing by −200 gives $x + 2y = 600$. From that, $y = -0.5x + 300$,
so the wall has a slope of −0.5, the same as `slope((0, 300), (400, 100))`.

The upright wall is `(300, 0, 15000)`, which is $300x = 15000$, or
$x = 50$. `line_through` could not have written it, since a line
straight up has no slope.

</details>

**8. Make.** How near is the ball to the wall? The nearest point of the
wall is where a line from the ball's centre meets the wall at a right
angle. From
[Straight lines](tutorial:straight-lines#parallel-and-perpendicular),
turning a line a quarter turn swaps its run and rise and changes one
sign. So if the wall is $ax + by = c$, the line through the centre
$(p, q)$ at a right angle to it is

$$bx - ay = bp - aq$$

Write `nearest_point(wall, centre)`, which solves those two lines
together with `solve_simultaneous`. Test it with the centre $(300, 200)$.

<details class="dl-answer"><summary>answer</summary>

```python
def nearest_point(wall, centre):
    """Return the point on the wall line (a, b, c) nearest to centre."""
    a, b, c = wall
    p, q = centre
    return solve_simultaneous(a, b, c, b, -a, b * p - a * q)

foot = nearest_point(wall, (300, 200))
print(foot)
print(distance((300, 200), foot))
print(slope((300, 200), foot) * slope((0, 300), (400, 100)))
```

The nearest point is $(280.0, 160.0)$, about 44.7 pixels from the
centre. The last line checks the right angle. The two slopes multiply
to $-1$, as perpendicular slopes must. For the upright wall, the same
function gives the point level with the centre, straight across.

</details>

**9. Explain.** Why is the point where the right-angled line meets the
wall the nearest one? Picture any other point on the wall. What shape do
the centre, the nearest point and that other point make, and which of
its sides is longest?

<details class="dl-answer"><summary>answer</summary>

The centre, the nearest point and any other point on the wall make a
right-angled triangle, with the right angle at the nearest point. The
line from the centre to the other point is its hypotenuse, and by
[Pythagoras](tutorial:how-far-apart#squares-on-the-sides-pythagoras)
the hypotenuse is always the longest side. Its square is the other two
squares added. So every other point on the wall is further away.

</details>

**10. Make.** Now `ball_hits_wall(ball, wall)`, which returns True
when a ball, kept as a dictionary as in problem 5, touches or crosses
the wall. Test it with balls of radius 10 at $(300, 200)$, at
$(260, 160)$ and at $(200, 200)$.

<details class="dl-answer"><summary>answer</summary>

```python
def ball_hits_wall(ball, wall):
    """Return True when a ball (a dict with a centre and a radius) touches or crosses the wall."""
    foot = nearest_point(wall, ball["centre"])
    return distance(ball["centre"], foot) <= ball["radius"]

for centre in [(300, 200), (260, 160), (200, 200)]:
    print(centre, ball_hits_wall({"centre": centre, "radius": 10}, wall))
```

`False`, `True`, `True`. The first ball is about 44.7 pixels from the
wall. The second is about 8.9 pixels from it, less than its radius, so
it overlaps. The third has its centre on the wall itself: $200 + 2
\times 200 = 600$. The checker has two parts now, one for circles and
one for the wall, each built from a tool of this unit.

</details>

**11. Fix.** In a racing game, a side track meets the main track at a
right angle, at the point $(4, 5)$ on the game's map. The main track
runs along $y = 2x - 3$. This code finds the side track's line, but a
check says the two are not at a right angle. What does it get, and what
needs to change?

```python exec
id: mixed-shapes-fix-path
track_slope = 2
side_slope = 1 / track_slope
side_start = 5 - side_slope * 4
print("side track: y =", side_slope, "x +", side_start)
print(close_enough(track_slope * side_slope, -1))
```

<details class="dl-answer"><summary>answer</summary>

A perpendicular slope is $-\frac{1}{m}$, not $\frac{1}{m}$. The fix is

```python
side_slope = -1 / track_slope
```

Then the side track is $y = -0.5x + 7$, and the check prints `True`. With
$+\frac{1}{2}$, the two lines both go uphill, and they cross at a sharp
angle, about 37°. `angle_between` can measure it: try
`angle_between((5, 7), (4, 5), (6, 6))`.

</details>

**12. Make.** The last part of the checker is the arrow in the corner.
It points from the player to the goal, and says how far away the goal
is. Write `bearing_and_distance(start, end)`, which returns a pair:
the bearing from `start` to `end`, from 0° up to 360°, clockwise from
the top of the screen, and the distance. Test it from $(160, 110)$ to a
goal at $(360, 260)$, and to one at $(10, 110)$.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find how far "east" (across) and "north" (up) `end` is from
   `start`.
2. `math.atan2(east, north)` gives the angle from the top, turning
   clockwise, in radians. Turn it into degrees, then use `% 360`.
3. `distance` gives the other half of the pair.

**Think about:** why `atan2` and not `atan(east / north)`? Try both on
the second goal.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def bearing_and_distance(start, end):
    """Return (bearing in degrees from 0 up to 360, distance) from start to end."""
    east = end[0] - start[0]
    north = end[1] - start[1]
    bearing = math.degrees(math.atan2(east, north)) % 360
    return (bearing, distance(start, end))

print(bearing_and_distance((160, 110), (360, 260)))
print(bearing_and_distance((160, 110), (10, 110)))
```

The first goal is on a bearing of about 53.1°, 250 pixels away: across
200 and up 150, a 4, 3, 5 triangle made 50 times bigger. The second is
due west, 270°, 150 pixels away. `atan(east / north)` would stop with a
`ZeroDivisionError` there, since the goal is not north at all. `atan2`
takes the two sides separately, as on
[Solving triangles](tutorial:how-tall-is-that-tree#bearings).

</details>

## Stretch

A scratch cell for the stretch problems.

```python exec
id: mixed-shapes-scratch-3
import math
# Your working for problems 13 to 16
```

**13. Another way.** A geometry book gives a formula for the distance
from a point $(p, q)$ to the line $ax + by = c$, with no nearest point
at all:

$$\frac{|ap + bq - c|}{\sqrt{a^2 + b^2}}$$

Check that it agrees with your `nearest_point` and `distance`, for the
slanted wall and the upright wall, at a hundred random centres on the
screen.

<details class="dl-answer"><summary>answer</summary>

```python
import random

def gap_by_formula(wall, centre):
    """Return the distance from centre to the wall line (a, b, c), by the book's formula."""
    a, b, c = wall
    p, q = centre
    return abs(a * p + b * q - c) / math.sqrt(a ** 2 + b ** 2)

for this_wall in [wall_line((0, 300), (400, 100)), wall_line((50, 0), (50, 300))]:
    for trial in range(100):
        centre = (random.uniform(0, 400), random.uniform(0, 300))
        by_foot = distance(centre, nearest_point(this_wall, centre))
        assert close_enough(by_foot, gap_by_formula(this_wall, centre))
print("The two ways agree.")
```

They agree every time. The formula is quicker, and a game that checks
thousands of walls a second might prefer it. The nearest point gives
more. It says where the ball touches the wall, which a game needs to
draw a spark there, or to bounce the ball.

</details>

**14. Make.** Put the checker together. A ball of radius 10 starts at
$(100, 44)$ and moves 12 pixels across and 9 up each frame, towards the
wall. The player stands at $(330, 150)$ with a radius of 25. Write a loop
over the frames that stops at the first hit, and says what was hit,
in which frame, and where the ball was. Then draw that frame: the wall
as a line, the two circles, and the ball's path so far.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Keep the wall with `wall_line`, and the player as a dictionary.
2. In each frame, find the ball's centre from its start and the
   frame number, and make a ball dictionary.
3. Check `ball_hits_wall` and `circles_hit`. If either is True, print
   and `break`.
4. For the drawing, `plt.Circle` and `add_patch` from
   [How far apart?](tutorial:how-far-apart#did-the-ball-hit-the-player)
   draw each circle, and `plt.plot` draws the wall and the path.

**Think about:** what should the checker say if both are hit in the
same frame?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
import matplotlib.pyplot as plt

wall = wall_line((0, 300), (400, 100))
player = {"centre": (330, 150), "radius": 25}
path_x = []
path_y = []
for frame in range(40):
    ball = {"centre": (100 + 12 * frame, 44 + 9 * frame), "radius": 10}
    path_x.append(ball["centre"][0])
    path_y.append(ball["centre"][1])
    if ball_hits_wall(ball, wall):
        print("the wall, in frame", frame, "at", ball["centre"])
        break
    if circles_hit(ball, player):
        print("the player, in frame", frame, "at", ball["centre"])
        break

figure, axes = plt.subplots()
axes.plot([0, 400], [300, 100], color="black", linewidth=3)
axes.plot(path_x, path_y, color="grey", linestyle="--")
axes.add_patch(plt.Circle(player["centre"], player["radius"], color="lightblue"))
axes.add_patch(plt.Circle(ball["centre"], ball["radius"], color="orange"))
axes.set_xlim(0, 400)
axes.set_ylim(0, 300)
axes.set_aspect("equal")
```

The ball hits the wall in frame 13, with its centre at $(256, 161)$,
about 9.8 pixels from the wall: just inside its radius of 10. The ball never reaches the player, because
the wall is in the way. Each frame moves the ball 15 pixels, a 3, 4, 5 triangle
again, so the check can find a hit up to 15 pixels late. If both were
hit in the same frame, this loop names the wall, because it checks the
wall first. That order is a choice about the game.

</details>

<aside class="dl-note" id="mixed-shapes-note-tennis">

**A ball on a screen in 1958.** On 18 October 1958, visitors to
Brookhaven National Laboratory, in New York, could play Tennis for Two.
William Higinbotham, a physicist there, built it from an analog
computer, and its screen was an oscilloscope about 13 cm across. Each
player hit the ball over a net with a knob and a button.

</aside>

**15. Another way.** In a tower-defence game, two guards walk round a
tower on a circle of radius 50. One is at 20° and the other at 80°. How
far apart are they? Find it two ways: with `point_on_circle` and
`distance`, and with the cosine rule, using the angle between them at
the tower. Can you say why the answer is exactly 50?

<details class="dl-answer"><summary>answer</summary>

```python
first_guard = point_on_circle(50, 20)
second_guard = point_on_circle(50, 80)
print(distance(first_guard, second_guard))

apart_angle = 80 - 20
print(math.sqrt(50 ** 2 + 50 ** 2 - 2 * 50 * 50 * math.cos(math.radians(apart_angle))))
```

Both give 50, apart from the last digit. The tower and the two guards
make a triangle with two sides of 50 and an angle of 60° between them.
The other two angles are equal, and they share the 120° that is left,
so all three are 60°. A triangle with three equal angles has three equal
sides, so the guards are 50 apart, as the 60° triangle on
[Going round in circles](tutorial:going-round-in-circles#exact-values-with-pythagoras)
was.

</details>

**16. Explain.** The checker treats the wall as a line that goes on for
ever. A real wall in a game has two ends. Describe a ball that the
checker would say hits the wall, when on the screen it misses. How
could you change `ball_hits_wall` to fix it, using tools you already
have?

<details class="dl-answer"><summary>answer</summary>

A ball that passes beyond one end of the wall, near the line the wall
would make if it went on, is close to that line but not to the wall.
For a wall from $(0, 300)$ to $(400, 100)$, a ball at $(460, 70)$ is on
the line $x + 2y = 600$, and the checker says it hits, but the wall
stopped at $x = 400$.

Here is one fix. After you find the nearest point, check that it lies between
the two ends, for example with `between` from
[Choosing a path](tutorial:choosing-a-path) on its $x$ (or on its $y$,
for an upright wall). If the nearest point is past an end, the nearest
part of the wall is that end itself, and `distance` from the centre to
the end decides the hit, as if the end were a circle of radius 0.

</details>

## Play it: your checker in a real game

The checker has been answering questions about still pictures. Here it
runs a game you can play. You steer a blue player to a green ring, round
a wall, while an orange ball bounces round the screen. The arrow in the
corner is problem 12's bearing and distance to the goal.

The game comes in two parts. The Python cell below is the level. Its
first lines are the settings, and those are yours to change. The rest
calculates the ball's whole path, frame by frame, with the tools of this
unit: `point_on_circle` turns a speed and an angle into a move, as on
[Going round in circles](tutorial:going-round-in-circles#a-tool-for-any-point-on-a-circle);
`solve_simultaneous` finds the nearest point of the wall, as in problem
8; and `distance` decides every bounce. The cell saves the path in the
page's database, `db`, where the game can read it. The ball starts
near the bottom left, moving at 35°. Before you run it, which does it
reach first, the wall or an edge of the screen?

```python exec
id: mixed-shapes-game-level
import matplotlib.pyplot as plt

# The level: change any of these, run this cell, then press Run on the game.
ball_speed = 4                       # pixels the ball moves each frame
ball_angle = 35                      # degrees, anticlockwise from the right
ball_radius = 10
player_radius = 14
player_start = (40, 250)
goal = (360, 150)
wall_ends = ((170, 40), (250, 230))

# The ball's path, frame by frame. You do not need to change this part.
screen_width, screen_height = 400, 300
wall_a, wall_b = wall_ends
a = wall_b[1] - wall_a[1]            # the wall as a*x + b*y = c, as in problem 7
b = wall_a[0] - wall_b[0]
c = a * wall_a[0] + b * wall_a[1]
wall_length = distance(wall_a, wall_b)


def nearest_on_wall(centre):
    """Return the point of the wall nearest to centre (problems 8 and 16)."""
    p, q = centre
    foot = solve_simultaneous(a, b, c, b, -a, b * p - a * q)
    if close_enough(distance(wall_a, foot) + distance(foot, wall_b), wall_length, tolerance=1e-6):
        return foot                  # the foot is between the two ends
    if distance(centre, wall_a) < distance(centre, wall_b):
        return wall_a
    return wall_b


move_x, move_y = point_on_circle(ball_speed, ball_angle)
x, y = 60, 60
path = []
first_bounce = None
for frame in range(1200):
    x, y = x + move_x, y + move_y
    # An edge straight up or straight across turns one part of the move round.
    if (x < ball_radius and move_x < 0) or (x > screen_width - ball_radius and move_x > 0):
        move_x = -move_x
        first_bounce = first_bounce or ("an edge", frame)
    if (y < ball_radius and move_y < 0) or (y > screen_height - ball_radius and move_y > 0):
        move_y = -move_y
        first_bounce = first_bounce or ("an edge", frame)
    # The slanted wall turns round the part of the move that points at it.
    touch = nearest_on_wall((x, y))
    gap = distance((x, y), touch)
    if 0 < gap <= ball_radius:
        out_x, out_y = (x - touch[0]) / gap, (y - touch[1]) / gap
        towards = move_x * out_x + move_y * out_y
        if towards < 0:
            move_x = move_x - 2 * towards * out_x
            move_y = move_y - 2 * towards * out_y
            first_bounce = first_bounce or ("the wall", frame)
    path.append((frame, x, y))

db.execute("DROP TABLE IF EXISTS ball_path_tbl")
db.execute("CREATE TABLE ball_path_tbl (ball_path_id INTEGER PRIMARY KEY, x REAL, y REAL)")
db.executemany("INSERT INTO ball_path_tbl VALUES (?, ?, ?)", path)
db.execute("DROP TABLE IF EXISTS setting_tbl")
db.execute("CREATE TABLE setting_tbl (setting_id TEXT PRIMARY KEY, value REAL)")
db.executemany("INSERT INTO setting_tbl VALUES (?, ?)", [
    ("ball_radius", ball_radius), ("player_radius", player_radius),
    ("start_x", player_start[0]), ("start_y", player_start[1]),
    ("goal_x", goal[0]), ("goal_y", goal[1]),
    ("wall_ax", wall_a[0]), ("wall_ay", wall_a[1]),
    ("wall_bx", wall_b[0]), ("wall_by", wall_b[1]),
])
db.commit()
print(len(path), "frames saved. The first bounce is off", first_bounce[0], "in frame", first_bounce[1])

path_x = []
path_y = []
for frame, x, y in path[:400]:
    path_x.append(x)
    path_y.append(y)
plt.figure(figsize=(4, 3))
plt.plot(path_x, path_y, color="C1", linewidth=1)
plt.plot([wall_a[0], wall_b[0]], [wall_a[1], wall_b[1]], color="black", linewidth=3)
plt.plot([player_start[0]], [player_start[1]], "o", color="C0", markersize=10)
plt.plot([goal[0]], [goal[1]], "o", color="green", markersize=10)
plt.xlim(0, screen_width)
plt.ylim(0, screen_height)
plt.gca().set_aspect("equal")
```

The ball reaches the wall first, in frame 46. The picture shows the
first 400 frames of its path, before you play the level. Now try the game. Its three panes are the engine,
written in JavaScript, the language of web pages, which
[Many languages, one idea](tutorial:many-languages-one-idea) meets
properly in Unit 10. You do not need to change anything in them. Press
Run on the game, click it (or tap it), and move with the arrow keys or
the buttons under it. The ball starts when you do.

```html app
id: mixed-shapes-game-html
app: shapes-game
<div class="game">
  <canvas width="400" height="300" tabindex="0" aria-label="The game: a blue player, an orange ball, a black wall and a green goal"></canvas>
  <p class="game-status" aria-live="polite">Run the Python cell above, then press Run here.</p>
  <div class="game-pad">
    <button type="button" data-move="left">left</button>
    <button type="button" data-move="up">up</button>
    <button type="button" data-move="down">down</button>
    <button type="button" data-move="right">right</button>
    <button type="button" class="game-again">start again</button>
  </div>
</div>
```

```css app
id: mixed-shapes-game-css
app: shapes-game
.game canvas {
  display: block;
  width: 100%;
  max-width: 400px;
  aspect-ratio: 4 / 3;
  border: 1px solid #888;
  touch-action: none;
}
.game canvas:focus {
  outline: 3px solid #3a7bd5;
}
.game-pad {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-top: 0.4rem;
}
.game-pad button {
  min-width: 3.4rem;
  min-height: 2.6rem;
}
```

```js app
id: mixed-shapes-game-js
app: shapes-game
// The game engine. The level comes from your Python cell, through the
// page's database. JavaScript cannot call your Python functions, so the
// engine has its own copy of three of them: distance, the nearest point
// of the wall, and the bearing.
if (root.dlStopGame) root.dlStopGame();

const canvas = root.querySelector("canvas");
const pen = canvas.getContext("2d");
const status = root.querySelector(".game-status");

let setting;
let path;
try {
  const rows = await dlQuery("SELECT setting_id, value FROM setting_tbl");
  setting = Object.fromEntries(rows.map((row) => [row.setting_id, row.value]));
  path = await dlQuery("SELECT x, y FROM ball_path_tbl ORDER BY ball_path_id");
} catch (error) {
  status.textContent = "Run the Python cell above first, then press Run here again.";
  return;
}

const WIDTH = 400;
const HEIGHT = 300;
const STEP = 2.5;                  // pixels the player moves each frame
const GOAL_RADIUS = 12;
const wallA = [setting.wall_ax, setting.wall_ay];
const wallB = [setting.wall_bx, setting.wall_by];
const goal = [setting.goal_x, setting.goal_y];

function distance(p, q) {
  return Math.hypot(q[0] - p[0], q[1] - p[1]);
}

function nearestOnWall(centre) {
  // How far along the wall the foot of the right-angled line lands,
  // from 0 at one end to 1 at the other, kept between the ends.
  const runX = wallB[0] - wallA[0];
  const runY = wallB[1] - wallA[1];
  let along = ((centre[0] - wallA[0]) * runX + (centre[1] - wallA[1]) * runY) / (runX * runX + runY * runY);
  along = Math.max(0, Math.min(1, along));
  return [wallA[0] + along * runX, wallA[1] + along * runY];
}

function bearing(start, end) {
  const degrees = Math.atan2(end[0] - start[0], end[1] - start[1]) * 180 / Math.PI;
  return (degrees + 360) % 360;
}

function allowed(point) {
  return distance(point, nearestOnWall(point)) > setting.player_radius;
}

let player;
let frame;
let state;
let frames;
const held = new Set();

function startAgain() {
  player = [setting.start_x, setting.start_y];
  frame = 0;
  frames = 0;
  state = "ready";
  status.textContent = "Click the game, then move. Reach the green ring without touching the ball.";
}

function update() {
  if (state === "ready" && held.size > 0) state = "playing";
  if (state !== "playing") return;
  const across = (held.has("right") ? STEP : 0) - (held.has("left") ? STEP : 0);
  const up = (held.has("up") ? STEP : 0) - (held.has("down") ? STEP : 0);
  const r = setting.player_radius;
  const inside = (value, top) => Math.max(r, Math.min(top - r, value));
  // Try the whole move, then only across, then only up: the wall blocks the rest.
  for (const next of [[player[0] + across, player[1] + up], [player[0] + across, player[1]], [player[0], player[1] + up]]) {
    const kept = [inside(next[0], WIDTH), inside(next[1], HEIGHT)];
    if (allowed(kept)) {
      player = kept;
      break;
    }
  }
  frame = (frame + 1) % path.length;
  frames += 1;
  const ball = [path[frame].x, path[frame].y];
  if (distance(player, ball) <= r + setting.ball_radius) {
    state = "hit";
    status.textContent = "The ball touched you after " + (frames / 60).toFixed(1) + " seconds. Press start again.";
  } else if (distance(player, goal) <= r + GOAL_RADIUS) {
    state = "won";
    status.textContent = "You reached the goal in " + (frames / 60).toFixed(1) + " seconds. Press start again to try for less.";
  }
}

function circle(centre, radius, colour) {
  pen.beginPath();
  pen.arc(centre[0], HEIGHT - centre[1], radius, 0, 2 * Math.PI);
  pen.fillStyle = colour;
  pen.fill();
}

function draw() {
  pen.fillStyle = "#f6f4ee";
  pen.fillRect(0, 0, WIDTH, HEIGHT);
  pen.strokeStyle = "#222";
  pen.lineWidth = 5;
  pen.beginPath();
  pen.moveTo(wallA[0], HEIGHT - wallA[1]);
  pen.lineTo(wallB[0], HEIGHT - wallB[1]);
  pen.stroke();
  circle(goal, GOAL_RADIUS, "#2e8b57");
  circle(player, setting.player_radius, "#1f6fb2");
  circle([path[frame].x, path[frame].y], setting.ball_radius, state === "hit" ? "#c0392b" : "#e67e22");
  // The arrow in the corner: which way the goal is, and how far.
  const turn = bearing(player, goal) * Math.PI / 180;
  const tip = [30 + 18 * Math.sin(turn), 30 - 18 * Math.cos(turn)];
  pen.strokeStyle = "#222";
  pen.lineWidth = 3;
  pen.beginPath();
  pen.moveTo(30, 30);
  pen.lineTo(tip[0], tip[1]);
  pen.stroke();
  circle([tip[0], HEIGHT - tip[1]], 4, "#222");
  pen.fillStyle = "#222";
  pen.font = "13px sans-serif";
  pen.fillText(Math.round(bearing(player, goal)) + "°  " + Math.round(distance(player, goal)) + " px", 56, 35);
}

const KEYS = { ArrowLeft: "left", ArrowRight: "right", ArrowUp: "up", ArrowDown: "down" };
canvas.addEventListener("keydown", (event) => {
  if (KEYS[event.key]) {
    event.preventDefault();
    held.add(KEYS[event.key]);
  }
});
canvas.addEventListener("keyup", (event) => held.delete(KEYS[event.key]));
canvas.addEventListener("blur", () => held.clear());
canvas.addEventListener("pointerdown", () => canvas.focus());
for (const button of root.querySelectorAll("[data-move]")) {
  const name = button.dataset.move;
  button.addEventListener("pointerdown", (event) => {
    event.preventDefault();
    held.add(name);
  });
  for (const end of ["pointerup", "pointerleave", "pointercancel"]) {
    button.addEventListener(end, () => held.delete(name));
  }
}
root.querySelector(".game-again").addEventListener("click", () => {
  startAgain();
  canvas.focus();
});

// Sixty steps a second, whatever the screen's own refresh rate.
let handle;
let last = performance.now();
let spare = 0;
function loop(now) {
  if (!canvas.isConnected) return;
  spare = Math.min(spare + now - last, 250);
  last = now;
  while (spare >= 1000 / 60) {
    update();
    spare -= 1000 / 60;
  }
  draw();
  handle = requestAnimationFrame(loop);
}
root.dlStopGame = () => cancelAnimationFrame(handle);
startAgain();
handle = requestAnimationFrame(loop);
```

The ball's path came from your Python, and the game only replays it.
The engine calculates the hits, the goal and the arrow, sixty times a
second.

**17. Predict.** In the level cell, change `ball_speed` to 30 and run
it. Before you look at the picture, predict: will the ball still bounce
off the wall every time it meets it? Then run it, and play.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The wall is a line with no thickness. The ball bounces when its
   centre is within 10 pixels of the wall, at the end of a frame.
2. At 30 pixels a frame, how far can the centre jump in one frame?
3. Think back to the fast ball on
   [How far apart?](tutorial:how-far-apart#watching-it-frame-by-frame).

</details>

<details class="dl-answer"><summary>answer</summary>

Not every time. The picture shows the path going straight through the
wall in places. In 1,200 frames it crosses 26 times. At 4, 8 or 12
pixels a frame, this level's ball never crosses. At 16 it crosses 6
times.

The check runs once a frame. When the ball can move more than its
radius towards the wall in one frame, its centre can land on the far
side of the wall's line. The checker then finds the wall close, but
the ball already moving away from it on that side, so it does not bounce it.
It is the tunnelling from
[How far apart?](tutorial:how-far-apart#watching-it-frame-by-frame),
with a wall in place of a player. One fix is to move a fast ball in
several small steps each frame, and check after each one.

</details>

**18. Explain.** Schlomo, who is learning Python too, reads the engine
and notices that it has its own `distance`, a second copy of the one in
his toolkit. He says it would be simpler to keep one copy, since two
copies can stop agreeing. Why does this page keep two anyway, and how
could you check that they agree?

<details class="dl-answer"><summary>answer</summary>

The engine runs in the browser's own language, JavaScript, sixty times
a second. It cannot call a Python function directly. The two parts share only
the database. So the Python calculates everything it can before the
game starts, which is the ball's path. The JavaScript does what depends
on the keys you press.

The two copies could stop agreeing. If someone changed the Python bounce
rule and not the JavaScript hit rule, the game could show a hit the
Python never predicted. One check: have the Python save a few test
points and their distances to the wall in a table, and have the engine
compare its own answers with them when it starts. There are other
ways too, such as writing the rule once in a form
both languages can read.

</details>
