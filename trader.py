import requests
import os
import json

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



if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.realpath(__file__))

    gdax = gdax_interface()
    json_out = gdax.get_order_book(level=2)

    print json.dumps(json_out, indent=4)
