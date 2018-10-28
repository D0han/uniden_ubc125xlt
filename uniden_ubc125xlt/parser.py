#!/usr/bin/env python2
# -*- coding: UTF-8 -*-


class Scan125(object):
    def __init__(self, config_dict=None):
        self.config = config_dict or dict()

    def load(self, config_path):
        with file(config_path, 'rb') as f:
            self.loads(f.read())

    def loads(self, config):
        for line in config.split('\n'):
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

    def dumps(self):
        config = '''\xef\xbb\xbf! Scan125 Scanner Data File - #scan125# - #full#
! Scan125 Control Program © Nick Bailey 2013-2018 V2.5.0.0   http://www.nick-bailey.co.uk    
! Comments added to this file will be removed!
! PLEASE DO NOT EDIT OR MESS WITH THIS FILE
'''
        order = ['MDL', 'VER', 'VOL', 'SQL', 'CNT', 'BLT', 'BSV', 'BTV', 'KBP', 'BPL',
                 'PRI', 'CLC', 'SCO', 'SSG', 'SCG', 'CIN', 'CSG', 'CSP', 'SBN', 'CBN']
        for k in order:
            v = self.config[k]
            if type(v) is list:
                v = ','.join((str(x) for x in v))
            config += '%s=%s\n' % (k, v)
        return config


if __name__ == '__main__':
    parser = Scan125()
    parser.load('scan125_config.txt')
    from pprint import pprint

    pprint(parser.config)
