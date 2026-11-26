---
title: "An IP Address Tool: Checking, Converting and Comparing Addresses"
year: "2026-2027"
version: 2026.11.26.1
covers:
  1-plan-first:
    covers: [PDP-LO6]
  2-week-one-is-this-a-valid-address:
    covers: [PDP-LO2, PDP-LO10]
  4-week-three-the-same-network:
    covers: [PDP-LO8]
---

# An IP Address Tool: Checking, Converting and Comparing Addresses

An IPv4 address such as `192.168.1.20` is four whole numbers from 0 to 255, joined by dots. Network engineers check addresses, turn them into binary, and ask whether two addresses are on the same network. On this page we build a small tool that does all three.

The project has three stages, about one week each. Each stage ends with a tool that works. In this project, each job goes in its own function, and the function hands back an answer instead of printing it. That way you can test each function on its own, before any `input` is involved.

There are questions on this page to answer in words as well as in code. The **+ Text** button between cells adds a text cell where you can write your answers.

## 1. Plan First

**1.1** Write down five strings that are valid addresses and five that are not. Try to make each invalid one wrong in a different way.

<!-- answer -->

**1.2** Write pseudocode for checking an address: the steps in plain words, one to a line, that decide whether a string is a valid address.

<!-- answer -->

## 2. Week One: Is This a Valid Address?

**2.1** Predict what each line prints, then run the cell.

```python exec
id: week-one-is-this-a-valid-address-1
parts = "192.168.1.20".split(".")
print(parts)
print(len(parts))
print("20".isdigit(), "-3".isdigit(), "".isdigit())
print(int("020"))
```

<!-- answer -->

**2.2** Write a function `is_valid(address)` that hands back `True` for a valid address and `False` for anything else. The test cell under it should print `True` on every line.

```python exec
id: week-one-is-this-a-valid-address-2
def is_valid(address):
    # your code here
    return False
```

```python exec
id: week-one-is-this-a-valid-address-3
print(is_valid("192.168.1.20") == True)
print(is_valid("10.0.0.1") == True)
print(is_valid("192.168.1.300") == False)
print(is_valid("192.168.1") == False)
print(is_valid("a.b.c.d") == False)
print(is_valid("") == False)
```

<details class="dl-hint"><summary>smaller steps</summary>

1. Split the address on dots. If there are not four parts, hand back `False`.
2. Loop over the parts. If a part is not all digits, hand back `False`.
3. Turn the part into an `int`. If it is bigger than 255, hand back `False`.
4. If the loop finishes without finding a problem, hand back `True`.

</details>

```solution
def is_valid(address):
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        if int(part) > 255:
            return False
    return True

print(is_valid("192.168.1.20") == True)
print(is_valid("192.168.1.300") == False)
```

**2.3** Add two tests of your own to the test cell, from your list in 1.1. Does your function pass them?

<!-- answer -->

**2.4** Should `192.168.001.20` be valid? Real tools disagree about this. Decide, and add a test that shows your decision.

<!-- answer -->

**2.5** Wrap your function in a small command line that asks for an address and says whether it is valid, until the person types `exit`.

```python exec
id: week-one-is-this-a-valid-address-4
# your command line here
```

## 3. Week Two: Addresses in Binary

**3.1** Predict what each line prints, then run the cell. What does `zfill(8)` do?

```python exec
id: week-two-addresses-in-binary-1
print(bin(192))
print(bin(192)[2:])
print(bin(5)[2:])
print(bin(5)[2:].zfill(8))
print(int("11000000", 2))
```

<!-- answer -->

**3.2** Write `to_binary(address)`, which hands back the address as four groups of eight digits, like `11000000.10101000.00000001.00010100`.

```python exec
id: week-two-addresses-in-binary-2
def to_binary(address):
    # your code here
    return ""

print(to_binary("192.168.1.20"))
```

```solution
def to_binary(address):
    groups = []
    for part in address.split("."):
        groups.append(bin(int(part))[2:].zfill(8))
    return ".".join(groups)

print(to_binary("192.168.1.20"))
```

**3.3** A network written as `/24` has a mask of 24 ones followed by 8 zeros. Write `mask_from_prefix(prefix)`, which hands back the mask in the usual dotted form. `mask_from_prefix(24)` should hand back `"255.255.255.0"`.

```python exec
id: week-two-addresses-in-binary-3
def mask_from_prefix(prefix):
    # your code here
    return ""

print(mask_from_prefix(24))
print(mask_from_prefix(16))
print(mask_from_prefix(20))
```

<details class="dl-hint"><summary>smaller steps</summary>

1. Build a string of 32 digits: `"1" * prefix` and then enough zeros.
2. Cut it into four slices of eight: `bits[0:8]`, `bits[8:16]`, and so on.
3. Turn each slice back into a number with `int(slice, 2)`, and join them with dots.

</details>

```solution
def mask_from_prefix(prefix):
    bits = "1" * prefix + "0" * (32 - prefix)
    numbers = []
    for start in range(0, 32, 8):
        numbers.append(str(int(bits[start:start + 8], 2)))
    return ".".join(numbers)

print(mask_from_prefix(24))
print(mask_from_prefix(20))
```

## 4. Week Three: The Same Network?

Two addresses are on the same network when the first `prefix` binary digits of each are the same. For `/24`, those are the first three numbers.

**4.1** By hand, decide whether `192.168.1.20` and `192.168.1.200` are on the same `/24` network. What about `192.168.1.20` and `192.168.2.20`? What about the same pair on a `/16` network?

<!-- answer -->

**4.2** Write `same_network(first, second, prefix)`. You can use `to_binary`, remove the dots with `replace(".", "")`, and compare slices.

```python exec
id: week-three-the-same-network-1
def same_network(first, second, prefix):
    # your code here
    return False

print(same_network("192.168.1.20", "192.168.1.200", 24) == True)
print(same_network("192.168.1.20", "192.168.2.20", 24) == False)
print(same_network("192.168.1.20", "192.168.2.20", 16) == True)
```

```solution
def same_network(first, second, prefix):
    first_bits = to_binary(first).replace(".", "")
    second_bits = to_binary(second).replace(".", "")
    return first_bits[:prefix] == second_bits[:prefix]

print(same_network("192.168.1.20", "192.168.1.200", 24) == True)
print(same_network("192.168.1.20", "192.168.2.20", 16) == True)
```

**4.3** A `/24` network has 2 to the power 8 addresses, but two of them are kept for the network itself and for broadcast. Write `host_count(prefix)`. How many hosts fit on a `/24`, a `/30` and a `/16`?

<!-- answer -->

**4.4** Join your functions into one command line, with a command for each job: `check`, `binary`, `mask`, `same` and `hosts`. Each command asks for what it needs and calls a function.

```python exec
id: week-three-the-same-network-2
# your tool here
```

## 5. Release and Review

**5.1** Swap tools with another pair. Each pair tries to make the other's tool crash. Which inputs crashed it? Which function should have caught them?

<!-- answer -->

**5.2** Every function on this page could be tested without typing anything. Why does that make testing faster? Which part of your program could not be tested that way?

<!-- answer -->

## 6. More to Try

1. Say whether an address is private. The private ranges start with `10.`, `192.168.`, or `172.16.` up to `172.31.`.
2. Given an address and a prefix, print the network address and the broadcast address.
3. Accept the address and prefix together, like `192.168.1.20/24`.
4. Draw the binary form with the network part and the host part in different symbols, so the split is easy to see.

```python exec
id: more-to-try-1
# your experiments here
```
