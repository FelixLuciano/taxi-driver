from src.main import result


def test_result():
    assert result() == True, "Hello World!"


def test_result2():
    assert result() != False, "Hello World!"
