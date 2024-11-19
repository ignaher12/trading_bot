from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import yfinance as yf
# Import the backtrader platform
import backtrader as bt

class CombinedStrategy(bt.Strategy):
    params = (
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
        ('rsi_periods', 14),
        ('rsi_oversold', 35),
        ('rsi_overbought', 65),
        ('bbands_period', 20),
        ('bbands_devfactor', 2),
        ('portfolio_percent', 0.10),
    )

    def __init__(self):
        self.indicators = {}
        for i, data in enumerate(self.datas):  # Iterar por cada instrumento agregado al dataset.
            self.indicators[data] = {
                #Indicador MACD, indica senales de entrada y salida.
                'macd': bt.indicators.MACD(data,
                                           period_me1=self.params.macd1,
                                           period_me2=self.params.macd2,
                                           period_signal=self.params.macdsig),
                #Indicador RSI, indica senales de entrada y de salida.
                'rsi': bt.indicators.RSI(data, period=self.params.rsi_periods),
                #Bandas de Bollinger.
                'bbands': bt.indicators.BollingerBands(data,
                                                       period=self.params.bbands_period,
                                                       devfactor=self.params.bbands_devfactor),
            }
            self.indicators[data]['macd_diff'] = (
                self.indicators[data]['macd'].macd - self.indicators[data]['macd'].signal
            )
            self.current_day = 0

    def next(self):
        self.current_day += 1
        for i, data in enumerate(self.datas):
            ind = self.indicators[data]
            macd_diff = ind['macd_diff']

            # Compra
            if ((2740 - self.current_day) > 10):  # Verifica si no hay posición en este activo
                macd_trending_up = macd_diff[0] > macd_diff[-1]
                price_near_bottom = data.close[0] <= ind['bbands'].lines.bot[0] * 1.02
                rsi_oversold = ind['rsi'][0] < self.params.rsi_oversold

                if macd_trending_up and (price_near_bottom or rsi_oversold):
                    size = self.calculate_position_size(data)
                    self.buy(data=data, size=size*0.05)
                    print(f'COMPRA: {data._name} - Precio: {data.close[0]}')

            # Venta
            if self.getposition(data):  # Verifica si hay posición en este activo
                macd_trending_down = macd_diff[0] < macd_diff[-1]
                price_near_top = data.close[0] >= ind['bbands'].lines.top[0] * 0.98
                rsi_overbought = ind['rsi'][0] > self.params.rsi_overbought

                if macd_trending_down and (price_near_top or rsi_overbought):
                    self.sell(data=data)
                    print(f'VENTA: {data._name} - Precio: {data.close[0]}')

    def calculate_position_size(self, data):
        portfolio_value = self.broker.getvalue()
        position_value = portfolio_value * self.params.portfolio_percent
        current_price = data.close[0]
        size = position_value / current_price
        return int(size)

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    #Agrego la estrategia
    initial_cash = 10000.0
    #Seteo comision del broker.
    cerebro.broker.setcommission(commission=0.001)
    # Descargar el csv 

        #Hay que ejecutar el cleaner para formatear el archivo cuando recien se descarga
        #esto deberiamos solucionarlo pero no se como.
        
    symbols = ['AAPL', 'BRK', 'NVDA']
    data_files = [
        'samples/orcl_cleaned_AAPL.csv',
        'samples/orcl_cleaned_BRK.csv',
        'samples/orcl_cleaned_NVDA.csv'
    ]
    #file_path = 'samples/orcl_cleaned_NVDA.csv'
    # Añadir los datos al cerebro
    for i, file_path in enumerate(data_files):
        data = bt.feeds.YahooFinanceCSVData(
            dataname=data_files[i],
            fromdate=datetime.datetime(2000, 1, 1),
            todate=datetime.datetime(2002, 12, 31),
            reverse=False
        )
        cerebro.adddata(data, name=symbols[i])

    # Agrega la data al cerebro.
    cerebro.addstrategy(CombinedStrategy)
    # Setea plata en el broker.
    cerebro.broker.setcash(initial_cash)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    init = cerebro.broker.getvalue()  
    # Run over everything
    cerebro.run()

    open_positions_value = 0
    for position in cerebro.broker.positions.values():
        open_positions_value += position.size * position.price

    # Calcula el valor total del portfolio
    total_portfolio_value = cerebro.broker.getvalue() + open_positions_value
    money_gained = total_portfolio_value - initial_cash  # Restamos el cash inicial

    # Calcula el porcentaje de ganancia respecto al portfolio inicial
    percentage_gain = (money_gained / initial_cash) * 100

    # Imprime los resultados
    print(f'Portfolio final (efectivo + posiciones abiertas): ${total_portfolio_value:.2f}')
    print(f'Portfolio en efectivo: ${cerebro.broker.getvalue():.2f}')
    print(f'Valor de posiciones abiertas: ${open_positions_value:.2f}')
    print(f'Dinero total ganado: ${money_gained:.2f}')
    print(f'Porcentaje del portfolio inicial ganado: %{percentage_gain:.2f}')
    
    try:
        cerebro.plot()
    except: 
        print('Error al graficar')