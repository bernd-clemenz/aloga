#
# python -m aloga --alogfile=C:\tools\apache-tomcat-9.0.10\logs\localhost_access_log.2018-07-28.txt --out=access.json
#

import aloga
from aloga.ExtractorListener import ExtractorListener
from aloga.clf.clfParser import clfParser
from aloga.clf.clfLexer import clfLexer
from antlr4 import *
import argparse
import datetime
import json
import sys


def parse_file(log_file):
    aloga.LOG.info('Loading log file')
    log_stream = FileStream(log_file)
    aloga.LOG.debug('created input stream')
    lexer = clfLexer(log_stream)
    aloga.LOG.debug('created lexer')
    stream = CommonTokenStream(lexer)
    aloga.LOG.debug('created token stream')
    parser = clfParser(stream)
    aloga.LOG.debug('created parser')
    walker = ParseTreeWalker()
    tree = parser.log()
    extractor = ExtractorListener(aloga.LOG)
    walker.walk(extractor, tree)
    aloga.LOG.debug('parsing done')

    return extractor.get_data()


def datetime_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def save_data(data_file, data_store):
    aloga.LOG.info('Saving access data file')
    if len(data_store) > 0:
        with open(data_file, 'w') as f:
            f.write(json.dumps(data_store, indent=2, sort_keys=True, default=datetime_converter))


if __name__ == '__main__':
    # 1. Define arguments and read commandline
    arg_parser = argparse.ArgumentParser(description="Simple access log analyzer.")
    arg_parser.add_argument('--conf', type=str, default='aloga.ini')
    arg_parser.add_argument('--alogfile', type=str, default=None)
    arg_parser.add_argument('--out', type=str, default=None)
    args = arg_parser.parse_args()

    try:
        if args.alogfile is None:
            raise Exception('Need a logfile parameter')

        aloga.init(args.conf)
        data = parse_file(args.alogfile)
        data = aloga.reorg_list_in_dict(data)

        data['77.178.156.78'] = dict()

        aloga.find_location_of_hosts(data)
        save_data(args.out, data)
    except Exception as x:
        print('ERROR: ' + str(x), file=sys.stderr)
        sys.exit(1)
