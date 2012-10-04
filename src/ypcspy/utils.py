#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Helper classes and functions for various tasks"""
# (c) 2012 Ville Korhonen <ville@xd.fi>

import sys
from lxml import html
from ypcspy.scraper import Scraper, ScraperMissingElementError

# opts = {'throttle': "50/60',} # 50 queries in 60 seconds
# s = Scraper(name='koaschat', baseurl='http://ypcs.fi/data', opts)
# users = s.parse('sample.json', parser=get_users)
# s.add_queue(['sample1.json', 'sample2.json', 'sample3.json', 'sample4.json'])
# s.add_queue([{'url':'sample5.json', 'callback': add_events,
# 'parser': parse_events,}])
# s.process_queue()

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
        title = scraper.parse(url, parser=html_title_parser)
        print title
        return 0
    return 1


def run():
    """Run main() and return"""
#    parser = argparse.ArgumentParser(description="Scraping Tool")
    args = sys.argv[1:]
#    args = parser.parse_args()
    sys.exit(main(args) or 0)

if __name__ == "__main__":
    run()
