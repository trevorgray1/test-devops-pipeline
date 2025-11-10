from testpkg import hello

def test_hello():
    assert hello() == "Hello from testpkg!"
