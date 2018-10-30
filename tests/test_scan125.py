from uniden_ubc125xlt import scan125

EMPTY_CHANNEL = {'ctcss': 0,
                 'freq': 0,
                 'mod': 'AUTO',
                 'name': '',
                 'unk1': 2,
                 'unk2': 1,
                 'unk3': 0}


class TestScan125Parser(object):
    def test_load(self):
        p = scan125.ConfigParser()
        assert p.config['CIN'][1] == EMPTY_CHANNEL
        p.load('tests/scan125_config.txt')
        assert p.config['CIN'][1] != EMPTY_CHANNEL

    def test_loads(self):
        p = scan125.ConfigParser()
        assert p.config['CIN'][1] == EMPTY_CHANNEL
        with file('tests/scan125_config.txt', 'rb') as f:
            config = f.read()
        p.loads(config)
        assert p.config['CIN'][1] != EMPTY_CHANNEL

    def test_dumps(self):
        p = scan125.ConfigParser()
        with file('tests/scan125_config.txt', 'rb') as f:
            config = f.read()
        p.loads(config)
        our_config = p.dumps().replace('! Generated with uniden_ubc125xlt package by D0han\n', '')
        assert our_config == config

    def test_find_free_channel(self):
        p = scan125.ConfigParser()
        p.load('tests/scan125_config.txt')
        for cell in range(1, 5):
            assert p.config['CIN'][cell] != EMPTY_CHANNEL
        p.config['CIN'][5] = EMPTY_CHANNEL
        assert p.find_free_channel() == 5
