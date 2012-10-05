# -*- coding: utf-8 -*-

import os
import json
import re

from ypcspy.scraper import Scraper

# TODO: Lue sivustokohtaiset XPATH-määritykset json-tiedostosta, ja tulosta sen mukaista juttua sitten kivasti <3

DEFINITION_FILE_EXTENSION = ".json"
TEST_DEFINITIONS = "~/.ypcspy/scraper/sites"

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
        
    def _parser(self, content, *args, **kwargs):
        pass

    def parse(self, url):
        pass


a = AwesomeScraper()
