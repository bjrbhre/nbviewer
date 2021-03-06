#-----------------------------------------------------------------------------
#  Copyright (C) 2013 The IPython Development Team
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------

import re

def url_path_join(*pieces):
    """Join components of url into a relative url

    Use to prevent double slash when joining subpath. This will leave the
    initial and final / in place
    """
    initial = pieces[0].startswith('/')
    final = pieces[-1].endswith('/')
    stripped = [s.strip('/') for s in pieces]
    result = '/'.join(s for s in stripped if s)
    if initial:
        result = '/' + result
    if final:
        result += '/'
    if result == '//':
        result = '/'
    return result

GIST_RGX = re.compile(r'^([a-f0-9]+)/?$')
GIST_URL_RGX = re.compile(r'^https?://gist.github.com/(\w+/)?([a-f0-9]+)/?$')
GITHUB_URL_RGX = re.compile(r'^https?://github.com/(\w+)/(\w+)/blob/(.*)$')
RAW_GITHUB_URL_RGX = re.compile(r'^https?://raw.?github.com/(\w+)/(\w+)/(.*)$')

def transform_ipynb_uri(value):
    """Transform a given value (an ipynb 'URI') into an app URL"""
    gist_n = GIST_RGX.match(value)
    if gist_n:
        return u'/%s' % gist_n.groups()[0]

    gist_url = GIST_URL_RGX.match(value)
    if gist_url:
        return u'/%s' % gist_url.group(2)

    github_url = GITHUB_URL_RGX.match(value)
    if github_url:
        user, repo, path = github_url.groups()
        return u'/github/%s/%s/blob/%s' % (user, repo, path)
    
    raw_github_url = GITHUB_URL_RGX.match(value)
    if raw_github_url:
        user, repo, path = raw_github_url.groups()
        return u'/github/%s/%s/blob/%s' % (user, repo, path)

    if value.startswith('https://'):
        return u'/urls/%s' % value[8:]

    if value.startswith('http://'):
        return u'/url/%s' % value[7:]

    return u'/url/%s' % value