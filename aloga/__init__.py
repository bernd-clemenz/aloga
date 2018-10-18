#
# -*- coding: utf-8-*-
# (c) 2018 ISC Clemenz & Weinbrecht GmbH
#
import configparser
import dateutil.parser
import logging
import logging.handlers
import os
import requests
import sys
import matplotlib.pyplot as plt
import numpy as np
import math

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
        
    if not os.path.isfile(config_name):
        raise Exception('config file missing')

    CFG.read(config_name)

    # 2. Init logging
    LOG = logging.getLogger('aloga')
    lv_cfg = CFG['aloga']['log.level']
    lv_mp = {'INFO': logging.INFO,
             'WARN': logging.WARNING,
             'DEBUG': logging.DEBUG,
             'FATAL': logging.FATAL,
             'ERROR': logging.ERROR}
    if lv_cfg is not None and lv_cfg in lv_mp.keys():
        level = lv_mp[lv_cfg]
    else:
        level = logging.INFO

    LOG.setLevel(level)
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


def _reorg_date_time(host_rec):
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
            ip_centric[rec['host']]['access'].append({'datetime': _reorg_date_time(rec),
                                                      'status': rec['status'],
                                                      'request': rec['request']})
        else:
            host_data = dict()
            host_data['access'] = [{'datetime': _reorg_date_time(rec),
                                    'status': rec['status'],
                                    'request': rec['request']}]
            ip_centric[rec['host']] = host_data

    return ip_centric


def _is_record_in_access_data(access_data, record):
    for original in access_data:
        if original['datetime'] == record['datetime'] and original['request'] == record['request']:
            return True

    return False


def merge(target, new_data):
    """
    Merges access data.
    :param target: existing data, target of merge
    :param new_data: the data to merge same structure as target
    :return: target if new_data and target are not None,
             new_data if target is None,
             target if new_data is none
    """
    global LOG
    LOG.info("Merging new data in store")

    if new_data is None:
        return target

    if target is None:
        return new_data

    # Iterate the new_data hosts
    for host, access_data in new_data.items():
        LOG.debug("new: " + host)
        if host in target:
            #
            # potentially new access data for a already known host
            #
            LOG.debug("   found in old data")
            target_access = target[host]['access']
            for record in access_data['access']:
                if not _is_record_in_access_data(target_access, record):
                    LOG.debug("       found new access: {0} -> {1}".format(record['datetime'], record['request']))
                    target_access.append(record)
        else:
            #
            # a new host, data are just taken
            #
            LOG.info("   new host found: {0}".format(host))
            target[host] = access_data

    return target


def _is_local_ip(ip):
    """
    Find if a address is from the local
    network.
    :param ip: the ip address to check
    :return: True if detected as a 'local'-Network address
    """
    return True if ip in ['127.0.0.1', "0:0:0:0:0:0:0:1"] or not ip.startswith('192.') else False


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
        return

    LOG.info("Geo-data read")
    geo_read_count = 0
    for h in data.keys():
        if not _is_local_ip(h) and 'geodata' not in data[h].keys():
            try:
                LOG.info("  for {0}".format(h))
                rsp = requests.get(url_fmt.format(h), timeout=time_out)
                if rsp.status_code == requests.codes.ok:
                    data[h]['geodata'] = rsp.json()
                    geo_read_count += 1
                else:
                    LOG.warning('Error accessing ipstack API: ' + str(rsp.status_code))
            except Exception as x:
                LOG.error('Cant read geo-data: ' + str(x))
    LOG.info('  Geo-data read count: {}'.format(geo_read_count))


def _status_type_counters(access_data):
    """
    Count the different HTTP-status code types.
    :param access_data: internal data store
    :return: sequence with counters for frequency of
    status http status code types.
    """
    global LOG
    LOG.debug("Counting response code types")
    info_count = 0
    ok_count = 0
    redir_count = 0
    client_error_count = 0
    server_error_count = 0
    other_count = 0
    for d in access_data:
        status = int(d['status'])
        if 100 <= status < 200:
            info_count += 1
        elif 200 <= status < 300:
            ok_count += 1
        elif 300 <= status < 400:
            redir_count += 1
        elif 400 <= status < 500:
            client_error_count += 1
        elif 500 <= status < 600:
            server_error_count += 1
        else:
            other_count += 1

    return info_count, ok_count, redir_count, client_error_count, server_error_count, other_count


def _time_of_access(access_data):
    """
    Creator method to return the next 'datetime' entry in an
    access-data list.
    :param access_data:
    :return: the next datetime-entry
    """
    for d in access_data:
        yield d['datetime']


def _time_range(access_data):
    """
    Find the range of minimum and maximum date in access data per client
    :param access_data: client access data
    :return: minimum and maximum date as sequence
    """
    global LOG
    LOG.debug("Time range")
    max_date = max(_time_of_access(access_data))
    min_date = min(_time_of_access(access_data))
    return min_date, max_date


