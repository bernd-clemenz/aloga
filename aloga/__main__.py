#
# Access log file analyzer.
# (c) 2018 ISC Clemenz & Weinbrecht GmbH
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
    """
    Data extraction using ANTLR4 runtime an the generated
    lexer/parser
    :param log_file: the access log data file name
    :return: list with extracted data
    """
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
    """
    Called by converter
    :param o: data item
    :return: converted item
    """
    if isinstance(o, datetime.datetime):
        return o.__str__()


def save_data(data_file, data_store):
    """
    Save the extracted data as JSON file
    :param data_file: name of the target file
    :param data_store: data structure to store as JSON
    :return:
    """
    aloga.LOG.info('Saving access data file as JSON')
    if len(data_store) > 0:
        with open(data_file + '.json', 'w') as f:
            f.write(json.dumps(data_store, indent=2, sort_keys=True, default=datetime_converter))


def save_data_as_csv(data_file, data_store):
    aloga.LOG.info("Saving as CSV")
    if len(data_store) > 0:
        with open(data_file + '.csv', 'w') as f:
            for host in data_store:
                acc = data_store[host]['access']
                for l in acc:
                    line = host + ';'
                    for k, v in l.items():
                        line = line + str(v) + ';'
                    line = line + '\n'
                    line = line.replace('"', '')
                    f.write(line)


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

        aloga.find_location_of_hosts(data)
        aloga.basic_statistics(data)
        plot = aloga.access_histogram(data)
        # TODO add further analysis and reports

        save_data(args.out, data)
        save_data_as_csv(args.out, data)
        plot.savefig(args.out + '.png')

        aloga.LOG.info('done.')
    except Exception as x:
        print('ERROR: ' + str(x), file=sys.stderr)
        sys.exit(1)
