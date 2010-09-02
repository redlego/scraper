# -*- coding: utf-8 -*-

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
