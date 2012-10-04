#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Helper classes and functions for various tasks"""
# (c) 2012 Ville Korhonen <ville@xd.fi>

import sys
from lxml import html
from ypcspy.scraper import Scraper, ScraperMissingElementError

def html_title_parser(content, *args, **kwargs):
    """Parse page title from HTML source"""
    doc = html.fromstring(content)
    title = doc.xpath('/html/head/title/text()')
    if len(title) == 0:
        raise ScraperMissingElementError, 'Document doesnt have html/head/title'
    else:
        return title[0]
    return title

def main(args):
    """CLI"""
    scraper = Scraper(name='scrapetool')
    
    if len(args) == 1:
        url = args[0]
    else:
        print "Y U NO URL give?"
        return 1
    
    print scraper.parse(url, parser=html_title_parser) 
    
    return 0

def run(args):
    """Run main() and return"""

    return main(args.args) or 0
