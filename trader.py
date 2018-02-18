import requests
import os

if __name__ == '__main__':
    print 'sup'


    script_dir = os.path.dirname(os.path.realpath(__file__))

    output_dir = os.path.join(script_dir, 'request.html')

    response = requests.get('https://api.gdax.com/products')

    print(response.json())
