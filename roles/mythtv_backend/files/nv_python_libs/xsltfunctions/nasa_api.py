#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# ----------------------
# Name: nasa_api - XPath and XSLT functions for the NASA RSS/HTML items
# Python Script
# Author:   R.D. Vaughan
# Purpose:  This python script is intended to perform a variety of utility functions
#           for the conversion of data to the MNV standard RSS output format.
#           See this link for the specifications:
#           http://www.mythtv.org/wiki/MythNetvision_Grabber_Script_Format
#
# License:Creative Commons GNU GPL v2
# (http://creativecommons.org/licenses/GPL/2.0/)
#-------------------------------------
__title__ ="nasa_api - XPath and XSLT functions for the NASA RSS/HTML"
__author__="R.D. Vaughan"
__purpose__='''
This python script is intended to perform a variety of utility functions
for the conversion of data to the MNV standard RSS output format.
See this link for the specifications:
http://www.mythtv.org/wiki/MythNetvision_Grabber_Script_Format
'''

__version__="v0.1.0"
# 0.1.0 Initial development


# Specify the class names that have XPath extention functions
__xpathClassList__ = ['xpathFunctions', ]

# Specify the XSLT extention class names. Each class is a stand lone extention function
#__xsltExtentionList__ = ['xsltExtExample', ]
__xsltExtentionList__ = []

import os, sys, re, time, datetime, shutil, urllib, string
from copy import deepcopy


class OutStreamEncoder(object):
    """Wraps a stream with an encoder"""
    def __init__(self, outstream, encoding=None):
        self.out = outstream
        if not encoding:
            self.encoding = sys.getfilesystemencoding()
        else:
            self.encoding = encoding

    def write(self, obj):
        """Wraps the output stream, encoding Unicode strings with the specified encoding"""
        if isinstance(obj, unicode):
            try:
                self.out.write(obj.encode(self.encoding))
            except IOError:
                pass
        else:
            try:
                self.out.write(obj)
            except IOError:
                pass

    def __getattr__(self, attr):
        """Delegate everything but write to the stream"""
        return getattr(self.out, attr)
sys.stdout = OutStreamEncoder(sys.stdout, 'utf8')
sys.stderr = OutStreamEncoder(sys.stderr, 'utf8')

try:
    from StringIO import StringIO
    from lxml import etree
except Exception, e:
    sys.stderr.write(u'\n! Error - Importing the "lxml" and "StringIO" python libraries failed on error(%s)\n' % e)
    sys.exit(1)

# Check that the lxml library is current enough
# From the lxml documents it states: (http://codespeak.net/lxml/installation.html)
# "If you want to use XPath, do not use libxml2 2.6.27. We recommend libxml2 2.7.2 or later"
# Testing was performed with the Ubuntu 9.10 "python-lxml" version "2.1.5-1ubuntu2" repository package
version = ''
for digit in etree.LIBXML_VERSION:
    version+=str(digit)+'.'
version = version[:-1]
if version < '2.7.2':
    sys.stderr.write(u'''
! Error - The installed version of the "lxml" python library "libxml" version is too old.
          At least "libxml" version 2.7.2 must be installed. Your version is (%s).
''' % version)
    sys.exit(1)


class xpathFunctions(object):
    """Functions specific extending XPath
    """
    def __init__(self):
        self.functList = ['nasaTitleEp', ]
        # Show 1
        self.regexPattern = re.compile(u'''Show\\ (?P<seasno>[0-9]+).*$''', re.UNICODE)
    # end __init__()

######################################################################################################
#
# Start of XPath extension functions
#
######################################################################################################

    def nasaTitleEp(self, context, *arg):
        '''Parse the guid element and extract an episode number
        Call example: 'mnvXpath:nasaTitleEp(string(title))'
        return the a massaged title element and an episode element
        '''
        stripArray = ['HST SM4:', 'NASA 360:', 'NASA 360', 'NASA EDGE:', 'NASA EDGE', 'NE Live@', 'NE@', 'NASA Mission Update:', "NASA TV's This Week @NASA," ]
        title = arg[0]
        for stripText in stripArray:
            title = title.replace(stripText, u'')
        title = title.strip()
        episodeNumber = None
        if title.startswith('Show'):
            match = self.regexPattern.match(title)
            if match:
                episodeNumber = match.groups()
                episodeNumber = int(episodeNumber[0])
                title = title[title.find(':')+1:].strip()

        mythtvNamespace = "http://www.mythtv.org/wiki/MythNetvision_Grabber_Script_Format"
        mythtv = "{%s}" % mythtvNamespace
        NSMAP = {'mythtv' : mythtvNamespace}
        elementTmp = etree.Element(mythtv + "mythtv", nsmap=NSMAP)
        if not episodeNumber is None:
            etree.SubElement(elementTmp, "title").text = u"EP%02d: %s" % (episodeNumber, title)
            etree.SubElement(elementTmp, mythtv + "episode").text = u"%s" % episodeNumber
        else:
            etree.SubElement(elementTmp, "title").text = title
        return elementTmp
    # end nasaTitleEp()

######################################################################################################
#
# End of XPath extension functions
#
######################################################################################################

######################################################################################################
#
# Start of XSLT extension functions
#
######################################################################################################

######################################################################################################
#
# End of XSLT extension functions
#
######################################################################################################
