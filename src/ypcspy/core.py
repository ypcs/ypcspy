#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse

def main(args):
    # TODO: do something w/ args
    if args.command == 'scrape':
        from ypcspy.scraper.cli import run as run_scrape
        return run_scrape(args)
    else:
        print "Nothing to do, I assume"
        return 0

def run():
    parser = argparse.ArgumentParser(description='ypcspy')
    parser.add_argument('command')
    parser.add_argument('args', nargs='+')    
    args = parser.parse_args()
    sys.exit(main(args) or 0)

if __name__ == "__main__":
    run()
