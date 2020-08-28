# Generated from clf.g4 by ANTLR 4.8
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\17")
        buf.write("G\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\3\2\5\2\32\n\2")
        buf.write("\3\2\6\2\35\n\2\r\2\16\2\36\3\2\5\2\"\n\2\3\3\3\3\3\3")
        buf.write("\3\3\3\3\3\3\3\3\3\3\3\3\3\3\5\3.\n\3\3\4\3\4\3\5\3\5")
        buf.write("\3\6\3\6\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\b\3\b\3\t\3\t\3")
        buf.write("\n\3\n\3\13\3\13\3\f\3\f\3\f\2\2\r\2\4\6\b\n\f\16\20\22")
        buf.write("\24\26\2\3\4\2\n\n\r\r\2?\2\34\3\2\2\2\4#\3\2\2\2\6/\3")
        buf.write("\2\2\2\b\61\3\2\2\2\n\63\3\2\2\2\f\65\3\2\2\2\16<\3\2")
        buf.write("\2\2\20>\3\2\2\2\22@\3\2\2\2\24B\3\2\2\2\26D\3\2\2\2\30")
        buf.write("\32\5\4\3\2\31\30\3\2\2\2\31\32\3\2\2\2\32\33\3\2\2\2")
        buf.write("\33\35\7\16\2\2\34\31\3\2\2\2\35\36\3\2\2\2\36\34\3\2")
        buf.write("\2\2\36\37\3\2\2\2\37!\3\2\2\2 \"\5\4\3\2! \3\2\2\2!\"")
        buf.write("\3\2\2\2\"\3\3\2\2\2#$\5\6\4\2$%\5\b\5\2%&\5\n\6\2&\'")
        buf.write("\5\f\7\2\'(\5\20\t\2()\5\24\13\2)-\5\26\f\2*+\5\16\b\2")
        buf.write("+,\5\22\n\2,.\3\2\2\2-*\3\2\2\2-.\3\2\2\2.\5\3\2\2\2/")
        buf.write("\60\t\2\2\2\60\7\3\2\2\2\61\62\7\r\2\2\62\t\3\2\2\2\63")
        buf.write("\64\7\r\2\2\64\13\3\2\2\2\65\66\7\3\2\2\66\67\7\6\2\2")
        buf.write("\678\7\4\2\289\7\7\2\29:\7\b\2\2:;\7\5\2\2;\r\3\2\2\2")
        buf.write("<=\7\t\2\2=\17\3\2\2\2>?\7\t\2\2?\21\3\2\2\2@A\7\t\2\2")
        buf.write("A\23\3\2\2\2BC\7\r\2\2C\25\3\2\2\2DE\7\r\2\2E\27\3\2\2")
        buf.write("\2\6\31\36!-")
        return buf.getvalue()