def basic_statistics(data):
    """
    Basic counters.
    :param data: reorganized dictionary with access data
    :return:
    """
    global LOG
    LOG.info("Basic statistics")
    for h in data.keys():
        if 'access' in data[h].keys():
            item = data[h]
            access_data = item['access']
            all_count = len(access_data)
            item['count'] = all_count
            info_count,\
                ok_count,\
                redir_count,\
                client_error_count,\
                server_error_count,\
                other_count = _status_type_counters(access_data)
            item['info_count'] = info_count
            item['ok_count'] = ok_count
            item['redir_count'] = redir_count
            item['client_error_count'] = client_error_count
            item['server_error_count'] = server_error_count
            item['other_count'] = other_count
            min_date, max_date = _time_range(access_data)
            item['min_date'] = min_date
            item['max_date'] = max_date
            item['client_error_quota'] = client_error_count / all_count
        else:
            item = dict()
            item['count'] = 0
            item['info_count'] = 0
            item['ok_count'] = 0
            item['redir_count'] = 0
            item['client_error_count'] = 0
            item['server_error_count'] = 0
            item['other_count'] = 0
            item['min_date'] = None
            item['max_date'] = None
            item['client_error_quota'] = 0
            item['access'] = []
            data[h] = item


def access_diagram(data, out_base_name):
    """
     Per access host
    :param data: reorganized dictionary with access data
    :param out_base_name: basic name for saving the diagram
    :return:
    """
    global LOG, CFG
    LOG.info('Diagram (access)')
    # 1 Selection of data
    threshold = int(CFG['diagram']['access_threshold'])
    items = data.keys()
    items = filter(_is_local_ip, items)
    items = list(filter(lambda it: data[it]['count'] > threshold, items))
    # 2 prepare display data.
    hosts = items
    y_pos = np.arange(len(hosts))
    count = list()
    for k in items:
        count.append(data[k]['count'])

    plt.rcdefaults()
    plt.figure(figsize=(14, 10))
    plt.barh(y_pos, count, align='center', alpha=0.5)
    plt.yticks(y_pos, hosts)
    plt.xlabel('Non-local access counter > 5')
    plt.ylabel('Hosts')
    plt.title('Access from non-local hosts')

    plt.savefig(out_base_name + '-ext-diag.png')


def access_client_error_diagram(data, out_base_name):
    """
         Client error quota per host
        :param data: reorganized dictionary with access data
        :param out_base_name: basic name for saving the diagram
        :return:
     """
    global LOG, CFG
    LOG.info('Diagram (client-error)')
    threshold = int(CFG['diagram']['access_threshold'])
    ce_threshold = float(CFG['diagram']['client_error_threshold'])
    items = data.keys()
    items = filter(_is_local_ip, items)
    items = list(filter(lambda it: data[it]['client_error_quota'] > ce_threshold and data[it]['count'] > threshold,
                        items))

    y_pos = np.arange(len(items))
    count = list()
    for k in items:
        count.append(data[k]['client_error_quota'])

    plt.rcdefaults()
    plt.figure(figsize=(14, 10))
    plt.barh(y_pos, count, align='center', alpha=0.5)
    plt.yticks(y_pos, items)
    plt.xlabel('Non-local access client error quota > ' + str(ce_threshold))
    plt.ylabel('Hosts')
    plt.title('Access from non-local hosts, client error quota > ' + str(ce_threshold))

    plt.savefig(out_base_name + '-ext-client-err.png')


def _transform_mercator(x_len, y_len, lat_limit, long, lat):
    global CFG, LOG
    LOG.debug("Transform geo to image")

    # directly in image coordinates
    x = x_len + long / 180.0 * x_len
    y_s = math.asinh(math.tan(math.radians(lat)))
    y_g = math.asinh(math.tan(math.radians(lat_limit)))
    y = y_len + y_s / y_g * y_len

    # invert it
    y = 2 * y_len - y

    return x, y


def _insert_markers_svg(markers, out_base_name):
    global CFG, LOG
    if len(markers) == 0:
        return
    template = CFG['map']['template']
    marker_placeholder = CFG['map']['placeholder']

    with open(template, "r") as f:
        svg = f.readlines()

    # scan for placeholder
    pos = -1
    for lnr in range(0, len(svg) - 1):
        if svg[lnr].find(marker_placeholder) != -1:
            pos = lnr
            break
    LOG.info("Placeholder at: {0}".format(pos))

    if pos < 0:
        LOG.error("Placeholder not found in SVG")
        return

    # insert markers
    for m in markers:
        svg.insert(pos, m)

    # write updated file
    LOG.info("Saving SVG file")
    with open(out_base_name + '.svg', 'w') as f:
        f.writelines(svg)


def world_map_svg(data, out_base_name):
    global CFG, LOG
    LOG.info("World-Map")

    # load transformation data from CFG
    x_len = float(CFG['map']['x_len'])
    y_len = float(CFG['map']['y_len'])
    lat_limit = float(CFG['map']['lat_limit'])

    markers = list()
    marker_template = '<use xlink:href="#markerDot" x="{0}" y="{1}"><title>{2}</title></use>'

    # iterate the hosts
    for k, v in data.items():
        if 'geodata' in v:
            LOG.info("  Geodata found for: {0}".format(k))
            x, y = _transform_mercator(x_len,
                                       y_len,
                                       lat_limit,
                                       v['geodata']['longitude'],
                                       v['geodata']['latitude'])
            markers.append(marker_template.format(x, y, str(v['geodata']['longitude']) + ',' + str(v['geodata']['latitude'])))

    _insert_markers_svg(markers, out_base_name)