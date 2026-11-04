---
title: "The seasons: a closer look at the Earth and the Sun"
year: "2026-2027"
version: 2026.11.04.3
---

# The seasons: a closer look at the Earth and the Sun

In [Sine and cosine waves](tutorial:sine-and-cosine-waves#where-a-wave-comes-from),
the hours of daylight in Dublin made a wave through the year. The page
said the Earth's axis is tilted. A different reason is often given for
summer and winter. Here are two ideas. Both are reasonable, and they
cannot both be true.

**Idea A.** The Earth's path round the Sun is not a perfect circle.
Summer is when the Earth is closest to the Sun, and winter is when it is
furthest away.

**Idea B.** The distance changes a little, but that is not the reason.
The tilt makes our half of the Earth lean towards the Sun for half the
year, with a higher sun and longer days, and away from it for the other
half.

## An experiment

Idea A predicts that the Earth is closest to the Sun in June or July, in
the Irish summer, and furthest in December or January. Idea B says the
distance is not the reason, so the closest month could be any month.

The cell draws two waves, one above the other: the daylight in Dublin, and
the distance from the Earth to the Sun through the year.

```python exec
id: an-experiment-1
import math
import matplotlib.pyplot as plt

months = list(range(12))     # 0 = January
daylight = [7.8, 9.5, 11.6, 13.8, 15.8, 16.9, 16.4, 14.7, 12.6, 10.5, 8.6, 7.4]
distance = [149.6 - 2.5 * math.cos(month / 12 * 2 * math.pi) for month in months]

fig, (top, bottom) = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
top.plot(months, daylight, "o-")
top.set_ylabel("daylight in Dublin (hours)")
bottom.plot(months, distance, "o-", color="darkorange")
bottom.set_ylabel("Earth to Sun (million km)")
bottom.set_xlabel("month (0 = January)")
```

```predict
type: choice

In which month is the Earth closest to the Sun?

- June or July
  - This is what idea A predicts: closest in summer.
- December or January
  - This reads the closest point as falling in winter.
- March or September
  - This reads the closest point as falling between the seasons.
```

Run it. The distance curve comes from NASA's two numbers: the closest
distance is 147.1 million km, in early January, and the furthest is 152.1
million km, in early July. The months in between follow a wave, like the
daylight did.

The Earth is closest in January, in the middle of the Irish winter, and furthest in July, in summer. The
two waves are almost upside down from each other. Idea A predicted the opposite, so the distance
cannot be what makes Irish summers warm. Idea B matches what happens.

Here is a second test. Sydney, in Australia, is in the southern half of
the Earth. It is the same distance from the Sun as Dublin on any day. Idea
A says its seasons should match Dublin's. What does idea B say? Can you
find when summer is in Sydney?

<details class="dl-answer"><summary>what idea B says, and what happens</summary>

Idea B says the southern half leans towards the Sun when the northern half
leans away. So Sydney's summer should be in December and January. It is:
Christmas in Sydney is in summer. The same distance, on the same day,
gives opposite seasons.

</details>

## What each idea counts

Idea A counts the distance from the Earth to the Sun. Idea B counts the
height of the sun in the sky, which the tilt changes through the year.

Each one changes the sunlight on the ground. We can put a number on both.
The closest and furthest distances are only about 3% apart. Sunlight gets
weaker as the distance grows: twice as far gives a quarter of the light.
So the distance changes the sunlight reaching the Earth by about 7%.

The tilt changes the height of the sun much more. At midday in June, the
sun over Dublin is about 60° above the horizon. At midday in December it
is about 13°. When the sun is low, the same sunlight is spread over more
ground.

```python exec
id: why-idea-a-feels-right-1
import math

distance_effect = (152.1 / 147.1) ** 2
tilt_effect = math.sin(math.radians(60.1)) / math.sin(math.radians(13.2))
print("closest against furthest:", round(distance_effect, 2), "times the sunlight")
print("June sun against December sun, in Dublin:", round(tilt_effect, 1), "times")
```

The distance changes the sunlight by about 1.07 times. The height of the
sun changes the sunlight on each square metre of Dublin by about 3.8
times, and the days are more than twice as long as well.

The next cell lets us move the height of the sun. The curve shows the
share of the overhead sunlight that lands on each square metre of ground.
The dot marks the height we chose.

```python exec
id: what-each-idea-counts-2
import math
import matplotlib.pyplot as plt

height = slider("height of the sun (degrees)", 5, 90, step=1, value=13, id="sun-height").value

heights = list(range(5, 91))
share = [math.sin(math.radians(angle)) for angle in heights]
fig, ax = plt.subplots()
ax.plot(heights, share)
ax.plot([height], [math.sin(math.radians(height))], "o")
ax.set_xlim(0, 90)
ax.set_ylim(0, 1.05)
ax.set_xlabel("height of the sun above the horizon (degrees)")
ax.set_ylabel("share of the overhead sunlight")
ax.grid(alpha=0.3)
print(f"at {height} degrees: {math.sin(math.radians(height)):.2f} of the overhead sunlight")
```

Can you find a height where each square metre gets half of the overhead
sunlight? How does that height compare with the sun in a Dublin
December?

## Where else it happens

The Moon has the same kind of path, closer at some times and further at
others. A "supermoon" is a full moon near its closest point. It looks
bigger in photos, but most people looking up could not see a difference
between it and an ordinary full moon. A change of several percent in
distance is a small change.

## Where to read more

NASA's Space Place explains the seasons with pictures:
[What causes the seasons?](https://spaceplace.nasa.gov/seasons/)
