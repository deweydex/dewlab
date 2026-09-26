def test_a_burn_uses_fuel():
    voyager = Probe("Voyager", 100)
    voyager.burn(30)
    assert voyager.get_fuel() == 70

def test_a_probe_can_burn_all_it_has():
    voyager = Probe("Voyager", 70)
    assert voyager.can_burn(70)

def test_a_negative_burn_is_refused():
    voyager = Probe("Voyager", 70)
    voyager.burn(-50)
    assert voyager.get_fuel() == 70

def test_a_landed_lander_cannot_burn():
    philae = Lander("Philae", 40)
    philae.land()
    assert not philae.can_burn(5)

def test_only_ready_probes_are_listed():
    outer = Mission("Outer Planets")
    philae = Lander("Philae", 40)
    outer.launch(Probe("Voyager", 70))
    outer.launch(philae)
    philae.land()
    assert outer.ready_for(30) == ["Voyager"]
