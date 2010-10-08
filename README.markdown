<img src="http://github.com/redlego/scraper/raw/master/redlego.png" />

What is RedLego?
----------------

It's been very difficult to compare the price of Adobe software
from territory to territory in a meaningful way. So here's RedLego, a
Python script that visits all the online stores, checks the prices,
converts them to $US at the current exchange rate and puts them all in
a handy json file for you to access.

There are two repositories: JSON price data and the scraper.

### JSON Price Data ###

**[http://github.com/redlego/data/](http://github.com/redlego/data/)**

You can access the raw JSON file at:

[http://github.com/redlego/data/master/prices.json](http://github.com/redlego/data/master/prices.json)

### Scraper ###

**[http://github.com/redlego/scraper/](http://github.com/redlego/scraper/)**

To install the scraper you will need:

* [pip](http://pypi.python.org/pypi/pip)
* [virtualenv](http://pypi.python.org/pypi/virtualenv)
* [virtualenvwrapper](http://pypi.python.org/pypi/virtualenvwrapper)
* An API key from [Exchange Rate API](http://exchangerate-api.com/api-key) (free).

To install:

    git clone http://github.com/redlego/scraper.git
    cd scraper
    mkvirtualenv scraper
    pip install -E scraper -r requirements.txt

Put your [Exchange Rate API key](http://exchangerate-api.com/api-key) in a file called `currency_api_key`.

Run `python redlego.py`
