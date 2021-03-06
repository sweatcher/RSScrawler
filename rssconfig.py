# -*- coding: utf-8 -*-
# RSScrawler - Version 2.3.1
# Projekt von https://github.com/rix1337
# Enthält Code von:
# https://github.com/dmitryint (im Auftrag von https://github.com/rix1337)

import ConfigParser
import logging
import os, sys


class RssConfig(object):
    _CONFIG_FILES = [os.path.join(os.path.dirname(sys.argv[0]), 'Einstellungen/RSScrawler.ini')]
    _DEFAULT_CONFIG = {
        'RSScrawler': [
            ("jdownloader", "str", "", ""),
            ("port", "9090", "int", ""),
            ("prefix", "str", "", ""),
            ("interval", "int", "", ""),
            ("pushbulletapi","str","",""),
            ("hoster", """Uploaded,Share-Online""", "", "")
        ],
        'MB': [
            ("quality", """480p;720p;1080p""", "", ""),
            ("ignore","str","",""),
            ("historical","bool","",""),
            ("regex","bool","", ""),
            ("cutoff","bool","", ""),
            ("crawl3d","bool","",""),
            ("enforcedl", "bool", "", ""),
            ("crawlseasons", "bool", "", ""),
            ("seasonsquality", "str", "", ""),
            ("seasonssource", "str", "", "")
        ],
        'SJ': [
            ("quality", """480p;720p;1080p""", "", ""),
            ("rejectlist", "str", "", ""),
            ("regex","bool","", "")
        ]
    }
    __config__ = []

    def __init__(self, section):
        self._section = section
        self._config =  ConfigParser.RawConfigParser()
        try:
            self._config.read(self._CONFIG_FILES)
            self._config.has_section(self._section) or self._set_default_config(self._section)
            self.__config__ = self._read_config(self._section)
        except ConfigParser.DuplicateSectionError:
            logging.error('Doppelte Sektion in der Konfigurationsdatei.')
            raise
        except ConfigParser.Error:
            logging.error('Ein unbekannter Fehler in der Konfigurationsdatei ist aufgetreten.')
            raise

    def _set_default_config(self, section):
        self._config.add_section(section)
        for (key,key_type,comment,value) in self._DEFAULT_CONFIG[section]:
            self._config.set(section,key,value)
        with open(self._CONFIG_FILES.pop(), 'wb') as configfile:
            self._config.write(configfile)

    def _read_config(self, section):
        return [(key, '', '', self._config.get(section,key)) for key in self._config.options(section)]

    def _get_from_config(self, scope, key):
        res = [param[3] for param in scope if param[0] == key]
        if [param for param in self._DEFAULT_CONFIG[self._section] if param[0] == key and param[1] == 'bool']:
            return True if len(res) and res[0].strip('\'"').lower() == 'true' else False
        else:
            return res[0].strip('\'"') if len(res) > 0 else False

    def get(self, key):
        return self._get_from_config(self.__config__, key) or self._get_from_config(self._DEFAULT_CONFIG[self._section], key)
