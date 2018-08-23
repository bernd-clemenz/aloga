#
# (c) 2018 ISC Clemenz & Weinbrecht GmbH
#
import configparser
import dateutil.parser
import logging
import logging.handlers
import requests
import sys
import matplotlib.pyplot as plt
import numpy as np

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

    # 3. init other modules
    plt.rcdefaults()

    LOG.info('ALOGA initialized')


def reorg_date_time(host_rec):
    """
    Reorganize structure of date time to ensure universally
    readable JSON output.
    :param host_rec: record of extracted data
    :return: a datetime version of the parsed data
    """
    t_str = host_rec['date'] + ' ' + host_rec['time'] + ' ' + host_rec['tz']
    t_val = dateutil.parser.parse(t_str)

    return t_val


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
            ip_centric[rec['host']]['access'].append({'datetime': reorg_date_time(rec),
                                                      'status': rec['status'],
                                                      'request': rec['request']})
        else:
            host_data = dict()
            host_data['access'] = [{'datetime': reorg_date_time(rec),
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
    if api_key is None:
        LOG.warning('No geodata can be fetched, no ipstack.key defined')

    LOG.info("Geodata read")

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


def basic_statistics(data):
    """
    Basic counters.
    :param data:  reorganized dictionary with access data
    :return:
    """
    global LOG
    LOG.info("Basic statistics")
    for h in data.keys():
        if 'access' in data[h].keys():
            data[h]['count'] = len(data[h]['access'])
        else:
            data[h]['count'] = 0


def access_histogram(data):
    """
    Histogramm per access host
    :param data: reorganized dictionary with access data
    :return: a matplotlib plot
    """
    global LOG
    objects = tuple(k for k in data.keys())
    y_pos = np.arange(len(objects))
    count = list()
    for k in data.keys():
        count.append(data[k]['count'])

    plt.barh(y_pos, count, align='center', alpha=0.5)
    plt.yticks(y_pos, objects)
    plt.xlabel('Hosts')
    plt.title('Access from hosts')

    return plt
