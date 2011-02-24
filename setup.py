#!/usr/bin/env python
#Copyright (C) 2010 Analyte Media
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
#conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""PyAuthorize setup script."""

__author__ = 'jordan.bouvier@analytemedia.com (Jordan Bouvier)'

from distutils.core import setup

setup(
    name='PyAuthorize',
    version='1.1.1',
    author='Jordan Bouvier',
    author_email='jordan.bouvier@analytemedia.com',
    url='http://open-source.analytemedia.com/pyauthorize',
    description='Python client for Authorize.net',
    long_description='A simple python client for Authorize.net\'s AIM API',
    classifiers=[
            'Programming Language :: Python',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Intended Audience :: Financial and Insurance Industry',
            'Intended Audience :: Information Technology',
            'Topic :: Office/Business :: Financial',
            'Topic :: Office/Business :: Financial :: Point-Of-Sale',
    ],
    py_modules=['pyauthorize', 'pyauthorize_test']
)