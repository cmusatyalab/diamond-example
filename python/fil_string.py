#!/usr/bin/python
#
# Diamond example filter
#
# This code is licensed under a permissive license and is meant to be
# copied and incorporated into other projects.
#
# Copyright (c) 2008-2011, Carnegie Mellon University
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#
# * Neither the name of the Carnegie Mellon University nor the names
#    of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

from opendiamond.filter import Filter, run_filter
from opendiamond.filter.parameters import *
import sys

class StringFilter(Filter):
    name = 'String filter'
    params = Parameters(
        StringParameter('Search string'),
    )
    # Override default dependency on RGB image filter, since we're not
    # processing image data
    dependencies = []

    def __init__(self, *args, **kwargs):
        Filter.__init__(self, *args, **kwargs)
        self.target_str = self.args[0]

    def __call__(self, obj):
        # See if the target string is in the object data
        loc = obj.data.find(self.target_str)
        if loc == -1:
            # Not found, fail object
            return 0
        else:
            # Found, put offset into object attribute
            obj['string-index'] = loc
            # Pass object
            return 1


if __name__ == '__main__':
    run_filter(sys.argv, StringFilter)
