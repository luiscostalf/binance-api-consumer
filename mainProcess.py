from binance.client import Client
import time
import datetime
import sys
import os

class mainProcess:
    def __init__(self, quantity, price, symbol, mode, min_ganho):
        self.client = Client("k8l0u4weAW5Z97sCU2dUX5OuGpis53THcLH20VvyW4rMVkY4KYM9gvY1vuzCSNJ7", "W7W3b2RtUY7h00rCOhKaD0K3el19QYrlLcP4ZstcXwwPStmDdhjskpq7lL4hD9q9")
        self.quantity = float(quantity)
        self.price = price
        self.symbol = str(symbol)
        self.mode = str(mode)
        self.amount_bought = (quantity * price)
        self.going = 0
        self.priceBefore = 0
        self.min_ganho = min_ganho
        self.bot()
        self.totalEarning = 0
        
    def bot(self):
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
                    f = open(self.symbol + 'statsLOG.txt', 'a')
                    log = open(self.symbol + 'lifeLOG.txt', 'a')
                    prices = self.client.get_all_tickers()
                    for price in prices:
                        if price['symbol'] == self.symbol + 'ETH':
                            f.write('\Price Last Check: ' + str(self.priceBefore) +'Was going: ' + str(self.going))
                            self.going = self.priceBefore - float(price['price'])
                            self.priceBefore = float(price['price'])
                            f.write('\nPrice Now: ' + str(self.priceBefore) +  ' Going Now: ' + str(self.going)  )
                    self.amountBought = (self.quantity * float(trades[0]['price']))
                    log.write('\nAlive: True' + ' Time: ' + str(datetime.datetime.time()) + 'PID: ' + os.getpid()   )
                    time.sleep(300)
                    f.close()
        except Exception as e:
                print e


    def buy(self):
        log = open(self.symbol + 'buyLOGStatus.txt', 'a')
        flag = True
        f = open(self.symbol + 'workfile.txt', 'a')
        while(flag):
            priceQuantity = int(self.quantity) * self.price
            earningETH = self.amount_bought - priceQuantity
            earningFee = earningETH - ((self.amount_bought * 0.001) + (priceQuantity * 0.001))
            if (earningFee >= self.min_ganho):
                self.totalEarning =- earningFee
                f.write('\nPrice:' + str(self.price) + ', PriceWithoutFee:' + str(earningETH) +
                    ', PriceWithFee:' + str(earningFee) + ', PriceUsedBuy:' + str(self.amount_bought))
                try: 
                    log.write('\START SELL quantity:'+ str(self.quantity) + ' price: ' + self.price + ' earningWithFee: ' + earningETH + ' earningWithoutFee: '+ earningFee)    
                    order = self.client.order_limit_buy(
                        symbol=self.symbol + 'ETH',
                        quantity=int(self.quantity),
                        price=str(self.price))
                    f.write('\quantity:' + str(self.quantity) + 'price:' + str(priceQuantity))
                    self.amountBought = self.quantity * self.price
                    self.mode = 'SELL'
                    log.write('\END SELL'+ str(datetime.datetime.time()) + ' TOTAL EARNING ' + str(self.totalEarning))
                    flag = False
                except Exception:
                    log.write('\nERROR SELLING '+ sys.exc_info()[0])
                    flag = False
                    continue
            else:
                self.price = self.price - 0.0000001
        f.close()

    def sell(self):
        log = open(self.symbol + 'sellLOGStatus.txt', 'a')
        f = open(self.symbol + 'sellLOG.txt', 'a')
        flag = True
        while(flag):
            priceQuantity = int(self.quantity) * self.price
            earningETH = priceQuantity - self.amount_bought
            earningFee = earningETH -((self.amount_bought * 0.001) + (priceQuantity * 0.001))
            f.write('\nPrice:' + str(self.price) + ', PriceWithoutFee:' + str(earningETH) +
                    ', PriceWithFee:' + str(earningFee) + ', PriceUsedBuy:' + str(self.amount_bought))
            if (earningFee >= self.min_ganho):
                self.totalEarning = + earningFee
                try: 
                    log.write('\START SELL quantity:'+ str(self.quantity) + ' price: ' + self.price + ' earningWithFee: ' + earningETH + ' earningWithoutFee: '+ earningFee)
                    order = self.client.order_limit_sell(
                        symbol=self.symbol + 'ETH',
                        quantity=int(self.quantity),
                        price=str(self.price))
                    f.write('\quantity:' + str(self.quantity) + 'price:' + str(priceQuantity))
                    self.amountBought = self.quantity * self.price
                    self.mode = 'BUY'
                    log.write('\END SELL'+ str(datetime.datetime.time()) + ' TOTAL EARNING ' + str(self.totalEarning))
                    flag = False
                except Exception:
                    log.write('\nERROR SELLING '+ sys.exc_info()[0])
                    flag = False
                    continue
            else:
                self.price = +self.price + 0.0000001
        f.close()
