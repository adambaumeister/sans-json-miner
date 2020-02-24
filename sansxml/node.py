from __future__ import absolute_import

import logging
import requests
from xml.etree.ElementTree import ElementTree

from . import basepoller

LOG = logging.getLogger(__name__)

class SansXML(basepoller.BasePollerFT):
    def configure(self):
        pass

    def _process_item(self, item):
        # called on each item returned by _build_iterator
        # it should return a list of (indicator, value) pairs
        indicator = item["IPv4"]
        value = {
            'type': 'IPv4',
            'confidence': 100
        }
        return [[indicator, value]]


    def _build_iterator(self, now):
        url = "https://isc.sans.edu/api/threatlist/shodan?json"
        r = requests.get(url)

        j = r.json()
        return j