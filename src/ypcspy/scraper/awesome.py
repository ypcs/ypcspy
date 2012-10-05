# -*- coding: utf-8 -*-

import os
import json
import re

from lxml import html

from ypcspy.scraper import Scraper

# TODO: Lue sivustokohtaiset XPATH-määritykset json-tiedostosta, ja tulosta sen mukaista juttua sitten kivasti <3

DEFINITION_FILE_EXTENSION = ".json"
TEST_DEFINITIONS = "~/.ypcspy/scraper/sites"

class AwesomeScraperNoDefinitionError(Exception):
    pass

class AwesomeScraper(Scraper):
    def __init__(self, *args, **kwargs):
        self._definitions = []

        definition_path = os.path.expanduser(TEST_DEFINITIONS)
        self._load_definitions(path=definition_path)

        super(AwesomeScraper, self).__init__()

    def _get_definition_files(self, path):
        if not os.path.exists(path):
            raise IOError, 'Invalid definition path %s' % path
        files = ["%s/%s" % (path, f) for f in os.listdir(path) if f.endswith(DEFINITION_FILE_EXTENSION)]
        return files

    def _load_definitions(self, path):
        files = self._get_definition_files(path)
        for f in files:
            content = json.load(open(f, 'r'))
            self._definitions += content

    def _get_matching_definitions(self, url):
        matches = []

        for d in self._definitions:
            p = re.compile(d['url'])
            m = p.match(url)
            if m:
                matches.append(d)
        return matches

    def _get_content(self, doc, c):
        print c

    def parse(self, url):
        defs = self._get_matching_definitions(url)

        if len(defs) == 0:
            raise AwesomeScraperNoDefinitionError, 'No valid parsers found for %s' % url

        # TODO: Create logic to choose between multiple defs OR combine results from multiple

        # TODO: Support othet methods in addition to default (GET)
        doc = html.fromstring(self._fetch(url))

        results = []

        for d in defs:
            slices = d['slices']
            t_result = []

            for s in slices:
                print s['description']
                result = self._get_content(doc, s['content'])
                t_result.append(result)
            results.append(t_result)

        # TODO: format results
        return results

a = AwesomeScraper()
a.parse('http://koas.fi/keskustelu')
#a.parse('http://www.google.fi')
