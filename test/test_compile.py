

def test_compile():
    try:
        import tiddlywebplugins.ltr
        assert True
    except ImportError, exc:
        assert False, exc
