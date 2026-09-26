---
title: "Time steps: simulating a falling ball, one step at a time"
year: "2026-2027"
version: 2026.09.26.1
covers:
  dropping-a-ball-from-liberty-hall:
    covers: [CMPS-LO3]
  what-one-step-does:
    covers: [CMPS-LO3]
  checking-it-against-a-formula:
    covers: [CMPS-LO7]
    touches: [CMPS-LO11]
  smaller-steps:
    covers: [CMPS-LO3, CMPS-LO13]
  a-ball-that-bounces:
    covers: [CMPS-LO13]
    touches: [CMPS-LO3]
---

# Time steps: simulating a falling ball, one step at a time

In [Simulating a queue](tutorial:when-a-queue-never-clears), time moved
in steps. Each step, some things arrived and the server cleared some.
Most video games move in steps too, usually sixty of them a second, and
so do weather forecasts and simulations of a planet's orbit.

On this page nothing is random. We drop a ball, and we move it forward
in time one step after another. The steps are easy. The interesting
question is how much to trust the answer.

## Dropping a ball from Liberty Hall

Liberty Hall in Dublin is about 60 metres tall. Suppose we drop a ball
from the roof. (Please do not try this.) We ignore the air, so the only
thing acting on the ball is gravity.

Gravity makes a falling thing faster by 9.8 metres per second, every
second. We write the ball's speed with a sign, to show its direction:
positive when it moves up, and negative when it moves down. A speed with
a direction like this is called a *velocity*. A ball falling at 20 metres
a second has a velocity of −20.

Here is a loop that moves the ball forward one second at a time.

```python exec
id: dropping-a-ball-from-liberty-hall-1
height = 60       # metres above the street
velocity = 0      # metres per second; the ball starts still
gravity = -9.8    # the change in velocity over one second
step = 1          # seconds

time = 0
while height > 0:
    height = height + velocity * step
    velocity = velocity + gravity * step
    time = time + step
    print(f"after {time} s: {height:.1f} m up, velocity {velocity:.1f} m/s")
```

```predict
type: choice

Before you run it: how many seconds does the ball take to reach the
street?

- About 2 seconds
  - 60 metres is not very far, and gravity is strong.
- About 3 or 4 seconds
- About 6 seconds
  - 60 metres at 9.8 metres a second takes about 6 seconds.
- More than 10 seconds
```

Look at the first line of the output. After one whole second, the ball
is still 60 metres up. It has not moved at all. Then it falls faster and
faster, and after 5 seconds it is at −38.0 metres: 38 metres under the
street. The loop only looks at the ball between steps, so it never saw
the moment the ball hit the ground.

Remember both of those strange things. They have the same cause.

## What one step does

Let's see what changes the answer. What happens when `gravity` is
`-1.6`, about the pull at the surface of the Moon? What happens when the
ball starts with `velocity = 10`, thrown upwards?

<details class="dl-answer"><summary>What each line does</summary>

- `height = height + velocity * step` moves the ball. Distance is
  velocity times time, so in one step the ball moves `velocity * step`
  metres. When the velocity is negative, the height gets smaller.
- `velocity = velocity + gravity * step` changes the velocity. Gravity
  adds −9.8 metres per second for every second, so in one step it adds
  `gravity * step`.
- `time = time + step` counts the seconds.
- `while height > 0:` checks the height once per step, before the next
  step begins.

</details>

The first line of the loop moves the ball using the velocity it has at
the start of the step. In the first step that velocity is 0, so the
ball does not move. In a real fall, the ball gets faster during the
whole second. The loop acts as if the velocity stays the same for the
whole step, and then changes it all at once at the end.

Every step works this way. We pretend that nothing changes during one
short piece of time. Then we move everything forward, and pretend again
for the next piece. The length of each piece is called the *time step*.
Here it is 1 second. A game that draws sixty pictures a second uses a
time step of 1/60 of a second.

This way of stepping forward is called *Euler's method*, after Leonhard
Euler, who described it in 1768. It is the simplest method there is for
moving a simulation forward in time, and it is still the first one that
most programmers write.

## Checking it against a formula

For a falling ball, we are lucky. There is a formula for the height at
any moment, from physics. After $t$ seconds of falling from 60 metres,
the height is

$$\text{height} = 60 - 4.9\,t^2$$

The 4.9 is half of 9.8. The ball reaches the street when the height is
0, so when $4.9\,t^2 = 60$.

```python exec
id: checking-it-against-a-formula-1
import math

landing = math.sqrt(60 / 4.9)
print(f"the formula says the ball lands after {landing:.2f} seconds")
```

The formula says 3.50 seconds. The loop said 5. Which one should we
believe?

