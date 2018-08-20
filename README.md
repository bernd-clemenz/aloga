# Access log analysis
The module takes access logs as written by Tomcat and finds IPs and does some
geo-location checks. The analyzer sits on top of common log file format
grammar for ANTLR4, which was modified to allow IPv6 addresses. Geo-data
are fetched via [ipstack](http://ipstack.com). A access key is required.

[RPYC remote control](https://rpyc.readthedocs.io/en/latest/tutorial/tut1.html)

## Build Lexer/Parser
In the etc/grammar directory do the following:
```bash
 java -jar ../tools/antlr-4.7.1-complete.jar -Dlanguage=Python3 clf.g4
```
Move the created files to aloga/clf directory.

## Resources
[Antlr4](http://www.antlr.org/download.html)
[Log file grammar](https://github.com/antlr/grammars-v4/blob/master/clf/clf.g4) 
[IPv6](https://tools.ietf.org/html/draft-ietf-6man-text-addr-representation-04)
