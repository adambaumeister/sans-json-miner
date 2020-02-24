from __future__ import absolute_import

import logging
import requests
from xml.etree.ElementTree import ElementTree

from minemeld.ft.basepoller import BasePollerFT

LOG = logging.getLogger(__name__)

class SansJSON(BasePollerFT):
    def configure(self):
        super(SansJSON, self).configure()
        pass

    def _process_item(self, item):
        indicator = item["ipv4"]
        value = {
            'type': 'IPv4',
            'confidence': 100
        }
        return [[indicator, value]]


    def _build_iterator(self, now):
        url = self.config.get('url', "https://isc.sans.edu/api/threatlist/shodan?json")
        r = requests.get(url)

        j = r.json()
        return j