Both answers come from the same model (as in
[The perceptron](tutorial:a-model-that-corrects-itself)): a ball that
starts still, gets faster by 9.8 metres per second every second, and
meets no air. The formula gets its answer from the model exactly, in one
calculation. The loop is a simulation of the same model. It runs the
model forward step by step, and each step starts from where the last one
finished. The model is the same in both, so the gap between 3.5 and 5
comes from the steps, not from the physics.

The next cell draws both answers on one graph: the formula as a curve,
and the loop's steps as dots.

```python exec
id: checking-it-against-a-formula-2
import matplotlib.pyplot as plt

times = [t / 100 for t in range(0, 351)]
plt.plot(times, [60 - 4.9 * t * t for t in times], label="the formula")

height, velocity, time = 60, 0, 0
heights, moments = [height], [time]
while height > 0:
    height = height + velocity * 1
    velocity = velocity - 9.8 * 1
    time = time + 1
    heights.append(height)
    moments.append(time)
plt.plot(moments, heights, "o--", label="steps of 1 second")
plt.axhline(0, color="grey")
plt.xlabel("seconds")
plt.ylabel("height (m)")
plt.legend()
```

The dots stay above the curve the whole way down. The loop's ball falls
too slowly, because each step uses the velocity from the start of the
step, and a falling ball is always faster at the end of a step than at
the start.

We can check a simulation against a case where we already know the
answer. This is one of the most useful checks we can do. A simulation
that fails this test will not be trusted anywhere else. Most simulations
are built for cases with no formula at all, and a check like this one
gives us a reason to believe them there.

## Smaller steps

If the trouble is that each step is too long, we can try shorter ones.
The function below runs the same loop with any time step, and returns
the time when the ball reaches the street. It counts the steps and
multiplies at the end. That way, many small numbers added together never
blur the time.

```python exec
id: smaller-steps-1
def landing_time(step):
    height = 60
    velocity = 0
    steps = 0
    while height > 0:
        height = height + velocity * step
        velocity = velocity - 9.8 * step
        steps = steps + 1
    return steps * step

print(f"{landing_time(1):.2f}")
```

```predict
type: number
tolerance: 0.05

With a time step of 0.1 seconds, what landing time do you expect?
After you have guessed, change the `1` in the last line to `0.1`.
```

Now we ask the same question for four time steps, each ten times shorter
than the one before.

```python exec
id: smaller-steps-2
for step in [1, 0.1, 0.01, 0.001]:
    answer = landing_time(step)
    steps_taken = round(answer / step)
    off_by = answer - landing
    print(f"step {step:<6} lands {answer:.4f} s,",
          f"off by {off_by:.4f} s, {steps_taken} steps")
```

Read the "off by" column from the top down: 1.5, then 0.1, then 0.01,
then less than 0.001. The answer is always a little late, by about one
time step. Make the step ten times shorter and the answer gets about ten
times closer.

The last column is the cost. Ten times shorter steps means ten times as
many of them, and each one is work for the computer.

Compare this with the darts in
[Monte Carlo simulation](tutorial:counting-darts). There, one more
correct decimal place needed about a hundred times as many darts. Here it
needs ten times as many steps. For the same extra work, Euler's method
gains far more than darts do, and there are methods that gain more
still.

Notice also what kind of error this is. Every run with the same step
gives exactly the same answer, and it is always late. In the words of
the darts page, the error is all in the accuracy. If you run it again,
nothing changes. Only a better method, or a shorter step, moves the
answer closer.

### Your turn

Suppose we want a landing time that is off by less than a thousandth of
a second.

1. Before you run anything, what time step do you expect that to need?
2. How many steps will the loop take?
3. Then try it, and look at the "off by" column.

```python exec
id: smaller-steps-3
```

```hint
after: 2 unchanged runs
The error was about the size of one time step. What time step is about
the size of a thousandth of a second? Try `landing_time` with it, and
subtract `landing`.
```

## A ball that bounces

A ball that stops at the street is a short simulation. Let's make it
bounce. When the ball goes below the street, we set its height to 0 and
flip the sign of its velocity, so that it moves up instead of down. A real ball
loses some speed in each bounce, so we multiply by a number that says
how bouncy it is: 1 keeps all the speed, and 0.8 keeps four fifths of it.

```python exec
id: a-ball-that-bounces-1
def bounce_heights(step, seconds, bounciness):
    height = 60
    velocity = 0
    heights = []
    for _ in range(round(seconds / step)):
        height = height + velocity * step
        velocity = velocity - 9.8 * step
        if height < 0:
            height = 0
            velocity = -velocity * bounciness
        heights.append(height)
    return heights

heights = bounce_heights(0.01, 20, 0.8)
times = [i * 0.01 for i in range(len(heights))]
plt.plot(times, heights)
plt.xlabel("seconds")
plt.ylabel("height (m)")
```

