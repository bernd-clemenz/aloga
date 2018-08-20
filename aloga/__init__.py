#
# (c) 2018 ISC Clemenz & Weinbrecht GmbH
#

import configparser
import logging
import logging.handlers
import requests
import sys

name = 'aloga'

LOG = None
CFG = None


def init(config_name):
    """
    Initialize the access log file analyzed module
    - Create a logger
    - Read configuration
    :param config_name the name ot the config file (ini)
    """
    global LOG, CFG

    # 1. Configuration
    if sys.version_info.major == 3:
        CFG = configparser.ConfigParser()
    else:
        raise Exception('Unsupported Python major version')

    CFG.read(config_name)

    # 2. Init logging
    LOG = logging.getLogger('aloga')
    LOG.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    rh = logging.handlers.RotatingFileHandler(CFG['aloga']['log.file'],
                                              maxBytes=1024 * 1024,
                                              backupCount=50)
    ch = logging.StreamHandler()
    rh.setFormatter(formatter)
    ch.setFormatter(formatter)
    LOG.addHandler(rh)
    LOG.addHandler(ch)
    LOG.info('ALOGA initialized')


def reorg_list_in_dict(data):
    """
    Reorganize data in memory to prepare their analysis as well
    as enrichment.
    :param data: a list of dictionaries with extracted access log information
    :return: dictionary, keys are the IP-Addresses of the found accessors
    """
    global LOG
    LOG.info("Reorg of extracted data")

    ip_centric = dict()
    for rec in data:
        if rec['host'] in ip_centric.keys():
            ip_centric[rec['host']]['access'].append({'date': rec['date'],
                                                      'time': rec['time'],
                                                      'tz': rec['tz'],
                                                      'status': rec['status'],
                                                      'request': rec['request']})
        else:
            host_data = dict()
            host_data['access'] = [{'date': rec['date'],
                                    'time': rec['time'],
                                    'tz': rec['tz'],
                                    'status': rec['status'],
                                    'request': rec['request']}]
            ip_centric[rec['host']] = host_data

    return ip_centric


def find_location_of_hosts(data):
    """
    Searches for non local IP-Addresses
    :param data: reorganized dictionary with access data
    :return:
    """
    global LOG, CFG
    api_key = CFG['aloga']['ipstack.key']
    time_out = int(CFG['aloga']['timeout'])
    url_fmt = 'http://api.ipstack.com/{0}?output=json&access_key=' + api_key

    for h in data.keys():
        if h not in ['127.0.0.1', "0:0:0:0:0:0:0:1"] and not h.startswith('192.'):
            if 'geodata' not in data[h].keys():
                try:
                    rsp = requests.get(url_fmt.format(h), timeout=time_out)
                    if rsp.status_code == requests.codes.ok:
                        data[h]['geodata'] = rsp.json()
                    else:
                        LOG.warning('Error accessing ipstack API: ' + str(rsp.status_code))
                except Exception as x:
                    LOG.error('Cant read geodata: ' + str(x))

