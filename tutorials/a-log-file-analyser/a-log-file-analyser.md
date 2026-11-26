---
title: "A Log-File Analyser: Who Keeps Failing to Log In?"
year: "2026-2027"
version: 2026.11.26.1
covers:
  1-plan-first:
    covers: [PDP-LO5]
  3-week-two-counting-by-address:
    covers: [PDP-LO2, PDP-LO6]
  4-week-three-a-report:
    covers: [PDP-LO7]
---

# A Log-File Analyser: Who Keeps Failing to Log In?

Servers and routers write a log: a line of text for every event, such as a login that worked or one that failed. A busy server writes thousands of lines a day, and nobody reads them all. People write small programs that read the log for them and report what matters. On this page we build one that finds addresses with many failed logins, which is often the first sign of an attack.

The project has three stages, about one week each. Each stage ends with a program that works.

There are questions on this page to answer in words as well as in code. The **+ Text** button between cells adds a text cell where you can write your answers.

## 1. Plan First

```python exec
id: plan-first-1
log = [
    "2026-11-26 09:14:02 LOGIN OK user=grace ip=10.0.0.12",
    "2026-11-26 09:15:40 LOGIN FAIL user=admin ip=10.0.0.99",
    "2026-11-26 09:15:41 LOGIN FAIL user=admin ip=10.0.0.99",
    "2026-11-26 09:15:43 LOGIN FAIL user=root ip=10.0.0.99",
    "2026-11-26 09:20:05 LOGIN FAIL user=linus ip=10.0.0.7",
    "2026-11-26 09:20:11 LOGIN OK user=linus ip=10.0.0.7",
    "2026-11-26 09:31:58 LOGIN FAIL user=admin ip=172.16.4.2",
    "2026-11-26 09:32:00 LOGIN FAIL user=admin ip=10.0.0.99",
    "2026-11-26 09:40:17 LOGIN OK user=ada ip=10.0.0.15",
]
```

**1.1** Run the cell above, and read the log yourself. Which address looks suspicious? What makes it look that way?

<!-- answer -->

**1.2** You found the suspicious address with your eyes. Write the steps you followed as pseudocode, so a program could follow them on a log of ten thousand lines.

<!-- answer -->

## 2. Week One: Taking a Line Apart

**2.1** Predict what each line prints, then run the cell.

```python exec
id: week-one-taking-a-line-apart-1
line = log[1]
parts = line.split()
print(parts)
print(parts[3])
print(parts[5])
print(parts[5].split("="))
print(parts[5].split("=")[1])
```

<!-- answer -->

**2.2** Count the failed logins in the whole log. Then count the logins that worked.

```python exec
id: week-one-taking-a-line-apart-2
# your counts here
```

```solution
failed = 0
worked = 0
for line in log:
    if line.split()[3] == "FAIL":
        failed = failed + 1
    else:
        worked = worked + 1
print(failed, "failed and", worked, "worked")
```

**2.3** Write `ip_of(line)`, which hands back the address in a line. Use it to print the address of every failed login.

```python exec
id: week-one-taking-a-line-apart-3
def ip_of(line):
    # your code here
    return ""

print(ip_of(log[0]) == "10.0.0.12")
```

```solution
def ip_of(line):
    return line.split()[5].split("=")[1]

print(ip_of(log[0]) == "10.0.0.12")
```

## 3. Week Two: Counting by Address

**3.1** Build two lists that stay in step: `addresses` holds each address once, and `fail_counts` holds the number of failed logins for that address. For each failed line, add 1 to its address's count, or add the address with a count of 1 if it is new.

```python exec
id: week-two-counting-by-address-1
addresses = []
fail_counts = []
# your loop here
print(addresses)
print(fail_counts)
```

```solution
addresses = []
fail_counts = []
for line in log:
    if line.split()[3] == "FAIL":
        address = ip_of(line)
        if address in addresses:
            position = addresses.index(address)
            fail_counts[position] = fail_counts[position] + 1
        else:
            addresses.append(address)
            fail_counts.append(1)
print(addresses)
print(fail_counts)
```

**3.2** Print every address with three or more failed logins. Make the number 3 a variable, so it is easy to change.

<!-- answer -->

**3.3** Count the failed logins by username in the same way. Which usernames do attackers try most? Why might those be the ones?

<!-- answer -->

## 4. Week Three: A Report

**4.1** Write a command line with commands such as `summary`, `suspects`, `user` (all lines for one username) and `ip` (all lines for one address).

<!-- answer -->

**4.2** In the log above, `10.0.0.99` failed three times in three seconds. A person cannot type that fast. Take the time from each line, and find addresses that fail more than once within ten seconds. The time `09:15:41` is `9 * 3600 + 15 * 60 + 41` seconds after midnight.

<!-- answer -->

**4.3** Add a note at the top of your program for the person who runs it: what it reads, what each command reports, and what the threshold means.

<!-- answer -->

## 5. Release and Review

**5.1** Write ten more log lines yourself, with an attack hidden in them. Swap logs with another pair. Does their program find your attack? Does yours find theirs?

<!-- answer -->

**5.2** Add a line that does not follow the pattern, such as an empty line or `SERVER RESTART`. Does your program crash? Where should it check?

<!-- answer -->

## 6. More to Try

1. Sort the suspects so the address with the most failures comes first.
2. Draw a bar chart of failures by hour, using `#` symbols.
3. Report usernames that logged in from more than one address.
4. Mark each address as private or public, using the rules from the IP address tool.

```python exec
id: more-to-try-1
# your experiments here
```
