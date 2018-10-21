#!/usr/bin/env python2


class Parser(object):
    def __init__(self, config_path=None, config_dict=None):
        self.config_path = config_path
        self.config = config_dict or dict()

    def parse(self):
        with file(self.config_path, 'rb') as f:
            self._parse_text(f.readlines())

    def _parse_text(self, config):
        for line in config:
            if line[:3] == '%s%s%s' % (chr(0xEF), chr(0xBB), chr(0xBF)):
                line = line[3:]  # cut off byte order mark
            line = line.strip()
            if not line or line.startswith('!') or line[3] != '=':
                continue

            k, v = line.split('=')

            if k == 'CIN':
                tmp = self.config.get(k, dict())
                cell, name, freq, modulation, ctcss, unk1, unk2, unk3 = v.split(',')
                tmp[int(cell)] = {
                    'name': name.strip(),
                    'freq': int(freq),
                    'mod': modulation,
                    'ctcss': int(ctcss),
                    'unk1': int(unk1),
                    'unk2': int(unk2),
                    'unk3': int(unk3),
                }
                self.config[k] = tmp
            elif k == 'CSP':
                tmp = self.config.get(k, dict())
                v = [int(x) for x in v.split(',')]
                tmp[v[0]] = {'min': v[1], 'max': v[2]}
                self.config[k] = tmp
            elif k in ('SBN', 'CBN'):
                tmp = self.config.get(k, dict())
                v = [x.strip() for x in v.split(',')]
                tmp[int(v[0])] = v[1:]
                self.config[k] = tmp
            else:
                self.config[k] = v.split(',') if ',' in v else v


if __name__ == '__main__':
    parser = Parser(config_path='scan125_config.txt')
    parser.parse()
    from pprint import pprint
    pprint(parser.config)
