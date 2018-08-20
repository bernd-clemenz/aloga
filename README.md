# Access log analysis
The module takes access logs as written by Tomcat and finds IPs and does some
geo-location checks. The analyzer sits on top of common log file format
grammar for ANTLR4, which was modified to allow IPv6 addresses. Geo-data
are fetched via [ipstack](http://ipstack.com). A access key is required.

## Requirements
* Python 3 installed
* Internet connection
* (optional) Java 8 Runtime installed and available via PATH environment variable

[RPYC remote control](https://rpyc.readthedocs.io/en/latest/tutorial/tut1.html)

## Build Lexer/Parser
In case the grammar should be extended to cater for more cases:

In the etc/grammar directory do the following:
```bash
 java -jar ../tools/antlr-4.7.1-complete.jar -Dlanguage=Python3 clf.g4
```
Move the generated files to aloga/clf directory. Don't modify the files, even
they are not PEP8 compliant.

## Configuration
The module is configured by a traditional ini-file.

|Name | Description |
|-----|-------------|
| log.file | Name of the logging file |
| timeout | Timeout for HTTP requests |
| ipstack.key | Access key for ipstack API |


## Installation
### From source

```bash
git clone git@github.com:bernd-clemenz/aloga.git
```

Switch to the installation directory and run:

```bash
python setup.py
```

Setup takes care of resolving the dependencies.

## Execution
The module is executable like this:

```bash
python -m aloga --conf=aloga.ini --alogafile=access_log --out=access_data.json
```

## Resources
- [Antlr4](http://www.antlr.org/download.html)
- [Log file grammar](https://github.com/antlr/grammars-v4/blob/master/clf/clf.g4) 
- [IPv6](https://tools.ietf.org/html/draft-ietf-6man-text-addr-representation-04)

# Copyrights
For the grammar file clf.g4:

> BSD License
> Copyright (c) 2016, Tom Everett
> All rights reserved.