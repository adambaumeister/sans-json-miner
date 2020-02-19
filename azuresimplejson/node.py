import logging
import json

import requests
import bs4  # we use bs4 to parse the HTML page

from minemeld.ft.json import SimpleJSON

LOG = logging.getLogger(__name__)

AZUREXML_URL = \
    'https://www.microsoft.com/EN-US/DOWNLOAD/confirmation.aspx?id=41653'

AZUREJSON_URL = 'https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519'

REGIONS_XPATH = '/AzurePublicIpAddresses/Region'


class AzureSimpleJSON(SimpleJSON):
    def configure(self):
        super(AzureSimpleJSON, self).configure()

        self.polling_timeout = self.config.get('polling_timeout', 20)
        self.verify_cert = self.config.get('verify_cert', True)

    def _build_request(self, now):
        r = requests.Request(
            'GET',
            AZUREJSON_URL
        )

        return r.prepare()

    def _build_iterator(self, now):
        _iterators = []

        rkwargs = dict(
            stream=False,
            verify=self.verify_cert,
            timeout=self.polling_timeout
        )

        r = requests.get(
            AZUREJSON_URL,
            **rkwargs
        )

        try:
            r.raise_for_status()
        except:
            LOG.error('%s - exception in request: %s %s',
                      self.name, r.status_code, r.content)
            raise

        html_soup = bs4.BeautifulSoup(r.content, "lxml")
        a = html_soup.find('a', class_='failoverLink')
        if a is None:
            LOG.error('%s - failoverLink not found', self.name)
            raise RuntimeError('{} - failoverLink not found'.format(self.name))
        LOG.debug('%s - download link: %s', self.name, a['href'])

        rkwargs = dict(
            stream=True,
            verify=self.verify_cert,
            timeout=self.polling_timeout
        )

        r = requests.get(
            a['href'],
            **rkwargs
        )
        result = self.extractor.search(r.json())
        dicts = []
        for r in result:
            if "properties" in r:
                props = r["properties"]
                if "addressPrefixes" in props:
                    for addr_prefix in props["addressPrefixes"]:
                        d = {}
                        d["ip_prefix"] = addr_prefix

                        dicts.append(d)

        return dicts
