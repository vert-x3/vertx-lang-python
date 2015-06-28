from __future__ import unicode_literals, absolute_import

import sys

if sys.version_info[0] < 3:
    long = long
    basestring = basestring
else:
    long = int
    basestring = str
