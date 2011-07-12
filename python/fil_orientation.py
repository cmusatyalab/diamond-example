#!/usr/bin/python
#
# Diamond example image filter
#
# This code is licensed under a permissive license and is meant to be
# copied and incorporated into other projects.
#
# Copyright (c) 2011, Carnegie Mellon University
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

class OrientationFilter(Filter):
    name = 'Orientation'
    params = Parameters(
        ChoiceParameter("Image orientation", (
            ('horz', "Horizontal"),
            ('vert', "Vertical"),
        )),
    )

    def __init__(self, *args, **kwargs):
        Filter.__init__(self, *args, **kwargs)
        self.want_vertical = (self.args[0] == 'vert')

    def __call__(self, obj):
        width, height = obj.image.size
        if (height < width) ^ self.want_vertical:
            return True
        else:
            return False


if __name__ == '__main__':
    run_filter(sys.argv, OrientationFilter)
