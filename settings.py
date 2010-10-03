# -*- coding: utf-8 -*-

import os.path
import sys

CURRENCY_API_KEY_FILE = 'currency_api_key'

if not os.path.exists(CURRENCY_API_KEY_FILE):
    print "Create a file called %s and put your exchangerate-api.com API key in it." % CURRENCY_API_KEY_FILE
    print "To get a (free) API key, go to http://exchangerate-api.com/api-key"
    sys.exit(1)

CURRENCY_CONVERSION_API_KEY = open(CURRENCY_API_KEY_FILE).read().strip()

STORE_URL_BASE = 'https://store2.adobe.com/cfusion/store/html/index.cfm?store=OLS-%s&event=displayCatalog'

PATHS = [
    'US',
    'UK',
    'AT',
    'BE',
    'EU',
    'DK',
    'FI',
    'FR',
    'DE',
    'IE',
    'SE',
    'CH',
]

BASE_CURRENCY = 'usd'

CURRENCIES = {
    u'£': 'gbp',
    u'US $': 'usd',
    u'€': 'eur',
    u'CHF': 'chf',
    u'DKK': 'dkk',
    u'NOK': 'nok',
    u'SEK': 'sek',
}

REMOVE_FROM_STORE_NAMES = [
    u'Adobe Store - ',
    u'Adobe Store – ',
    u'Adobe Download Store - ',
    u'Adobe Online Store - ',
    u'Boutique en ligne Adobe - ',
]

OUTPUT_FILE = "adobe_prices.json"
