#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import StringIO
import csv


class ConfigParser(object):
    def __init__(self, config_dict=None):
        if config_dict is None:
            self.config = {0: {'Comment': '',
                               'DVCODE': '',
                               'DtcsCode': '023',
                               'DtcsPolarity': 'NN',
                               'Duplex': '',
                               'Frequency': '446.193750',
                               'Location': '0',
                               'Mode': 'NFM',
                               'Name': 'PMR16',
                               'Offset': '0.000000',
                               'RPT1CALL': '',
                               'RPT2CALL': '',
                               'Skip': 'S',
                               'TStep': '5.00',
                               'Tone': '',
                               'URCALL': '',
                               'cToneFreq': '88.5',
                               'rToneFreq': '88.5'}, }
        else:
            self.config = config_dict

    def load(self, config_path):
        with file(config_path, 'rb') as f:
            self.loads(f.read())

    def loads(self, config):
        config = config.split('\n')
        reader = csv.DictReader(config)
        for row in reader:
            self.config[int(row['Location'])] = row

    def dumps(self):
        fieldnames = 'Location,Name,Frequency,Duplex,Offset,Tone,rToneFreq,cToneFreq,DtcsCode,DtcsPolarity,' \
                     'Mode,TStep,Skip,Comment,URCALL,RPT1CALL,RPT2CALL,DVCODE'.split(',')
        si = StringIO.StringIO()
        writer = csv.DictWriter(si, fieldnames=fieldnames)
        writer.writeheader()
        for k, v in self.config.iteritems():
            writer.writerow(v)
        return si.getvalue()


if __name__ == '__main__':
    parser = ConfigParser()
    parser.load('../tests/chirp_config.csv')
    from pprint import pprint

    pprint(parser.config)