class clfParser ( Parser ):

    grammarFileName = "clf.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'['", "':'", "']'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "DATE", "TIME", "TZ", "LITERAL", "IP", "IPV4", "IPV6", 
                      "STRING", "EOL", "WS" ]

    RULE_log = 0
    RULE_line = 1
    RULE_host = 2
    RULE_logname = 3
    RULE_username = 4
    RULE_datetimetz = 5
    RULE_referer = 6
    RULE_request = 7
    RULE_useragent = 8
    RULE_statuscode = 9
    RULE_bytes = 10

    ruleNames =  [ "log", "line", "host", "logname", "username", "datetimetz", 
                   "referer", "request", "useragent", "statuscode", "bytes" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    DATE=4
    TIME=5
    TZ=6
    LITERAL=7
    IP=8
    IPV4=9
    IPV6=10
    STRING=11
    EOL=12
    WS=13

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class LogContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOL(self, i:int=None):
            if i is None:
                return self.getTokens(clfParser.EOL)
            else:
                return self.getToken(clfParser.EOL, i)

        def line(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(clfParser.LineContext)
            else:
                return self.getTypedRuleContext(clfParser.LineContext,i)


        def getRuleIndex(self):
            return clfParser.RULE_log

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLog" ):
                listener.enterLog(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLog" ):
                listener.exitLog(self)




    def log(self):

        localctx = clfParser.LogContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_log)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 26 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 23
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==clfParser.IP or _la==clfParser.STRING:
                        self.state = 22
                        self.line()


                    self.state = 25
                    self.match(clfParser.EOL)

                else:
                    raise NoViableAltException(self)
                self.state = 28 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

            self.state = 31
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==clfParser.IP or _la==clfParser.STRING:
                self.state = 30
                self.line()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LineContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def host(self):
            return self.getTypedRuleContext(clfParser.HostContext,0)


        def logname(self):
            return self.getTypedRuleContext(clfParser.LognameContext,0)


        def username(self):
            return self.getTypedRuleContext(clfParser.UsernameContext,0)


        def datetimetz(self):
            return self.getTypedRuleContext(clfParser.DatetimetzContext,0)


        def request(self):
            return self.getTypedRuleContext(clfParser.RequestContext,0)


        def statuscode(self):
            return self.getTypedRuleContext(clfParser.StatuscodeContext,0)


        def bytes(self):
            return self.getTypedRuleContext(clfParser.BytesContext,0)


        def referer(self):
            return self.getTypedRuleContext(clfParser.RefererContext,0)


        def useragent(self):
            return self.getTypedRuleContext(clfParser.UseragentContext,0)


        def getRuleIndex(self):
            return clfParser.RULE_line

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLine" ):
                listener.enterLine(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLine" ):
                listener.exitLine(self)




    def line(self):

        localctx = clfParser.LineContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_line)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 33
            self.host()
            self.state = 34
            self.logname()
            self.state = 35
            self.username()
            self.state = 36
            self.datetimetz()
            self.state = 37
            self.request()
            self.state = 38
            self.statuscode()
            self.state = 39
            self.bytes()
            self.state = 43
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==clfParser.LITERAL:
                self.state = 40
                self.referer()
                self.state = 41
                self.useragent()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class HostContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(clfParser.STRING, 0)

        def IP(self):
            return self.getToken(clfParser.IP, 0)

        def getRuleIndex(self):
            return clfParser.RULE_host

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHost" ):
                listener.enterHost(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHost" ):
                listener.exitHost(self)




    def host(self):

        localctx = clfParser.HostContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_host)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 45
            _la = self._input.LA(1)
            if not(_la==clfParser.IP or _la==clfParser.STRING):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LognameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(clfParser.STRING, 0)

        def getRuleIndex(self):
            return clfParser.RULE_logname

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLogname" ):
                listener.enterLogname(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLogname" ):
                listener.exitLogname(self)




    def logname(self):

        localctx = clfParser.LognameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_logname)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47
            self.match(clfParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UsernameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(clfParser.STRING, 0)

        def getRuleIndex(self):
            return clfParser.RULE_username

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUsername" ):
                listener.enterUsername(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUsername" ):
                listener.exitUsername(self)




    def username(self):

        localctx = clfParser.UsernameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_username)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 49
            self.match(clfParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DatetimetzContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DATE(self):
            return self.getToken(clfParser.DATE, 0)

        def TIME(self):
            return self.getToken(clfParser.TIME, 0)

        def TZ(self):
            return self.getToken(clfParser.TZ, 0)

        def getRuleIndex(self):
            return clfParser.RULE_datetimetz

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDatetimetz" ):
                listener.enterDatetimetz(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDatetimetz" ):
                listener.exitDatetimetz(self)




    def datetimetz(self):

        localctx = clfParser.DatetimetzContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_datetimetz)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 51
            self.match(clfParser.T__0)
            self.state = 52
            self.match(clfParser.DATE)
            self.state = 53
            self.match(clfParser.T__1)
            self.state = 54
            self.match(clfParser.TIME)
            self.state = 55
            self.match(clfParser.TZ)
            self.state = 56
            self.match(clfParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RefererContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LITERAL(self):
            return self.getToken(clfParser.LITERAL, 0)

        def getRuleIndex(self):
            return clfParser.RULE_referer

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReferer" ):
                listener.enterReferer(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReferer" ):
                listener.exitReferer(self)




    def referer(self):

        localctx = clfParser.RefererContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_referer)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 58
            self.match(clfParser.LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RequestContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LITERAL(self):
            return self.getToken(clfParser.LITERAL, 0)

        def getRuleIndex(self):
            return clfParser.RULE_request

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRequest" ):
                listener.enterRequest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRequest" ):
                listener.exitRequest(self)




    def request(self):

        localctx = clfParser.RequestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_request)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 60
            self.match(clfParser.LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UseragentContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LITERAL(self):
            return self.getToken(clfParser.LITERAL, 0)

        def getRuleIndex(self):
            return clfParser.RULE_useragent

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUseragent" ):
                listener.enterUseragent(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUseragent" ):
                listener.exitUseragent(self)




    def useragent(self):

        localctx = clfParser.UseragentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_useragent)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            self.match(clfParser.LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatuscodeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(clfParser.STRING, 0)

        def getRuleIndex(self):
            return clfParser.RULE_statuscode

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatuscode" ):
                listener.enterStatuscode(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatuscode" ):
                listener.exitStatuscode(self)




    def statuscode(self):

        localctx = clfParser.StatuscodeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_statuscode)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 64
            self.match(clfParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BytesContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(clfParser.STRING, 0)

        def getRuleIndex(self):
            return clfParser.RULE_bytes

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBytes" ):
                listener.enterBytes(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBytes" ):
                listener.exitBytes(self)




    def bytes(self):

        localctx = clfParser.BytesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_bytes)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self.match(clfParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