That looks like a bouncing ball. Each bounce is lower than the one
before, since each one keeps only four fifths of the speed.

Now we try a ball that is perfectly bouncy, with `bounciness` of 1. A
real ball like that, dropped from 60 metres, would climb to 60 metres
again after every bounce, and never higher, because nothing gives it any
extra speed.

```python exec
id: a-ball-that-bounces-2
heights = bounce_heights(0.1, 40, 1.0)
times = [i * 0.1 for i in range(len(heights))]
plt.plot(times, heights)
plt.axhline(60, color="grey", linestyle="--")
plt.xlabel("seconds")
plt.ylabel("height (m)")
print(f"highest point: {max(heights):.1f} m")
```

```predict
type: choice

With a time step of 0.1 seconds, what will the perfectly bouncy ball do
over 40 seconds?

- Climb to 60 metres again after every bounce
  - Nothing in the model adds speed or takes it away.
- Climb a little less high after each bounce
  - Every simulation loses a little on each step.
- Climb a little higher after each bounce
```

The ball climbs higher after every bounce: 65 metres, then 69, and by
the end of 40 seconds it reaches 80.4 metres. Nothing in the model gives
the ball any extra speed. The simulation has invented it.

The cause is the one we saw at the start of the page. Each step uses the
velocity from the start of the step, so the ball falls a little too
slowly and reaches the floor a little late. All that extra time, gravity
has been making it faster. So it hits the floor faster than a real ball
dropped from 60 metres, and bounces higher. The next fall starts higher,
so it hits even faster. The error in each step is small, but it is
always in the same direction, so it grows.

This is the other half of the lesson about time steps. A small error in
one step can grow over many steps. A simulation that looks fine for 5
seconds can be far from the truth after 40. A game with a ball that
bounces higher and higher is showing you exactly this.

### Your turn

Can you find a time step that keeps the perfectly bouncy ball within one
metre of 60 metres, for the whole 40 seconds? How many steps does that
take?

```python exec
id: a-ball-that-bounces-3
heights = bounce_heights(0.1, 40, 1.0)
print(f"highest point: {max(heights):.1f} m")
```

```hint
after: 2 unchanged runs
Which number in the first line is the time step? Try making it ten times
shorter, and then ten times shorter again. How many steps is 40 seconds
at each one?
```

## Looking back

The formula and the loop gave different answers for the same falling
ball, and the loop came closer only when its steps got shorter. For a
ball, we had a formula to check against. How would you decide how far to
trust a simulation of something with no formula at all, like the weather
next Tuesday?

Here is a challenge. Real balls meet air. Air slows a ball down more when it
moves faster. Can you add air to the falling ball, so that each step
also removes a little of the velocity? What happens to the landing
time? Does the ball reach a speed that it never goes faster than? The
formula on this page cannot answer that question, and the simulation
can.

```python challenge
# A falling ball with air. The model: each step, the air removes a
# small fraction of the velocity. drag is not used yet: where in the
# loop does it belong?
height = 60
velocity = 0
gravity = -9.8
drag = 0.1
step = 0.01

time = 0
while height > 0:
    height = height + velocity * step
    velocity = velocity + gravity * step
    time = time + step
print(f"lands after {time:.2f} s, at {velocity:.1f} m/s")
```

## Where to read more

Fiedler, G. (2004). *Integration Basics.* Gaffer On Games.
<https://gafferongames.com/post/integration_basics/>. A game programmer
explains the step on this page, the error in it, and the small change
most games make to it. It is written for programmers, not
mathematicians.

MinuteLabs.io (2020). *Let's Build a Physics Simulation (PONG: Part 1).*
<https://www.youtube.com/watch?v=gNA6HKRWAI0>. Jasper Palfree builds a
moving ball in JavaScript from nothing, then makes it bounce off the
walls of the screen. It is the same stepping forward in time as this
page, drawn sixty times a second. It is 41 minutes long.

Sebastian Lague (2023). *Coding Adventure: Simulating Fluids.*
<https://www.youtube.com/watch?v=rSKMYc1CQHE>. His simulation starts
with one particle falling and bouncing inside a box, one time step at a
time. Then he adds thousands more, and a few rules about how they push
on each other, until they move like water. It is 48 minutes long.

Patrick J (2010). *Euler's Method for Differential Equations: The Basic
Idea.* <https://www.youtube.com/watch?v=RGtCw5E7gBc>. It shows the same
method on paper, for a reader who wants the mathematics behind it. It is
12 minutes long.
