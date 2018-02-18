import requests
import os
import json
import datetime
import matplotlib.pyplot as plt

import private

import hmac, hashlib, time, requests, base64
from requests.auth import AuthBase

# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = signature.digest().encode('base64').rstrip('\n')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request


class gdax_interface:
    def __init__(self):
        self.url = 'https://api.gdax.com'
        self.product_id = 'LTC-USD'

    def set_product_id(self, id):
        self.product_id = id

    def get(self, path):
        response = requests.get(self.url + path)

        return response.json()

    def post(self, path, content, auth=False):
        # response = requests.post(self.url + path, auth=auth)
        response = requests.post(self.url + '/orders', json=content, auth=auth)

        return response.json()

    def get_products(self):
        return self.get('/products')

    def get_order_book(self, level = False):

        request_url = '/products/' + self.product_id + '/book'
        if level:
            request_url += '?level=' + str(level)

        return self.get(request_url)

    def get_historic_rates(self, start, stop, granularity = '60'):
        request_url = '/products/' + self.product_id + '/candles'
        request_url += '?start=' + str(start)
        request_url += '?stop=' + str(stop)
        request_url += '?granularity=' + str(granularity)

        return self.get(request_url)

    def plot_historic_rates(self, json_response):
        keys = ['time', 'low', 'high', 'open', 'close', 'volume']

        arrs = zip(*json_response)


        f, axarr = plt.subplots(len(keys)-1, sharex=True)




        for idx, val in enumerate(keys):
            if idx == 0:
                continue

            time = arrs[0]

            axarr[idx-1].plot(time, arrs[idx])
            axarr[idx-1].set_title(val)
            axarr[idx-1].grid()


        plt.show()


    def post_limit_order(self, side, price, size):

        key, secret, auth_pass = private.get_auth()
        auth = CoinbaseExchangeAuth(key, secret, auth_pass)

        order = {
            'size': size,
            'price': price,
            'side': side,
            'product_id': 'BTC-USD',
        }

        return self.post('/orders', order, auth=auth)


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.realpath(__file__))

    gdax = gdax_interface()

    gdax.set_product_id('BTC-USD')

    json_response = gdax.post_limit_order('sell', 100000, 0.002)

    print json.dumps(json_response, indent=4)


    #   ben's awesome strategy here
    
    # now = datetime.datetime.now()
    # delta = datetime.timedelta(days=1)
    #
    # start = (now - delta).isoformat()
    # stop = now.isoformat()
    #
    # json_response = gdax.get_historic_rates(start,stop)
    #
    # gdax.plot_historic_rates(json_response)
