from uniden_ubc125xlt import scan125


class TestScan125Parser(object):
    def test_load(self):
        p = scan125.ConfigParser()
        p.load('tests/scan125_config.txt')
        assert p.config

    def test_loads(self):
        p = scan125.ConfigParser()
        with file('tests/scan125_config.txt', 'rb') as f:
            config = f.read()
        p.loads(config)
        assert p.config

    def test_dumps(self):
        p = scan125.ConfigParser()
        with file('tests/scan125_config.txt', 'rb') as f:
            config = f.read()
        p.loads(config)
        our_config = p.dumps().replace('! Generated with uniden_ubc125xlt package by D0han\n', '')
        assert our_config == config
