def test_a_hit_takes_health():
    ada = Character("Ada", 10)
    ada.take_damage(3)
    assert ada.get_health() == 7

def test_a_hit_to_exactly_zero_is_down():
    ada = Character("Ada", 10)
    ada.take_damage(10)
    assert ada.is_down()

def test_heal_refuses_a_negative_amount():
    ada = Character("Ada", 5)
    ada.heal(-50)
    assert ada.get_health() == 5

def test_heal_stops_at_max_health():
    ada = Character("Ada", 9)
    ada.heal(5)
    assert ada.get_health() == 10

def test_nobody_down_is_standing():
    cave = Room("Cave")
    ada = Character("Ada", 10)
    cave.enter(ada)
    cave.enter(Healer("Mira", 10))
    ada.take_damage(12)
    assert cave.standing() == ["Mira"]
