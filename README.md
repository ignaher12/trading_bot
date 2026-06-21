# Trading Bot — Backtesting de estrategia combinada

> **Proyecto académico.** Este código fue desarrollado como trabajo práctico para una
> materia de la facultad. Su objetivo es educativo: practicar la descarga de datos
> financieros, la limpieza de datos y el *backtesting* de una estrategia de trading.

## Descripción

El proyecto implementa un bot que simula (*backtesting*) una estrategia de trading sobre
datos históricos de acciones. La estrategia combina tres indicadores técnicos clásicos:

- **MACD** (Moving Average Convergence Divergence) — señales de entrada/salida según la tendencia.
- **RSI** (Relative Strength Index) — detección de zonas de sobrecompra y sobreventa.
- **Bandas de Bollinger** — referencia de precios extremos (bandas superior e inferior).

La simulación se corre con la librería [`backtrader`](https://www.backtrader.com/), partiendo
de un capital inicial de USD 10.000 y una comisión de broker del 0,1 %.

## Estructura del proyecto

```
trading_bot/
├── data.py          # Descarga datos históricos desde Yahoo Finance (yfinance)
├── cleaner.py       # Limpia los CSV descargados (normaliza fechas y encabezados)
├── strategy.py      # Define la estrategia y corre el backtest con backtrader
└── samples/         # CSVs de ejemplo (datos crudos "invalid" y limpios "cleaned")
```

### Flujo de trabajo

1. **`data.py`** — Descarga los datos históricos de una acción desde Yahoo Finance y los
   guarda como `samples/orcl_invalid_<TICKER>.csv` (datos crudos).
2. **`cleaner.py`** — Toma el CSV crudo, limpia el formato de fechas y los encabezados, y
   genera `samples/orcl_cleaned_<TICKER>.csv` listo para usar.
3. **`strategy.py`** — Carga los CSV limpios, aplica la estrategia combinada y muestra el
   resultado del backtest (valor final del portfolio, ganancia y gráfico).

## Acciones incluidas

Los datos de ejemplo abarcan: **AAPL, AMD, BRK, DIS, NVDA y WMT**.

En `strategy.py` se pueden elegir tres conjuntos de acciones modificando la variable `datos`:

| `datos` | Conjunto                          |
|---------|-----------------------------------|
| `1`     | AAPL, BRK, NVDA                   |
| `2`     | AMD, DIS, WMT                     |
| `3`     | AMD, AAPL, NVDA (por defecto)     |

## Requisitos

- Python 3.x
- Dependencias:

```bash
pip install yfinance backtrader matplotlib
```

> `matplotlib` se usa para graficar los resultados (`cerebro.plot()`).

## Uso

Desde la carpeta `trading_bot/`:

```bash
# 1. (Opcional) Descargar datos nuevos de una acción
#    Editar la variable `accion` dentro de data.py y ejecutar:
python data.py

# 2. (Opcional) Limpiar el CSV descargado
#    Editar la variable `accion` dentro de cleaner.py y ejecutar:
python cleaner.py

# 3. Correr el backtest con los datos ya incluidos en samples/
python strategy.py
```

Al finalizar, `strategy.py` imprime en consola el valor final del portfolio, el valor de las
posiciones abiertas, el dinero ganado y el porcentaje de ganancia, y abre un gráfico con la
evolución de las operaciones.

## Notas

- Los CSV de la carpeta `samples/` ya vienen incluidos, por lo que el backtest puede correrse
  sin necesidad de volver a descargar datos.
- El rango de fechas del backtest está acotado en el código (por defecto, años 2000–2002) y
  puede ajustarse en `strategy.py`.
