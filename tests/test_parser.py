from uniden_ubc125xlt import parser


class TestScan125(object):
    def test_load(self):
        p = parser.Scan125()
        p.load('tests/scan125_config.txt')
        assert p.config is not None

    def test_loads(self):
        p = parser.Scan125()
        with file('tests/scan125_config.txt', 'rb') as f:
            config = f.read()
        p.loads(config)
        assert p.config is not None

    def test_dumps(self):
        p = parser.Scan125()
        with file('tests/scan125_config.txt', 'rb') as f:
            config = f.read()
        p.loads(config)
        assert p.dumps() == config
