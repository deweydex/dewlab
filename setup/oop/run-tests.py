def run_tests():
    passed = 0
    failed = 0
    for name in list(globals()):
        if name.startswith("test_"):
            try:
                globals()[name]()
                passed = passed + 1
            except AssertionError as error:
                print("FAILED", name, error)
                failed = failed + 1
    print(passed, "passed,", failed, "failed")
