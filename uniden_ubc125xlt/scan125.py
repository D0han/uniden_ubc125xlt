#!/usr/bin/env python2
# -*- coding: UTF-8 -*-


class ConfigParser(object):
    def __init__(self, config_dict=None):
        if config_dict is None:
            self.config = {'CNT': '8',
                           'BTV': '!2.60V',
                           'VER': '!2.5.0.0',
                           'MDL': 'UBC125XLT',
                           'SCG': '0111111110',
                           'VOL': '6',
                           'BLT': 'KY',
                           'BSV': '14',
                           'SQL': '4',
                           'BPL': '1',
                           'CSG': '1111101101',
                           'SSG': '1101111###',
                           'PRI': '0',
                           'SCO': ['4', '1'],
                           'KBP': ['99', '0'],
                           'CLC': ['2', '0', '1', '001010', '1'],
                           'CSP': {1: {'max': 279999, 'min': 250000},
                                   2: {'max': 301999, 'min': 280000},
                                   3: {'max': 499999, 'min': 302000},
                                   4: {'max': 880000, 'min': 500000},
                                   5: {'max': 1369999, 'min': 1080000},
                                   6: {'max': 1439999, 'min': 1370000},
                                   7: {'max': 1740000, 'min': 1440000},
                                   8: {'max': 3999999, 'min': 2250000},
                                   9: {'max': 5120000, 'min': 4000000},
                                   10: {'max': 9600000, 'min': 8060000}},
                           'CBN': {x: [''] for x in range(1, 11)},
                           'SBN': {x: [''] for x in range(1, 11)},
                           'CIN': {x: {'ctcss': 0,
                                       'freq': 0,
                                       'mod': 'AUTO',
                                       'name': '',
                                       'unk1': 2,
                                       'unk2': 1,
                                       'unk3': 0}
                                   for x in range(1, 501)},
                           }
        else:
            self.config = config_dict

    def load(self, config_path):
        with file(config_path, 'rb') as f:
            self.loads(f.read())

    def loads(self, config):
        for line in config.split('\n'):
            if line[:3] == '{}{}{}'.format(chr(0xEF), chr(0xBB), chr(0xBF)):
                line = line[3:]  # cut off byte order mark
            line = line.strip()
            if not line or line.startswith('!') or line[3] != '=':
                continue

            k, v = line.split('=')

            if k == 'CIN':
                channels = self.config.get(k, dict())
                cell, name, freq, modulation, ctcss, unk1, unk2, unk3 = v.split(',')
                channels[int(cell)] = {
                    'name': name.strip(),
                    'freq': int(freq),
                    'mod': modulation,
                    'ctcss': int(ctcss),
                    'unk1': int(unk1),
                    'unk2': int(unk2),
                    'unk3': int(unk3),
                }
                self.config[k] = channels
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

    def dumps(self):
        config = '''\xef\xbb\xbf! Scan125 Scanner Data File - #scan125# - #full#
! Scan125 Control Program © Nick Bailey 2013-2018 V2.5.0.0   http://www.nick-bailey.co.uk    
! Comments added to this file will be removed!
! PLEASE DO NOT EDIT OR MESS WITH THIS FILE
! Generated with uniden_ubc125xlt package by D0han
'''
        order = ['MDL', 'VER', 'VOL', 'SQL', 'CNT', 'BLT', 'BSV', 'BTV', 'KBP', 'BPL',
                 'PRI', 'CLC', 'SCO', 'SSG', 'SCG', 'CIN', 'CSG', 'CSP', 'SBN', 'CBN']
        for k in order:
            v = self.config[k]
            if type(v) is list:
                v = ','.join((str(x) for x in v))
            elif k == 'CSP':
                for k2, v2 in v.iteritems():
                    config += 'CSP={:02d},{:08d},{:08d}\n'.format(k2, v2['min'], v2['max'])
                continue
            elif k == 'CIN':
                for k2, v2 in v.iteritems():
                    name = '{:16}'.format(v2['name']) if v2['name'] else ' '
                    config += 'CIN={:03d},{},{:08d},{},{},{},{},{}\n'.format(k2, name, v2['freq'],
                                                                             v2['mod'], v2['ctcss'], v2['unk1'],
                                                                             v2['unk2'], v2['unk3'])
                continue
            elif k in ('SBN', 'CBN'):
                for k2, v2 in v.iteritems():
                    config += '{}={:02d},{}\n'.format(k, k2, v2[0])
                continue
            config += '{}={}\n'.format(k, v)
        return config

    def set_channel(self, cell=None, frequency=0, name='', modulation='AUTO', ctcss=0,
                    unk1=2, unk2=1, unk3=0, block_nr=None):
        if cell is None:
            cell = self.find_free_channel()
        if block_nr is not None:
            assert 0 <= block_nr <= 10
            assert 0 < cell <= 50
            cell = 50 * block_nr + cell
        assert 0 < cell <= 500
        modulation = 'FM' if modulation == 'NFM' else modulation
        assert modulation in ('AUTO', 'FM', 'AM')
        assert len(name) <= 16
        channels = self.config['CIN']
        channels[cell] = {
            'name': name,
            'freq': frequency,
            'mod': modulation,
            'ctcss': ctcss,
            'unk1': unk1,
            'unk2': unk2,
            'unk3': unk3,
        }
        self.config['CIN'] = channels

    def find_free_channel(self):
        empty_channel = {'ctcss': 0,
                         'freq': 0,
                         'mod': 'AUTO',
                         'name': '',
                         'unk1': 2,
                         'unk2': 1,
                         'unk3': 0}
        channels = self.config['CIN']
        for cell in range(1, 501):
            try:
                if channels[cell] == empty_channel:
                    return cell
            except KeyError:
                return cell
        raise ValueError('No free channels found')


if __name__ == '__main__':
    parser = ConfigParser()
    parser.load('../tests/scan125_config.txt')
    from pprint import pprint

    pprint(parser.config)
