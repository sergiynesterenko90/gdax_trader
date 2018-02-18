import requests
import os
import json
import datetime
import matplotlib.pyplot as plt

class gdax_interface:
    def __init__(self):
        self.url = 'https://api.gdax.com'
        self.product_id = 'LTC-USD'

    def get(self, path):
        response = requests.get(self.url + path)

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


    def post_limit_order(self, type, side, price, size, post_only = True):

        request_url = '/orders/?'
        request_url += 'client_oid=' + str(self.client_oid)
        request_url += '?type=' + str('limit')
        request_url += '?side=' + str(side)
        request_url += '?product_id=' + str(self.proudct_id)
        request_url += '?price=' + str(price)
        request_url += '?size=' + str(size)
        request_url += '?post_only=True'

        return self.post






if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.realpath(__file__))

    gdax = gdax_interface()
    # json_out = gdax.get_order_book(level=2)

    now = datetime.datetime.now()
    delta = datetime.timedelta(days=1)

    start = (now - delta).isoformat()
    stop = now.isoformat()

    json_response = gdax.get_historic_rates(start,stop)

    gdax.plot_historic_rates(json_response)

    # print json.dumps(json_out, indent=4)
