from uniden_ubc125xlt import chirp


class TestChirpParser(object):
    def test_load(self):
        p = chirp.ConfigParser()
        assert 1 not in p.config
        p.load('tests/chirp_config.csv')
        assert 1 in p.config

    def test_loads(self):
        p = chirp.ConfigParser()
        assert 1 not in p.config
        with file('tests/chirp_config.csv', 'rb') as f:
            config = f.read()
        p.loads(config)
        assert 1 in p.config

    def test_dumps(self):
        p = chirp.ConfigParser()
        with file('tests/chirp_config.csv', 'rb') as f:
            config = f.read()
        p.loads(config)
        our_config = p.dumps()
        assert our_config == config
