import yfinance as yf
accion = "DIS"
#Descarga el dataframe de la accion y el intervalo especificado.
data = yf.download(f'{accion}', start='2000-01-01', end='2010-12-31', ignore_tz = True)
# Guardar los datos en un archivo CSV
data.to_csv(f'samples/orcl_invalid_{accion}.csv')