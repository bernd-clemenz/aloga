#
# -*- coding: utf-8-*-
# Listener for the clfParser. It extracts basic data from the parsed lines
# into a list of dictionaries.
# (c) 2018 ISC Clemenz & Weinbrecht GmbH
#

from aloga.clf.clfListener import clfListener
from aloga.clf.clfParser import clfParser


class ExtractorListener(clfListener):
    """
    This listener does the data extraction from the
    access log files. It has to be registered with
    the parser.
    """
    log = None
    all_data = list()
    line_data = None
    line_counter = 0

    def __init__(self, log):
        """
        Constructor.
        :param log:  global logger
        """
        self.log = log
        log.debug("created extractor")

    def get_data(self):
        """
        get all the extracted data
        :return: extracted data
        """
        return self.all_data

    def enterLine(self, ctx: clfParser.LineContext):
        """
        prepare per line data container.
        :param ctx: parser context
        :return:
        """
        self.line_counter += 1
        # self.log.debug("entered line: {}".format(self.line_counter))
        self.line_data = dict()

    def exitLine(self, ctx: clfParser.LineContext):
        """
        Collect data in per line storage
        :param ctx: parser context
        :return:
        """
        # self.log.debug("exit line: {}".format(self.line_counter))
        # Host
        host = ctx.host()

        if host.IP() is not None:
            self.line_data['host'] = str(host.IP())
        elif host.STRING() is not None:
            self.line_data['host'] = str(host.STRING())
        # date/time
        datetimetz = ctx.datetimetz()
        self.line_data['date'] = str(datetimetz.DATE())
        self.line_data['time'] = str(datetimetz.TIME())
        self.line_data['tz'] = str(datetimetz.TZ())
        # request
        request = ctx.request()
        self.line_data['request'] = str(request.LITERAL())
        # status
        status = ctx.statuscode()
        self.line_data['status'] = str(status.STRING())

        self.all_data.append(self.line_data)
