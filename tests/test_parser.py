from uniden_ubc125xlt import parser


class TestScan125(object):
    def test_load(self):
        p = parser.Scan125()
        p.load('tests/scan125_config.txt')
        assert p.config is not None
