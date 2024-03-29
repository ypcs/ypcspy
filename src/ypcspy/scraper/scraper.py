#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Helper classes and functions for various tasks"""
# (c) 2012 Ville Korhonen <ville@xd.fi>

import requests
import requests_cache

import json

from lxml import html

CACHE_DEFAULT_NAME = "ypcspy"
CACHE_DEFAULT_TIMEOUT = 600 # 600 seconds, ie. 10 minutes
HTTP_DEFAULT_METHOD = 'GET'

def json_handler(obj):
    """Handle unknown formats when converting python objects to json"""
    # datetime.datetime
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError, "".join(['Object of type %s with value of ',
            '%s is not JSON serializable']) % (type(obj), repr(obj))

class ScraperMissingElementError(Exception):
    """HTML elements missing"""
    pass

class ScraperFetchError(Exception):
    """HTTP error"""
    pass

class Scraper(object):
    """Base class for building advanced web scraping apps

    >>> s = Scraper()
    >>> s.parse(url='http://www.google.com/', parser=html_title_parser)
    'Google'
    """
    def __init__(self, name=CACHE_DEFAULT_NAME, *args, **kwargs):
        self._name = name
        self._stats = {
            'fetched': 0,
        }

        if 'cache_time' in kwargs:
            cache_time = kwargs['cache_time'] / 60
        else:
            cache_time = CACHE_DEFAULT_TIMEOUT / 60
        requests_cache.configure(self._name, expire_after=cache_time)

    def _fetch(self, url, method='GET', *args, **kwargs):
        """Execute actual HTTP query using requests library"""
        t_method = method.lower()

        # TODO: submit also URL parameters or POST data payload if specified
        if t_method == 'get':
            response = requests.get(url)
        elif t_method == 'post':
            response = requests.post(url)
        else:
            raise ValueError, "".join([
                'Invalid fetch method %s, ',
                'possibly not implemented yet'
            ]) % t_method

        self._add_to_stats('fetched')

        return response.text

    def _add_to_stats(self, s_type):
        """Update stats"""
        if self._stats.has_key(s_type):
            self._stats[s_type] += 1
        else:
            self._stats[s_type] = 1
        return self._stats[s_type]

    def add_queue(self, url):
        """Add job to queue"""
        raise NotImplementedError

    def process_queue(self):
        """Start processing queue"""
        raise NotImplementedError

    def get(self, url, *args, **kwargs):
        """Fetch given URL using HTTP GET"""
        return self._fetch(url, method='get', *args, **kwargs)

    def post(self, url, *args, **kwargs):
        """Fetch given URL using HTTP POST"""
        return self._fetch(url, method='post', *args, **kwargs)

    def _format_parse_result(self, parsed, callback=None, format=None):
        if callback:
            callback(parsed)
        else:
            if format == 'json':
                return json.dumps(parsed, default=json_handler)
            else:
                return parsed

    def _limit_parse_result(self, parsed, *args, **kwargs):
        """Limit amount of results
        >>> from ypcspy.scraper.scraper import Scraper
        >>> s = Scraper()
        >>> parsed = ['a','b','c','d','e']
        >>> s._limit_parse_result(parsed)
        ['a', 'b', 'c', 'd', 'e']
        >>> s._limit_parse_result(parsed, limit=0)
        ['a', 'b', 'c', 'd', 'e']
        >>> s._limit_parse_result(parsed, limit=1)
        ['a']
        >>> s._limit_parse_result(parsed, limit=10)
        ['a', 'b', 'c', 'd', 'e']
        >>> s._limit_parse_result(parsed, limit=5)
        ['a', 'b', 'c', 'd', 'e']
        """
        if 'limit' in kwargs and kwargs['limit'] > 0 and len(parsed) > 1:
            parsed = parsed[0:int(kwargs['limit'])]
        return parsed

    def parse(self, url, parser, callback=None, format=None,
        method=HTTP_DEFAULT_METHOD, *args, **kwargs):
        """Parse given URL using parser and return results"""
        response = self._fetch(url, method=method)
        parsed = self._limit_parse_result(parser(response, *args, **kwargs), *args, **kwargs)

        return self._format_parse_result(parsed, callback=callback, format=format)

def html_title_parser(content, *args, **kwargs):
    """Parse page title from HTML source

    >>> from ypcspy.scraper.scraper import html_title_parser
    >>> html_title_parser('<html><head><title>Test</title></head></html>')
    'Test'
    >>> html_title_parser('<head><title>Test</title></head>')
    'Test'
    >>> html_title_parser('<title>Test</title>')
    'Test'
    >>> html_title_parser('<head><title>Test</title><title>Test2</title></head>')
    'Test'
    """
    doc = html.fromstring(content)
    title = doc.xpath('/html/head/title/text()')
    if len(title) == 0:
        raise ScraperMissingElementError, 'Document doesnt have html/head/title'
    else:
        return title[0]
    return title
