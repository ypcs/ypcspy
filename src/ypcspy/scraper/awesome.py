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

    def _get_slice_xpath(self, slice, doc):
        if isinstance(slice, dict) and slice.has_key('xpath'):
            return doc.xpath(slice['xpath'])
        else:
            return None

    def _parse_slices(self, slice, doc, recursion=0):
        print type(doc)
        print slice
        print recursion
        recursion += 1
        if isinstance(doc, list):
            for d in doc:
                if slice.has_key('slice'):
                    results = []

                    for s in slice['slice']:
                        result = self._parse_slices(s, self._get_slice_xpath(s, d), recursion)
                        results.append(result)
                    return results
                else:
                    return self._get_slice_xpath(slice, d)
        else:
            if slice.has_key('slice'):
                results = []
                for s in slice['slice']:
                    result = self._parse_slices(s, self._get_slice_xpath(s, doc), recursion)
                    results.append(result)
                return results
            else:
                return self._get_slice_xpath(slice, doc)
                                    
        
        # 1. kerta: doc = lxml.html.HtmlElement, slice = 

    def _get_collections(self, definition):
        # TODO: sisältääkö definition collectioneja?
        results = []
        if definition.has_key('collections'):
            for c in definition['collections']:
                results.append(c)
        return  results      

    def parse(self, url):
        defs = self._get_matching_definitions(url)

        if len(defs) == 0:
            raise AwesomeScraperNoDefinitionError, 'No valid parsers found for %s' % url

        # TODO: Create logic to choose between multiple defs OR combine results from multiple

        # TODO: Support othet methods in addition to default (GET)
        doc = html.fromstring(self._fetch(url))
        results = []
        collections = []
    
        for d in defs:
            collections += self._get_collections(d)
        
        for c in collections:
            collection = {
                'name': c['name'],
                'slices': self._parse_slices(slice=c, doc=doc),            
            }
            results.append(collection)

        return self._format_parse_result(results)

a = AwesomeScraper(cache_time=3600)
print a.parse('http://koas.fi/keskustelu')
#a.parse('http://www.google.fi')
