from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import yfinance as yf
# Import the backtrader platform
import backtrader as bt

#intento de estrategia de vela - martillo para comprar y estrella de la tarde para vender.
class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.dataopen= self.datas[0].open
    def next(self):
        # Simply log the closing price of the series from the reference
        #self.log('Close, %.2f' % self.dataclose[0])
        
        if self.dataclose[0] < self.dataclose[-1]:
            # current close less than previous close
            if self.dataclose[-1] < self.dataclose[-2]:
                # previous close less than the previous close
                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.buy()
                if self.dataopen[0] < self.dataclose[0]:
                    # previous close less than the previous close
                    # BUY, BUY, BUY!!! (with all possible default parameters)
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.buy()
        else:
            if self.dataclose[-1] > self.dataclose[-2]:
                self.sell()


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    #Agrego la estrategia
    cerebro.addstrategy(TestStrategy)
    #Seteo comision del broker.
    cerebro.broker.setcommission(commission=0.001)
    # Descargar el csv 
    #data = yf.download('AAPL', start='2000-01-01', end='2000-12-31', ignore_tz = True)
    # Guardar los datos en un archivo CSV
    #data.to_csv('samples/orcl_invalid.csv')
    
        #Hay que ejecutar el cleaner para formatear el archivo cuando recien se descarga
        #esto deberiamos solucionarlo pero no se como.
        
    datapath = 'samples/orcl_cleaned.csv'

    # Formatea la data del csv con los parametros del framework. 
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2000, 1, 1),
        todate=datetime.datetime(2000, 12, 31),
        reverse=False
    )
    # Agrega la data al cerebro.
    cerebro.adddata(data)
    # Setea plata en el broker.
    cerebro.broker.setcash(100000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    init = cerebro.broker.getvalue()
    
    # Run over everything
    cerebro.run()
    cerebro.plot()
    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    end = cerebro.broker.getvalue()
    print(f"El mega agente de bolsas recaudo un total de $ {end-init}")