import csv
from datetime import datetime
accion = "BRK"
input_file = f'samples/orcl_invalid_{accion}.csv'
output_file = f'samples/orcl_cleaned_{accion}.csv'

# Abrir el archivo de entrada y el archivo de salida
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Saltar la primera fila (encabezado con "Ticker")
    next(reader)

    # Escribir la fila de encabezado correctamente
    writer.writerow(['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

    # Iterar sobre las filas restantes
    for row in reader:
        # Eliminar los espacios extraños y la zona horaria en la fecha
        date = row[0]
        try:
            # Eliminar la zona horaria de la fecha
            date = date.split(' ')[0]  # Tomamos solo la parte de la fecha (YYYY-MM-DD)
            date = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')  # Asegurar el formato correcto

            # Escribir las filas con la fecha limpia
            writer.writerow([date] + row[1:])
        except ValueError:
            # Si hay un error con el formato de la fecha, podemos imprimir un mensaje y omitir la fila
            print(f"Error con la fecha: {row[0]}")
