#
# -*- coding: utf-8-*-
# Access log file analyzer.
# (c) 2018 ISC Clemenz & Weinbrecht GmbH
#

import aloga
from aloga.ExtractorListener import ExtractorListener
import argparse
import datetime
import dateutil
import json
import os
import sys


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
    """
    Saves extracted data as CSV.
    :param data_file: name of the file to write
    :param data_store: internal data container
    :return:
    """
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


def save_results(r_data, r_plot, out_base_name):
    """
    All save operations in one call
    :param r_data: internal data container
    :param r_plot: plot result
    :param out_base_name: base name of output files
    :return:
    """
    save_data(out_base_name, r_data)
    save_data_as_csv(out_base_name, r_data)
    r_plot.savefig(out_base_name + '.png')


def _check_for_old_data(out_file_base_name):
    """
    Check for results of previous operations.
    :param out_file_base_name: the basic output file name
    :return: True if it already exits, otherwise False
    """
    aloga.LOG.info("check for existing data")
    fn = out_file_base_name + '.json'
    if os.path.isfile(fn) and os.path.getsize(fn) > 0:
        aloga.LOG.debug("  {0} already exists.".format(fn))
        return True
    return False


def _load_old_data(out_file_base_name):
    """
    Load data from previous operations.
    :param out_file_base_name: the basic output file name
    :return: content as dictionary
    """
    aloga.LOG.info("load existing data")
    with open(out_file_base_name + '.json', "r") as f:
        prev_date = json.load(f)
    aloga.LOG.debug("   date time conversion")
    for host, access_data in prev_date.items():
        for record in access_data['access']:
            record['datetime'] = dateutil.parser.parse(record['datetime'])

    return prev_date


def _old_data(out_file_base_name):
    aloga.LOG.info("handle existing data")
    if _check_for_old_data(out_file_base_name):
        return _load_old_data(out_file_base_name)

    return None


def analyze_log_file(alogfile, nogeo, old_data):
    """
    Do all analysis in one shot.
    :param alogfile: file to analyze
    :param nogeo: flag, controls if geo-ip data are fetched, defaults to True
                  NO geo-data are fetched.
    :return: internal data store, matplotlib plot as sequence
    """
    aloga.LOG.info("analyze")
    r_data = ExtractorListener.parse_log_file(aloga.LOG, alogfile)
    r_data = aloga.reorg_list_in_dict(r_data)
    if old_data is not None:
        r_data = aloga.merge(old_data, r_data)
    if not nogeo:
        aloga.find_location_of_hosts(r_data)
    aloga.basic_statistics(r_data)
    r_plot = aloga.access_histogram(r_data)

    # TODO add further analysis and reports
    return r_data, r_plot


if __name__ == '__main__':
    # 1. Define arguments and read commandline
    arg_parser = argparse.ArgumentParser(description="Simple access-log analyzer.")
    arg_parser.add_argument('--conf', type=str, default='aloga.ini')
    arg_parser.add_argument('--alogfile', type=str, default=None)
    arg_parser.add_argument('--nogeo', type=bool, default=True)
    arg_parser.add_argument('--out', type=str, default=None)
    args = arg_parser.parse_args()

    try:
        if args.alogfile is None:
            raise Exception('Need a logfile parameter')
        if args.out is None:
            raise Exception('Need a out-file-basename parameter')

        aloga.init(args.conf)

        old_data = _old_data(args.out)

        data, plot = analyze_log_file(args.alogfile, args.nogeo, old_data)
        save_results(data, plot, args.out)

        aloga.LOG.info('done.')
    except Exception as x:
        print('ERROR: ' + str(x), file=sys.stderr)
        sys.exit(1)
