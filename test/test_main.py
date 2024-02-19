from test.utils import run_testcase


def test_testcase_0():
    run_testcase("data/testcase_0.txt")

def test_testcase_1():
    failed = False

    try:
        run_testcase("data/testcase_1.txt")
    except Exception:
        failed = True

    assert failed, "Target is out of bounds. Should've failed!"

def test_testcase_2():
    run_testcase("data/testcase_2.txt")

def test_testcase_3():
    run_testcase("data/testcase_3.txt")
