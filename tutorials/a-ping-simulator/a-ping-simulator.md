---
title: "A Ping Simulator: A Pretend Network That Answers Back"
year: "2026-2027"
version: 2026.11.26.1
covers:
  1-plan-first:
    covers: [PDP-LO6]
  2-week-one-one-ping:
    covers: [PDP-LO8]
  3-week-two-many-pings-and-their-statistics:
    covers: [PDP-LO6]
---

# A Ping Simulator: A Pretend Network That Answers Back

The command `ping` sends a small message to another machine and waits for a reply. It reports how long each reply took, in milliseconds, and how many messages were lost. A program in this notebook cannot send real messages, so on this page we build a pretend network instead. Our devices answer with random delays, some lose messages, and some are switched off. The output looks like the real command.

The project has three stages, about one week each. Each stage ends with a program that works.

There are questions on this page to answer in words as well as in code. The **+ Text** button between cells adds a text cell where you can write your answers.

## 1. Plan First

**1.1** If you have used `ping` on a real computer, write down what its output looked like. If you have not, here is an example of the kind of output it gives.

```text
PING 10.0.0.1: 56 data bytes
64 bytes from 10.0.0.1: icmp_seq=0 ttl=64 time=2.104 ms
64 bytes from 10.0.0.1: icmp_seq=1 ttl=64 time=1.877 ms
Request timeout for icmp_seq 2
64 bytes from 10.0.0.1: icmp_seq=3 ttl=64 time=2.311 ms

4 packets transmitted, 3 packets received, 25.0% packet loss
```

Which parts of the output change from line to line? Which parts stay the same?

<!-- answer -->

**1.2** Our pretend network needs a list of devices. For each device, what does the program need to know? Write a short list.

<!-- answer -->

## 2. Week One: One Ping

```python exec
id: week-one-one-ping-1
import random

names = ["gateway", "switch-1", "printer", "server"]
addresses = ["10.0.0.1", "10.0.0.2", "10.0.0.30", "10.0.0.50"]
switched_on = [True, True, False, True]
loss_chance = [0.0, 0.1, 0.0, 0.3]
```

**2.1** Run the cell above. Then predict what this prints, and run it several times.

```python exec
id: week-one-one-ping-2
print(random.random())
print(random.random() < 0.3)
print(round(random.uniform(1, 5), 3))
```

<!-- answer -->

**2.2** Write `ping_once(address)`, which hands back a delay in milliseconds, or `None` if the message was lost. A device that is switched off never answers. A device that is on loses a message when `random.random()` is less than its loss chance.

```python exec
id: week-one-one-ping-3
def ping_once(address):
    # your code here
    return None

print(ping_once("10.0.0.1"))
print(ping_once("10.0.0.30"))
print(ping_once("10.9.9.9"))
```

```solution
def ping_once(address):
    if address not in addresses:
        return None
    position = addresses.index(address)
    if not switched_on[position]:
        return None
    if random.random() < loss_chance[position]:
        return None
    return round(random.uniform(1, 5), 3)

print(ping_once("10.0.0.1"))
print(ping_once("10.0.0.30"))
```

**2.3** Run the test cell many times. Which device always answers? Which never answers? Which answers sometimes?

<!-- answer -->

## 3. Week Two: Many Pings and Their Statistics

**3.1** Write a command `ping` that asks for an address and calls `ping_once` four times. It prints a line for each reply or timeout in the style of the real output.

<!-- answer -->

**3.2** After the four lines, print the summary: how many were sent, how many came back, and the packet loss as a percentage. Then add the smallest, largest and average delay.

<!-- answer -->

<details class="dl-hint"><summary>smaller steps</summary>

1. Keep the delays that came back in a list.
2. `len` of that list is the number received.
3. `min`, `max` and `sum` work on a list of numbers.
4. What should the summary say when no replies came back at all?

</details>

**3.3** Let the person ping a name such as `server` as well as an address. Where in the code does the name become an address?

<!-- answer -->

## 4. Week Three: The Network Changes

**4.1** Add commands that change the network: `off` and `on` switch a device, and `add` creates a new device with a name, an address and a loss chance. Use your `is_valid` function from the IP address tool if you built it.

<!-- answer -->

**4.2** Add a command `scan` that pings every device once and prints a table of which ones answered. Draw it neatly, with the names in a straight column.

<!-- answer -->

**4.3** A real network has routers between you and a far machine. Add a list of hops for the server, such as the gateway, then switch-1, then the server, and a command `trace` that pings each hop in order. What should it print when a hop in the middle does not answer?

<!-- answer -->

## 5. Release and Review

**5.1** Your program uses random numbers, so it gives different output every time. How can you test it? Try `random.seed(1)` at the top, and run it twice. What changes?

<!-- answer -->

**5.2** Ask another pair to use your simulator as if it were a real network. Which part did not behave like the real command?

<!-- answer -->

## 6. More to Try

1. Give each device a typical delay, so far devices are slower than near ones.
2. Add `ping -c 10` to choose how many pings to send.
3. Keep a history of every ping, and draw the delays for one device as a row of bars.
4. On a computer with Python installed, look up the `subprocess` module and run the real `ping` command. Compare its output with your simulator's.

```python exec
id: more-to-try-1
# your experiments here
```
