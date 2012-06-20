#!/usr/bin/env python
#
# Diamond example web application
#
# This code is licensed under a permissive license and is meant to be
# copied and incorporated into other projects.
#
# Copyright (c) 2012, Carnegie Mellon University
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

from flask import (Flask, abort, redirect, render_template, request, session,
        url_for)
import json
from opendiamond.scope import ScopeCookie, get_blaster_map
from optparse import OptionParser
import urllib2
from urlparse import urljoin
import uuid

app = Flask(__name__)
app.config.from_object(__name__)


# In a real application, these would be database tables.  They would also
# need garbage collection.
search_state = {}
result_state = {}


@app.before_request
def csrf_protect():
    request.csrf_token = request.cookies.get('csrf_token', str(uuid.uuid4()))
    if request.method == 'POST':
        if request.form.get('_csrf_token', None) != request.csrf_token:
            abort(403, 'Bad or missing CSRF token')


@app.after_request
def csrf_set(response):
    response.set_cookie('csrf_token', request.csrf_token, max_age=3600*24*30)
    return response


@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Parse form
        try:
            cookie = request.files['cookie'].read()
            orientation = request.form['orientation']
        except KeyError:
            abort(400, 'Bad form submission')

        # Split megacookie into a list of cookies per JSON Blaster
        cookies = get_blaster_map([ScopeCookie.parse(c)
                for c in ScopeCookie.split(cookie)])

        # Make sure at least one cookie specifies a Blaster
        if not cookies:
            abort(400, 'No cookies or no JSON Blaster specified')

        # Create searches
        def static_url(path):
            return urljoin(request.url_root, url_for('static', filename=path))
        searches = []
        for blaster, cookie_list in cookies.iteritems():
            config = {
                'cookies': [c.encode() for c in cookie_list],
                'filters': [
                    {
                        'name': 'RGB',
                        'code': {
                            'uri': static_url('filters/fil_decode'),
                        },
                        'min_score': 1,
                    }, {
                        'name': 'Orientation',
                        'code': {
                            'uri': static_url('filters/fil_orientation'),
                        },
                        'arguments': [orientation],
                        'min_score': 1,
                    }
                ],
            }
            req = urllib2.Request(blaster, json.dumps(config), {
                'Content-Type': 'application/json',
                'User-Agent': 'webappfind/0.1',
            })
            try:
                response = urllib2.urlopen(req)
            except urllib2.HTTPError, e:
                abort(400, e.read() or e.reason)
            except urllib2.URLError, e:
                abort(400, e.reason)
            searches.append(json.loads(response.read()))

        # Add to global state
        id = str(uuid.uuid4())
        search_state[id] = searches

        return redirect(url_for('results', id=id))
    else:
        return render_template('search.html')


@app.route('/results/<id>')
def results(id):
    try:
        searches = search_state[id]
    except KeyError:
        abort(404)
    return render_template('results.html', searches=searches)


@app.route('/result', methods=['POST'])
def make_result():
    # Parse form
    try:
        result_url = request.form['result_url']
    except KeyError:
        abort(400, 'Bad form submission')

    # Add global state
    id = str(uuid.uuid4())
    result_state[id] = result_url
    return redirect(url_for('result', id=id))


@app.route('/result/<id>')
def result(id):
    try:
        result_url = result_state[id]
    except KeyError:
        abort(404)
    return render_template('result.html', result_url=result_url)


if __name__ == '__main__':
    parser = OptionParser(usage='Usage: %prog [options]')
    parser.add_option('-d', '--debug', dest='DEBUG', action='store_true',
                help='run in debugging mode (insecure)')
    parser.add_option('-l', '--listen', metavar='ADDRESS', dest='host',
                default='127.0.0.1',
                help='address to listen on [127.0.0.1]')
    parser.add_option('-p', '--port', metavar='PORT', dest='port',
                type='int', default=5000,
                help='port to listen on [5000]')

    (opts, args) = parser.parse_args()
    # Overwrite only those settings specified on the command line
    for k in dir(opts):
        if not k.startswith('_') and getattr(opts, k) is None:
            delattr(opts, k)
    app.config.from_object(opts)

    # We must run multithreaded because the JSON Blaster calls us back
    # while we are processing a search request
    app.run(host=opts.host, port=opts.port, threaded=True)
