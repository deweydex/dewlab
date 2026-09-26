def test_a_dive_goes_down():
    sub = Submarine("Nautilus")
    sub.dive(100)
    assert sub.get_depth() == 100

def test_a_dive_to_exactly_the_limit_is_allowed():
    sub = Submarine("Nautilus")
    sub.dive(400)
    assert sub.get_depth() == 400

def test_rise_refuses_a_negative_number():
    sub = Submarine("Nautilus")
    sub.rise(-500)
    assert sub.get_depth() == 0

def test_a_bathyscaphe_goes_deeper():
    trieste = Bathyscaphe("Trieste")
    trieste.dive(10916)
    assert trieste.get_depth() == 10916

def test_the_deepest_submarine():
    deep_blue = Expedition("Deep Blue")
    nautilus = Submarine("Nautilus")
    trieste = Bathyscaphe("Trieste")
    deep_blue.add(nautilus)
    deep_blue.add(trieste)
    trieste.dive(5000)
    assert deep_blue.deepest() == trieste
