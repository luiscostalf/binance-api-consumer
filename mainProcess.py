from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceWithdrawException
import time
from datetime import datetime
import sys
import os


class mainProcess:
    def __init__(self, quantity, price, symbol, mode, min_ganho):
        self.client = Client("k8l0u4weAW5Z97sCU2dUX5OuGpis53THcLH20VvyW4rMVkY4KYM9gvY1vuzCSNJ7", "W7W3b2RtUY7h00rCOhKaD0K3el19QYrlLcP4ZstcXwwPStmDdhjskpq7lL4hD9q9")
        if (quantity >= 1):
            self.quantity = int(quantity)
        else:
            self.quantity = float(quantity)
        self.price = price
        self.symbol = str(symbol)
        self.mode = str(mode)
        self.amount_bought = (quantity * price)
        self.going = 0
        self.priceBefore = 0
        self.min_ganho = min_ganho
        self.totalEarning = 0
        
        
    def bot(self):
        log = open(self.symbol + 'lifeLOG.txt', 'a')
        log.write('\nBot started' + ' Time: ' + str(datetime.now()) + 'PID: ' + str(os.getpid())   )
        log.write('\nAlive: True' + ' Time: ' + str(datetime.now()) + 'PID: ' + str(os.getpid())   )
        try:
            while(True):
                trades = self.client.get_open_orders(symbol=self.symbol + 'ETH')
                if (trades == []):
                    if (self.mode == 'SELL'):
                        f = open(self.symbol + 'balance.txt', 'a')
                        balance = self.client.get_asset_balance(asset='ETH')
                        balanceCoin = self.client.get_asset_balance(
                            asset=self.symbol)
                        f.write('\nBalance before:' + str(balance) +
                                'Balance ' + str(self.symbol) + 'before:' + str(balanceCoin))
                        self.sell()
                        balance = self.client.get_asset_balance(asset='ETH')
                        balanceCoin = self.client.get_asset_balance(
                            asset=self.symbol)
                        f.write('\nBalance after:' + str(balance) +
                                'Balance ' + str(self.symbol) + 'after:' + str(balanceCoin))
                        f.close()
                        time.sleep(10)
                    else:
                        f = open(self.symbol + 'balance.txt', 'a')
                        balance = self.client.get_asset_balance(asset='ETH')
                        balanceCoin = self.client.get_asset_balance(
                            asset=self.symbol)
                        f.write('\nBalance before:' + str(balance) +
                                'Balance ' + str(self.symbol) + 'before:' + str(balanceCoin))
                        self.buy()
                        balance = self.client.get_asset_balance(asset='ETH')
                        balanceCoin = self.client.get_asset_balance(
                            asset=self.symbol)
                        f.write('\nBalance after:' + str(balance) +
                                'Balance ' + str(self.symbol) + 'after:' + str(balanceCoin))
                        f.close()
                        time.sleep(10)
                else:
                    log = open(self.symbol + 'lifeLOG.txt', 'a')
                    f = open(self.symbol + 'statsLOG.txt', 'a')
                    prices = self.client.get_all_tickers()
                    for price in prices:
                        if price['symbol'] == self.symbol + 'ETH':
                            f.write('\Price Last Check: ' + str(self.priceBefore) +'Was going: ' + str(self.going))
                            self.going = self.priceBefore - float(price['price'])
                            self.priceBefore = float(price['price'])
                            f.write('\nPrice Now: ' + str(self.priceBefore) +  ' Going Now: ' + str(self.going)  )
                    self.amountBought = (self.quantity * float(trades[0]['price']))
                    log.write('\nAlive: True' + ' Time: ' + str(datetime.now()) + 'PID: ' + str(os.getpid())  )
                    time.sleep(300)
                    f.close()
                    log.close()
        except Exception as e:
                log = open(self.symbol + 'lifeLOG.txt', 'a')
                log.write('\nAlive: True' + ' Error: ' + str(e) + 'PID: ' + str(os.getpid())   )
                log.close()
                print e
        finally:
            pass



    def buy(self):
        log = open(self.symbol + 'buyLOGStatus.txt', 'a')
        flag = True
        f = open(self.symbol + 'workfile.txt', 'a')
        while(flag):
            priceQuantity = self.quantity * self.price
            earningETH = self.amount_bought - priceQuantity
            earningFee = earningETH - ((self.amount_bought * 0.001) + (priceQuantity * 0.001))
            f.write('\nPrice:' + str(self.price) + ', PriceWithoutFee:' + str(earningETH) + ', PriceWithFee:' + str(earningFee) + ', PriceUsedBuy:' + str(self.amount_bought))
            if float(earningFee) >= float(self.min_ganho):
                self.totalEarning =- earningFee
                try: 
                    log.write('\START BUY quantity:'+ str(self.quantity) + ' price: ' + str(self.price) + ' earningWithFee: ' + str(earningETH) + ' earningWithoutFee: '+ str(earningFee))
                    balance = self.client.get_asset_balance(asset='ETH')
                    while(balance['free'] < priceQuantity):
                        log.write('\No funds:'+ str(balance['free']) +  'money needed: ' + str(priceQuantity))
                        time.sleep(30)
                        balance = self.client.get_asset_balance(asset='ETH')
                    order = self.client.order_limit_buy(
                        symbol=self.symbol + 'ETH',
                        quantity=self.quantity,
                        price=str(self.price))
                    f.write('\quantity:' + str(self.quantity) + 'price:' + str(priceQuantity))
                    self.amountBought = self.quantity * self.price
                    self.mode = 'SELL'
                    log.write('\END SELL'+ str(datetime.now()) + ' TOTAL EARNING ' + str(self.totalEarning))
                    flag = False
                except BinanceAPIException as e:
                    print e.status_code
                    print e.message
                    log.write('\nERROR BUYING '+ str(e.message) + 'PID: ' + str(os.getpid()))
                    log.close()
                    flag = False
                    continue
            else:
                self.price = self.price - 0.00001
        f.close()
        log.close()

    def sell(self):
        log = open(self.symbol + 'sellLOGStatus.txt', 'a')
        f = open(self.symbol + 'sellLOG.txt', 'a')
        flag = True
        while(flag):
            priceQuantity = self.quantity * self.price
            earningETH = priceQuantity - self.amount_bought
            earningFee = earningETH -((self.amount_bought * 0.001) + (priceQuantity * 0.001))
            if float(earningFee) <= float(self.min_ganho):
                f.write('\nPrice:' + str(self.price) + ', PriceWithoutFee:' + str(earningETH) + ', PriceWithFee:' + str(earningFee) + ', PriceUsedBuy:' + str(self.min_ganho))
            if float(earningFee) >= float(self.min_ganho):
                flag = False
                self.totalEarning = + earningFee 
                try: 
                    log.write('\START SELL quantity:'+ str(self.quantity) + ' price: ' + str(self.price) + ' earningWithFee: ' + str(earningETH) + ' earningWithoutFee: '+ str(earningFee))
                    balance = self.client.get_asset_balance(asset=self.symbol)
                    while(balance['free'] < self.quantity):
                        log.write('\nNo funds:'+ str(balance['free']) +  'money needed: ' + str(self.quantity))
                        time.sleep(30)
                        balance = self.client.get_asset_balance(asset=self.symbol)
                    order = self.client.order_limit_sell(
                        symbol=self.symbol + 'ETH',
                        quantity=self.quantity,
                        price=str(self.price))
                    f.write('\quantity:' + str(self.quantity) + 'price:' + str(priceQuantity))
                    self.amountBought = self.quantity * self.price
                    self.mode = 'BUY'
                    log.write('\END SELL'+ str(datetime.now()) + ' TOTAL EARNING ' + str(self.totalEarning))
                    flag = False
                except BinanceAPIException as e:
                    print e.status_code
                    print e.message
                    log.write('\nERROR SELLING '+ str(e.message) + 'PID: ' + str(os.getpid()))
                    flag = False
            else:
                self.price = +self.price + 0.000001
        f.close()
        log.close()
