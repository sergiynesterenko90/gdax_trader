import gdax


if __name__ == '__main__':
    print 'sup'

    public_client = gdax.PublicClient()

    ltcousd = public_client.get_product_historic_rates('LTC-USD', granularity='60')
    ltcoeur = public_client.get_product_historic_rates('LTC-EUR', granularity='60')

    print ltcousd
