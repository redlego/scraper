# -*- coding: utf-8 -*-

from scrapelib import Scraper
from pyquery import PyQuery
import unicodedata
import settings
import json
import re

scraper = Scraper(requests_per_minute=20, use_cache_first=True)


class Store(object):
    """Class to represent a store for a particular country"""

    def __init__(self, path):
        """Load the store from the given path. Will keep retrying
        until the loaded HTML can be successfully parsed and
        some table rows can be extracted. Prints progress
        to stdout
        """
        self.path = path
        self.load_attempts = 0

        print "\nLoading store from url: %s" % self.path

        # Keep retrying loading the store HTML until we get some rows
        while self.row_count == 0:
            self.load_attempts += 1
            if self.load_attempts > 1:
                print "\tNo rows found, retrying..."
            self.load_page()
        print "Loaded store: %s" % self.name

    def load_page(self):
        url_base = settings.STORE_URL_BASE
        self.raw_page = scraper.urlopen(url_base % self.path)
        self.pyquery = PyQuery(self.raw_page)

    @property
    def name(self):
        name = self.pyquery('h1#pageHeader').text()
        for to_remove in settings.REMOVE_FROM_STORE_NAMES:
            name = name.replace(to_remove, '')
        return name

    @property
    def slug(self):
        """Return a lowercased and normalised string representing the name of the store"""
        name = self.name.lower().replace(' ', '-')
        return unicodedata.normalize('NFKD', unicode(name)).encode('ASCII', 'ignore')

    @property
    def row_count(self):
        if not hasattr(self, 'pyquery'):
            return 0
        return len(self.rows)

    @property
    def rows(self):
        return self.pyquery('table#catalog tbody tr')

    @property
    def products(self):
        for row in self.rows:
            yield Product(row)


class Product(object):
    """Class to represent a product"""

    def __init__(self, row):
        self.raw_row = row
        self.pyquery = PyQuery(self.raw_row)

    @property
    def name(self):
        return self.pyquery('td h4 a').text().replace('Adobe ', '')

    @property
    def slug(self):
        """Return a lowercased and normalised string representing the name of the product"""
        return self.name.lower().replace(' ', '-')

    @property
    def full_price_without_tax(self):
        query = self.pyquery('span.priceWithoutTax')
        # The full price is the rightmost priceWithoutTax span
        price_string = query.eq(len(query) - 1).text()
        return Price(price_string)


class CurrencyParser(object):
    """Class to handle splitting a currency string into parts.
    Example strings that the class can deal with:

    € 199,00  exkl. MwSt.
    £651.99 ex VAT
    £2,109.00 ex VAT
    US $2,599.00
    US $299.00
    € 1.199,99  exkl. MwSt.
    CHF 1'932.16 exkl. MwSt.

    Construct the class, passing in the string:

        parser = CurrencyParser('US $2,599.00')

    You can now use the `symbol` and `amount` properties to access
    parts of the parsed current string

        parser.symbol # will be "US $"
        parser.amount # will be (float) 2599.00
    """

    def __init__(self, currency_string):

        # Extract the currency symbol
        parts = re.split(r"(\d)", currency_string, 1)
        self.symbol = parts[0].strip()

        # Rejoin the rest of the string and remove any trailing stuff
        rest = "".join(parts[1:])
        currency_string = self.remove_trailing(rest)

        self.amount = float(self.parse_currency(currency_string))

    def remove_trailing(self, currency_string):
        parts = re.split(r"(\d )", currency_string, 1)
        if len(parts) == 1:
            return parts[0]
        else:
            return "".join(parts[0:2]).strip()

    def parse_currency(self, currency_string):

        # Remove anything that isn't a digit, comma or dot
        currency_string = re.sub(r'[^\d,.]', '', currency_string)

        first_comma = currency_string.find(',')
        first_dot = currency_string.find('.')

        # 100 - probably won't happen
        if first_comma == -1 and first_dot == -1:
            return currency_string

        # 100.00 - just return this
        if first_comma == -1:
            return currency_string

        # 100,00
        if first_dot == -1:
            return currency_string.replace(',', '.')

        # 100,000.00
        if first_comma < first_dot:
            return currency_string.replace(',', '')

        # 100.00,00
        if first_dot < first_comma:
            return currency_string.replace('.', '').replace(',', '.')


class Price(object):
    """Class to represent a price. Uses the xurrency.com API to convert"""

    base_url = 'http://www.exchangerate-api.com/%s/%s/%s?k=%s'

    def __init__(self, price):
        self.raw_price = price
        if price is not None:
            self.parser = CurrencyParser(price)

    @property
    def amount(self):
        if self.raw_price is not None:
            return self.parser.amount

    @property
    def currency_symbol(self):
        if self.raw_price is not None:
            return self.parser.symbol

    @property
    def currency_code(self):
        """Look up the currency symbol in the currency code dict in settings.py"""
        if self.raw_price is not None:
            symbol = self.currency_symbol
            if symbol not in settings.CURRENCIES:
                raise CurrencyError('Unknown currency symbol: %s' % symbol)
            return settings.CURRENCIES[symbol]

    def convert(self):
        """Convert price to the base currency setting defined in settings.py"""
        amount = self.amount
        if amount is None:
            return None
        code = self.currency_code
        if code == settings.BASE_CURRENCY:
            return self.format_currency(amount)
        response = scraper.urlopen(self.base_url % (code, settings.BASE_CURRENCY, amount, settings.CURRENCY_CONVERSION_API_KEY))
        return self.format_currency(response)

    def format_currency(self, amount):
        return "%.2f" % float(amount)


class Storage(object):
    """Class to store and serialise data extracted from the Adobe store pages"""

    products = {}

    def add_record(self, product_slug, product_name, store_slug, amount):
        if product_slug not in self.products:
            self.products[product_slug] = {
                'product-name': product_name,
                'prices': {},
            }
        self.products[product_slug]['prices'][store_slug] = amount

    def dump_json(self):
        return json.dumps(self.products, indent=4)


class CurrencyError(Exception):
    def __init___(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

"""Load and process data from the Adobe store pages"""
if __name__ == "__main__":
    try:
        storage = Storage()
        for path in settings.PATHS:
            store = Store(path)
            for product in store.products:
                print "\tprocessing product %s" % product.slug
                storage.add_record(
                    product.slug,
                    product.name,
                    store.slug,
                    product.full_price_without_tax.convert(),
                )

        print "Dumping JSON file to %s" % settings.OUTPUT_FILE
        open(settings.OUTPUT_FILE, 'w').write(storage.dump_json())
    except CurrencyError as e:
        print "ERROR: %s" % repr(e)
