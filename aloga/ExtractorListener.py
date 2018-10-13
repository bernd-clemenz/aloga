#
# -*- coding: utf-8-*-
# Listener for the clfParser. It extracts basic data from the parsed lines
# into a list of dictionaries.
# (c) 2018 ISC Clemenz & Weinbrecht GmbH
#

from aloga.clf.clfListener import clfListener
from aloga.clf.clfLexer import clfLexer
from aloga.clf.clfParser import clfParser
from antlr4 import *


class ExtractorListener(clfListener):

    @staticmethod
    def parse_log_file(log, log_file):
        """
        Data extraction using ANTLR4 runtime an the generated
        lexer/parser
        :param log the logger
        :param log_file: the access log data file name
        :return: list with extracted data
        """
        log.info('Loading log file')
        log_stream = FileStream(log_file)
        log.debug('created input stream')
        lexer = clfLexer(log_stream)
        log.debug('created lexer')
        stream = CommonTokenStream(lexer)
        log.debug('created token stream')
        parser = clfParser(stream)
        log.debug('created parser')
        walker = ParseTreeWalker()
        tree = parser.log()
        extractor = ExtractorListener(log)
        walker.walk(extractor, tree)
        log.debug('parsing done')

        return extractor.get_data()

    # -------------------------------------------------------------------------

    """
    This listener does the data extraction from the
    access log files. It has to be registered with
    the parser.
    """
    _log = None
    _all_data = list()
    _line_data = None
    _line_counter = 0

    def __init__(self, log):
        """
        Constructor.
        :param log:  global logger
        """
        self._log = log
        self._log.debug("created extractor")

    def get_data(self):
        """
        get all the extracted data
        :return: extracted data
        """
        return self._all_data

    def enterLine(self, ctx: clfParser.LineContext):
        """
        prepare per line data container.
        :param ctx: parser context
        :return:
        """
        self._line_counter += 1
        # self.log.debug("entered line: {}".format(self.line_counter))
        self._line_data = dict()

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
            self._line_data['host'] = str(host.IP())
        elif host.STRING() is not None:
            self._line_data['host'] = str(host.STRING())
        # date/time
        datetimetz = ctx.datetimetz()
        self._line_data['date'] = str(datetimetz.DATE())
        self._line_data['time'] = str(datetimetz.TIME())
        self._line_data['tz'] = str(datetimetz.TZ())
        # request
        request = ctx.request()
        self._line_data['request'] = str(request.LITERAL())
        # status
        status = ctx.statuscode()
        self._line_data['status'] = str(status.STRING())

        self._all_data.append(self._line_data)
